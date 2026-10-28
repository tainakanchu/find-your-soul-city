"""ERA5 climate normals (1990-2019) per GHS-UCDB urban centre, from the WeatherBench 2 ERA5 climatology.

Source: WeatherBench 2 (WB2) "ERA5 hourly climatology" zarr on public GCS
    gs://weatherbench2/datasets/era5-hourly-climatology/1990-2019_6h_1440x721.zarr
Every variable is [hour=4 (00/06/12/18 UTC), dayofyear=366, latitude=721 (90 -> -90), longitude=1440 (0..359.75)],
float32, chunked [3, 3, 721, 1440] (one chunk ~ 20 MB compressed). Each value is the 1990-2019 mean for that
UTC hour and day of year, smoothed by WB2 with a 61-day triangular window (weatherbench2/utils.py).

We stream every chunk once per variable, keep only the 0.25 deg cells needed for the target cities and the
524-centre reference set, and cache those small per-cell arrays under .cache/raw/era5/.

Per-city cell rule: ERA5 cell centres inside the UCDB polygon with land_sea_mask >= 0.5 (cos-lat weighted
mean); if there is none, the land cell nearest to the polygon's representative point.

Validation helpers (not used to produce values): GHS-UCDB CLIMATE theme (C3S bioclimatic indicators, ERA5
derived), GHCN-Monthly v4 station normals (independent, for the elevation / lapse-rate question), and the
WB2 hourly ERA5 store (to measure the bias of averaging only 00/06/12/18 UTC).
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import math
import tarfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import numcodecs
import numpy as np
import pyogrio
import requests
import shapely

from .cities import City, load_cities, reference_centres, ucdb_gpkg
from .common import CACHE, REFERENCE, Interim, fetch, record_dataset

SOURCE_ID = "era5"
RAW = CACHE / "era5"
GCS = "https://storage.googleapis.com/weatherbench2/datasets"
CLIM_URL = f"{GCS}/era5-hourly-climatology/1990-2019_6h_1440x721.zarr"
STATIC_URL = f"{GCS}/era5/1959-2022-6h-1440x721.zarr"
HOURLY_URL = f"{GCS}/era5/1959-2023_01_10-full_37-1h-0p25deg-chunk-1.zarr"
LICENSE_URLS = [f"{GCS}/era5-hourly-climatology/LICENSE", f"{GCS}/era5/LICENSE"]
CDS_ERA5_CATALOGUE = "https://cds.climate.copernicus.eu/api/catalogue/v1/collections/reanalysis-era5-single-levels"
GHCNM_URL = "https://www.ncei.noaa.gov/pub/data/ghcn/v4/ghcnm.tavg.latest.qcf.tar.gz"
PERIOD = "1990-2019"
YEARS = range(1990, 2020)

# Read from the WB2 climatology store. Its 2m_dewpoint_temperature and all mean_*_radiation_flux arrays are
# entirely NaN (every chunk is the same 150 877-byte all-fill block), so those are not used.
VARS = {
    "t2m": "2m_temperature",  # K (cross-check of the smoothing only)
    "tp24": "total_precipitation_24hr",  # m per 24 h accumulation ending at the given hour
    "tcc": "total_cloud_cover",  # 0-1
}
# Read from the WB2 copy of hourly ERA5 at 00/06/12/18 UTC for every day 1990-2019 -> unsmoothed monthly means.
HOURLY_VARS = {"t2m": "2m_temperature", "d2m": "2m_dewpoint_temperature"}
STATIC_VARS = {"lsm": "land_sea_mask", "z": "geopotential_at_surface"}
G0 = 9.80665  # m s-2, WMO standard gravity used by ECMWF to convert geopotential to height
LAND_MIN = 0.5

# Day-of-year -> month on a 365-day calendar (WB2 indexes by ordinal day; day 366 is dropped, see notes).
MONTH_LEN = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
DOY_MONTH = np.repeat(np.arange(12), MONTH_LEN)  # 365 entries
N_LEAP = sum(1 for y in YEARS if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0)
# Mean month length over 1990-2019 (February gets the leap days of the period) -> monthly/annual totals.
MEAN_MONTH_DAYS = MONTH_LEN + np.array([0, N_LEAP / len(YEARS)] + [0] * 10)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Standard-atmosphere tropospheric lapse rate (ICAO / U.S. Standard Atmosphere 1976), K per m.
STD_LAPSE = 0.0065
# Decision taken from the GHCN-M validation (see etl/notes/era5.md): report ERA5 temperatures at the model
# orography without a lapse-rate correction, and flag the elevation mismatch in `detail`.
APPLY_LAPSE = False

_tls = threading.local()


def _session() -> requests.Session:
    s = getattr(_tls, "s", None)
    if s is None:
        s = _tls.s = requests.Session()
    return s


def _get(url: str, retries: int = 6) -> bytes:
    for attempt in range(retries + 1):
        try:
            r = _session().get(url, timeout=180)
            r.raise_for_status()
            return r.content
        except requests.RequestException:
            if attempt == retries:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


# --------------------------------------------------------------------------------------------- zarr access
class Store:
    def __init__(self, url: str, name: str):
        self.url = url
        self.path = fetch(f"{url}/.zmetadata", RAW / f"{name}.zmetadata", record=False)
        self.raw = self.path.read_bytes()
        self.meta = json.loads(self.raw)["metadata"]

    def zarray(self, var: str) -> dict:
        return self.meta[f"{var}/.zarray"]

    def attrs(self, var: str) -> dict:
        return self.meta.get(f"{var}/.zattrs", {})

    def chunk(self, var: str, key: str) -> np.ndarray:
        za = self.zarray(var)
        raw = _get(f"{self.url}/{var}/{key}")
        buf = numcodecs.get_codec(za["compressor"]).decode(raw)
        return np.frombuffer(buf, dtype=za["dtype"]).reshape(za["chunks"])

    def whole(self, var: str) -> np.ndarray:
        za = self.zarray(var)
        assert za["shape"] == za["chunks"], var
        return self.chunk(var, ".".join("0" * len(za["shape"])))

    def record(self, key_name: str, variables: list[str], note: str) -> str:
        record_dataset(
            self.url,
            kind="zarr v2 store (consolidated .zmetadata), read chunk by chunk",
            variables={v: {"shape": self.zarray(v)["shape"], "chunks": self.zarray(v)["chunks"],
                           "attrs": self.attrs(v)} for v in variables},
            store_attrs=self.meta.get(".zattrs", {}),
            zmetadata_sha256=hashlib.sha256(self.raw).hexdigest(),
            note=note,
        )
        return self.url


def grid(store: Store) -> tuple[np.ndarray, np.ndarray]:
    lat = store.whole("latitude").astype(np.float64)
    lon = store.whole("longitude").astype(np.float64)
    assert lat[0] == 90 and lat[-1] == -90 and np.all(np.diff(lat) < 0), "latitude must be 90 -> -90"
    assert lon[0] == 0 and np.allclose(np.diff(lon), 0.25), "longitude must be 0..359.75"
    return lat, lon


def static_fields(st: Store) -> dict[str, np.ndarray]:
    out = {}
    for k, v in STATIC_VARS.items():
        p = RAW / f"static_{v}.npy"
        if not p.exists():
            np.save(p, st.whole(v))
        out[k] = np.load(p)
    return out


# --------------------------------------------------------------------------------------------- cells
def _haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dlat, dlon = p2 - p1, np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlon / 2) ** 2
    return 6371.0 * 2 * np.arcsin(np.sqrt(a))


def select_cells(c: City, lat: np.ndarray, lon: np.ndarray, lsm: np.ndarray) -> dict | None:
    lonw = (lon + 180) % 360 - 180
    minx, miny, maxx, maxy = shapely.bounds(c.geom)
    rows = np.flatnonzero((lat >= miny) & (lat <= maxy))
    cols = np.flatnonzero((lonw >= minx) & (lonw <= maxx))
    rr, cc = np.meshgrid(rows, cols, indexing="ij")
    rr, cc = rr.ravel(), cc.ravel()
    inside = shapely.contains_xy(c.geom, lonw[cc], lat[rr]) if rr.size else np.zeros(0, bool)
    rr, cc = rr[inside], cc[inside]
    n_inside = int(rr.size)
    land = lsm[rr, cc] >= LAND_MIN
    if land.any():
        rr, cc = rr[land], cc[land]
        rule, dist = "centres_in_polygon_land", None
    else:
        r0 = np.flatnonzero(np.abs(lat - c.lat) <= 2.0)
        dlon = (lonw - c.lon + 180) % 360 - 180
        c0 = np.flatnonzero(np.abs(dlon) <= 2.0 / max(math.cos(math.radians(c.lat)), 0.2))
        R, C = np.meshgrid(r0, c0, indexing="ij")
        R, C = R.ravel(), C.ravel()
        ok = lsm[R, C] >= LAND_MIN
        R, C = R[ok], C[ok]
        if not R.size:
            return None  # no ERA5 land cell within 2 deg (e.g. small islands) -> missing
        d = _haversine_km(c.lat, c.lon, lat[R], lonw[C])
        k = int(np.argmin(d))
        rr, cc = R[k:k + 1], C[k:k + 1]
        rule, dist = "nearest_land_cell_to_representative_point", round(float(d[k]), 1)
    return {"rows": rr, "cols": cc, "rule": rule, "n_cells": int(rr.size), "n_centres_in_polygon": n_inside,
            "nearest_km": dist}


# --------------------------------------------------------------------------------------------- extraction
def extract(store: Store, var: str, rows: np.ndarray, cols: np.ndarray) -> np.ndarray:
    """Return var[:, :, rows, cols] -> (hour, dayofyear, ncells), streaming each chunk once (cached)."""
    cache = RAW / f"cells_{var}.npz"
    if cache.exists():
        z = np.load(cache)
        idx = {(int(r), int(c)): i for i, (r, c) in enumerate(zip(z["rows"], z["cols"], strict=True))}
        if all((int(r), int(c)) in idx for r, c in zip(rows, cols, strict=True)):
            sel = np.array([idx[(int(r), int(c))] for r, c in zip(rows, cols, strict=True)], dtype=int)
            return z["data"][:, :, sel]
    za = store.zarray(var)
    nh, nd = za["shape"][:2]
    ch, cd = za["chunks"][:2]
    keys = [(i, j) for i in range(math.ceil(nh / ch)) for j in range(math.ceil(nd / cd))]
    out = np.full((nh, nd, rows.size), np.nan, dtype=np.float32)
    t0, done = time.time(), [0]
    lock = threading.Lock()

    def work(k):
        i, j = k
        a = store.chunk(var, f"{i}.{j}.0.0")
        h1, d1 = min(ch, nh - i * ch), min(cd, nd - j * cd)
        out[i * ch:i * ch + h1, j * cd:j * cd + d1] = a[:h1, :d1][:, :, rows, cols]
        with lock:
            done[0] += 1
            if done[0] % 20 == 0:
                print(f"    {var}: {done[0]}/{len(keys)} chunks, {time.time() - t0:.0f}s", flush=True)

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(work, keys))
    assert not np.isnan(out).any(), f"{var}: NaN after extraction"
    np.savez(cache, rows=rows, cols=cols, data=out)
    return out


# --------------------------------------------------------------------------------------------- climatology
def daily(a: np.ndarray) -> np.ndarray:
    """(4, 366, n) -> (365, n): mean of the 4 UTC samples, day 366 dropped."""
    return a[:, :365].mean(axis=0)


def monthly_mean(d: np.ndarray) -> np.ndarray:
    """(365, n) -> (12, n)."""
    return np.stack([d[DOY_MONTH == m].mean(axis=0) for m in range(12)])


def city_mean(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    return (x * w).sum(axis=-1) / w.sum()


# --------------------------------------------------------------------------------------------- validation inputs
def ucdb_columns(layer: str, cols: list[str]) -> dict[int, dict[str, float]]:
    _m, _f, _g, fields = pyogrio.raw.read(ucdb_gpkg(), layer=layer, columns=["ID_UC_G0", *cols], read_geometry=False)
    ids = fields[0]
    return {int(ids[i]): {c: float(fields[k + 1][i]) for k, c in enumerate(cols)} for i in range(len(ids))}


def hourly_monthly_means(rows: np.ndarray, cols: np.ndarray) -> dict[str, np.ndarray]:
    """Monthly means 1990-2019 (12, ncells) of HOURLY_VARS from all 00/06/12/18 UTC fields (43 830 per variable).

    Per-year partial sums are cached (.cache/raw/era5/hourly_<year>.npz) so an interrupted run resumes.
    """
    st = Store(HOURLY_URL, "hourly")
    tz = st.zarray("time")
    t0 = dt.datetime(1959, 1, 1)
    tchunks: dict[int, np.ndarray] = {}

    def time_at(i: int) -> int:
        ci = i // tz["chunks"][0]
        if ci not in tchunks:
            tchunks[ci] = st.chunk("time", str(ci))
        return int(tchunks[ci][i - ci * tz["chunks"][0]])

    sums = {k: np.zeros((12, rows.size)) for k in HOURLY_VARS}
    counts = np.zeros(12)
    for y in YEARS:
        cache = RAW / f"hourly_{y}.npz"
        if cache.exists():
            z = np.load(cache)
            if np.array_equal(z["rows"], rows) and np.array_equal(z["cols"], cols):
                for k in HOURLY_VARS:
                    sums[k] += z[k]
                counts += z["counts"]
                continue
        n_days = (dt.datetime(y + 1, 1, 1) - dt.datetime(y, 1, 1)).days
        steps = [(dt.datetime(y, 1, 1) + dt.timedelta(days=d, hours=h)) for d in range(n_days) for h in (0, 6, 12, 18)]
        idx = [int((t - t0).total_seconds() // 3600) for t in steps]
        assert time_at(idx[0]) == idx[0] and time_at(idx[-1]) == idx[-1], "hourly time axis not contiguous"
        month = np.array([t.month - 1 for t in steps])
        ys = {k: np.zeros((12, rows.size)) for k in HOURLY_VARS}
        yc = np.bincount(month, minlength=12).astype(float)
        t_start = time.time()
        for k, var in HOURLY_VARS.items():
            vals = np.zeros((len(idx), rows.size), np.float64)

            def work(j, var=var, vals=vals, idx=idx):
                vals[j] = st.chunk(var, f"{idx[j]}.0.0")[0][rows, cols]

            with ThreadPoolExecutor(16) as ex:
                list(ex.map(work, range(len(idx))))
            assert np.isfinite(vals).all(), f"{var} {y}: non-finite values"
            for m in range(12):
                ys[k][m] = vals[month == m].sum(axis=0)
        np.savez(cache, rows=rows, cols=cols, counts=yc, **ys)
        print(f"    hourly store {y}: {len(idx)} steps x {len(HOURLY_VARS)} vars, {time.time() - t_start:.0f}s",
              flush=True)
        for k in HOURLY_VARS:
            sums[k] += ys[k]
        counts += yc
    st.record("hourly", list(HOURLY_VARS.values()) + ["2m_temperature", "total_cloud_cover"],
              "WB2 copy of hourly ERA5; 00/06/12/18 UTC of every day 1990-2019 streamed for t2m/d2m monthly means, "
              "plus 48 days x 24 h of 2010 for the 6-hourly sampling-bias check")
    return {k: sums[k] / counts[:, None] for k in HOURLY_VARS}


def hourly_sampling_bias(rows: np.ndarray, cols: np.ndarray) -> dict[str, np.ndarray]:
    """24-hourly mean minus mean of 00/06/12/18 UTC, for 48 days of 2010 (days 1, 8, 15, 22 of each month)."""
    cache = RAW / "hourly_sampling_2010.npz"
    if cache.exists():
        z = np.load(cache)
        if np.array_equal(z["rows"], rows) and np.array_equal(z["cols"], cols):
            return {k: z[k] for k in ("t2m", "tcc")}
    st = Store(HOURLY_URL, "hourly")
    tz = st.zarray("time")
    t0 = dt.datetime(1959, 1, 1)
    days = [dt.datetime(2010, m, d) for m in range(1, 13) for d in (1, 8, 15, 22)]
    idx = [int((day - t0).total_seconds() // 3600) + h for day in days for h in range(24)]
    tchunk = {}
    for i in (idx[0], idx[-1]):
        ci = i // tz["chunks"][0]
        if ci not in tchunk:
            tchunk[ci] = st.chunk("time", str(ci))
        assert int(tchunk[ci][i - ci * tz["chunks"][0]]) == i, "hourly store time axis is not contiguous"
    res = {}
    for key, var in (("t2m", "2m_temperature"), ("tcc", "total_cloud_cover")):
        vals = np.zeros((len(idx), rows.size), np.float32)

        def work(k, var=var, vals=vals):
            vals[k] = st.chunk(var, f"{idx[k]}.0.0")[0][rows, cols]

        print(f"  hourly {var}: {len(idx)} chunks", flush=True)
        with ThreadPoolExecutor(8) as ex:
            list(ex.map(work, range(len(idx))))
        v = vals.reshape(len(days), 24, rows.size)
        res[key] = (v.mean(axis=1) - v[:, ::6].mean(axis=1)).mean(axis=0)  # per cell
    np.savez(cache, rows=rows, cols=cols, **res)
    return res


def ghcnm_normals() -> list[dict]:
    """GHCN-M v4 QCF stations with a 1990-2019 TAVG normal (>= 20 valid years in every calendar month)."""
    tgz = fetch(GHCNM_URL, RAW / "ghcnm" / "ghcnm.tavg.latest.qcf.tar.gz", timeout=600)
    inv, dat = {}, None
    with tarfile.open(tgz) as tf:
        for m in tf.getmembers():
            if m.name.endswith(".inv"):
                for line in tf.extractfile(m).read().decode("latin-1").splitlines():
                    inv[line[0:11]] = (float(line[12:20]), float(line[21:30]), float(line[31:37]), line[38:68].strip())
            elif m.name.endswith(".dat"):
                dat = tf.extractfile(m).read().decode("latin-1")
    sums: dict[str, np.ndarray] = {}
    cnts: dict[str, np.ndarray] = {}
    for line in dat.splitlines():
        y = int(line[11:15])
        if y not in YEARS or line[15:19] != "TAVG":
            continue
        sid = line[0:11]
        s = sums.setdefault(sid, np.zeros(12))
        n = cnts.setdefault(sid, np.zeros(12))
        for m in range(12):
            o = 19 + 8 * m
            v = int(line[o:o + 5])
            if v != -9999 and line[o + 6] == " ":  # QC flag blank = passed
                s[m] += v / 100.0
                n[m] += 1
    out = []
    for sid, n in cnts.items():
        if n.min() >= 20 and sid in inv:
            la, lo, el, name = inv[sid]
            if el <= -999:
                continue
            mon = sums[sid] / n
            out.append({"id": sid, "lat": la, "lon": lo, "elev": el, "name": name,
                        "tann": float((mon * MONTH_LEN).sum() / 365)})
    return out


# --------------------------------------------------------------------------------------------- main
def pearson(a, b) -> float:
    return float(np.corrcoef(a, b)[0, 1])


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    clim = Store(CLIM_URL, "clim")
    stat = Store(STATIC_URL, "static")
    lat, lon = grid(clim)
    lat_s, lon_s = grid(stat)
    assert np.array_equal(lat, lat_s) and np.array_equal(lon, lon_s)
    hours = clim.whole("hour").tolist()
    doy = clim.whole("dayofyear")
    assert hours == [0, 6, 12, 18] and doy[0] == 1 and doy[-1] == 366
    for k, v in VARS.items():
        assert clim.zarray(v)["shape"] == [4, 366, 721, 1440], v
    assert clim.attrs(VARS["t2m"])["units"] == "K" and clim.attrs(VARS["tp24"])["units"] == "m"
    sf = static_fields(stat)
    lsm, zsfc = sf["lsm"], sf["z"] / G0

    targets = load_cities()
    refs = reference_centres()
    allc: dict[str, City] = {c.city_id: c for c in (*targets, *refs)}
    sel = {cid: select_cells(c, lat, lon, lsm) for cid, c in allc.items()}
    no_land = sorted(cid for cid, s in sel.items() if s is None)
    sel = {cid: s for cid, s in sel.items() if s is not None}
    cells = sorted({(int(r), int(c)) for s in sel.values() for r, c in zip(s["rows"], s["cols"], strict=True)})
    rows = np.array([r for r, _ in cells])
    cols = np.array([c for _, c in cells])
    pos = {rc: i for i, rc in enumerate(cells)}
    print(f"{len(allc)} centres -> {len(cells)} unique ERA5 cells", flush=True)

    raw = {}
    for k, v in VARS.items():
        print(f"  extracting {v}", flush=True)
        raw[k] = extract(clim, v, rows, cols)

    # unit conversion per cell
    t_wb2 = monthly_mean(daily(raw["t2m"])) - 273.15  # degC, 61-day smoothed climatology (cross-check only)
    print("  monthly means from the hourly store", flush=True)
    hm = hourly_monthly_means(rows, cols)
    t_m = hm["t2m"] - 273.15
    d_m = hm["d2m"] - 273.15
    p_day = daily(raw["tp24"]) * 1000.0  # mm/day: mean 24-h accumulation (m) over the four end hours
    p_m = monthly_mean(p_day) * MEAN_MONTH_DAYS[:, None]  # mm/month
    c_ann = daily(raw["tcc"]).mean(axis=0) * 100.0  # %
    # consistency check of the tp24 interpretation: the 4 end hours of tp24 must agree with each other
    tp_h = raw["tp24"][:, :365].mean(axis=1)  # (4, n): annual mean per end hour
    wet = tp_h.mean(axis=0) >= 0.3e-3
    tp_spread = float(np.max(np.abs(tp_h[:, wet] / tp_h[:, wet].mean(axis=0) - 1)))
    del raw

    print("  hourly sampling-bias check", flush=True)
    hb = hourly_sampling_bias(rows, cols)

    ucdb_ids = {c.ucdb_id for c in allc.values()}
    climcols = ucdb_columns("GHSL_UCDB_THEME_CLIMATE_GLOBE_R2024A",
                            ["CL_B01_CUR_1990", "CL_B01_CUR_2000", "CL_B01_CUR_2010",
                             "CL_B12_CUR_1990", "CL_B12_CUR_2000", "CL_B12_CUR_2010"])
    geo = ucdb_columns("GHSL_UCDB_THEME_GEOGRAPHY_GLOBE_R2024A", ["GE_ELV_AVG_2025"])
    climcols = {k: v for k, v in climcols.items() if k in ucdb_ids}

    rec: dict[str, dict] = {}
    for cid, c in allc.items():
        if cid not in sel:
            continue
        s = sel[cid]
        ii = np.array([pos[(int(r), int(cc))] for r, cc in zip(s["rows"], s["cols"], strict=True)])
        w = np.cos(np.radians(lat[s["rows"]]))
        tm, dm, pm = city_mean(t_m[:, ii], w), city_mean(d_m[:, ii], w), city_mean(p_m[:, ii], w)
        z_era5 = float(city_mean(zsfc[s["rows"], s["cols"]], w))
        elev = geo.get(c.ucdb_id, {}).get("GE_ELV_AVG_2025", float("nan"))
        iw, ic = int(np.argmax(tm)), int(np.argmin(tm))
        rec[cid] = {
            "city": c, "sel": s, "tm": tm, "dm": dm, "pm": pm,
            "t_ann": float((tm * MEAN_MONTH_DAYS).sum() / MEAN_MONTH_DAYS.sum()),
            "p_ann": float(pm.sum()), "cloud": float(city_mean(c_ann[ii], w)),
            "t_wb2": city_mean(t_wb2[:, ii], w),
            "iw": iw, "ic": ic, "z_era5": z_era5, "elev": elev,
            "lsm_mean": float(city_mean(lsm[s["rows"], s["cols"]], w)),
            "hb_t": float(city_mean(hb["t2m"][ii], w)), "hb_c": float(city_mean(hb["tcc"][ii], w)) * 100,
        }

    # ------------------------------------------------ validation 1: UCDB CLIMATE (C3S bioclimatic indicators)
    val: dict[str, object] = {"tp24_end_hour_max_rel_spread": round(tp_spread, 4)}

    def compare(ids, key, col_t, col_p):
        a_t, b_t, a_p, b_p, rows_ = [], [], [], [], []
        for cid in ids:
            r = rec[cid]
            u = climcols.get(r["city"].ucdb_id)
            if not u:
                continue
            bt = np.mean([u[x] for x in col_t])
            bp = np.mean([u[x] for x in col_p])
            if not (np.isfinite(bt) and np.isfinite(bp)) or bp < 0:
                continue
            a_t.append(r["t_ann"]); b_t.append(bt); a_p.append(r["p_ann"]); b_p.append(bp)
            rows_.append((cid, r["t_ann"] - bt, r["p_ann"] - bp, r["p_ann"] / bp if bp > 0 else np.nan))
        a_t, b_t, a_p, b_p = map(np.array, (a_t, b_t, a_p, b_p))
        out = {
            "n": len(a_t),
            "temp_r": round(pearson(a_t, b_t), 4), "temp_bias_K": round(float((a_t - b_t).mean()), 3),
            "temp_mae_K": round(float(np.abs(a_t - b_t).mean()), 3),
            "precip_r": round(pearson(a_p, b_p), 4), "precip_bias_mm": round(float((a_p - b_p).mean()), 1),
            "precip_median_ratio": round(float(np.median(a_p / b_p)), 3),
            "worst_temp": [(c, round(d, 2)) for c, d, _, _ in sorted(rows_, key=lambda x: -abs(x[1]))[:6]],
            "worst_precip": [(c, round(d), round(q, 2)) for c, _, d, q in sorted(rows_, key=lambda x: -abs(x[2]))[:6]],
        }
        val[key] = out

    tids = [c.city_id for c in targets if c.city_id in rec]
    rids = [c.city_id for c in refs if c.city_id in rec]
    val["no_land_cell"] = no_land
    dw = np.array([rec[c]["t_wb2"].max() - rec[c]["tm"].max() for c in tids])
    dc = np.array([rec[c]["t_wb2"].min() - rec[c]["tm"].min() for c in tids])
    da = np.array([float((rec[c]["t_wb2"] * MEAN_MONTH_DAYS).sum() / MEAN_MONTH_DAYS.sum()) - rec[c]["t_ann"]
                   for c in tids])
    val["wb2_smoothed_minus_monthly"] = {
        "warmest_mean_K": round(float(dw.mean()), 3), "warmest_min_K": round(float(dw.min()), 3),
        "coldest_mean_K": round(float(dc.mean()), 3), "coldest_max_K": round(float(dc.max()), 3),
        "annual_mean_K": round(float(da.mean()), 4), "annual_maxabs_K": round(float(np.abs(da).max()), 4)}
    hbt = np.array([rec[c]["hb_t"] for c in tids])
    hbc = np.array([rec[c]["hb_c"] for c in tids])
    val["sampling_bias_2010_targets"] = {
        "t2m_mean_K": round(float(hbt.mean()), 3), "t2m_min_K": round(float(hbt.min()), 3),
        "t2m_max_K": round(float(hbt.max()), 3), "t2m_worst": sorted(((c, round(float(x), 2)) for c, x in zip(tids, hbt, strict=True)), key=lambda x: -abs(x[1]))[:5],
        "tcc_mean_pct": round(float(hbc.mean()), 2), "tcc_maxabs_pct": round(float(np.abs(hbc).max()), 2)}
    compare(tids, "ucdb_2010_targets", ["CL_B01_CUR_2010"], ["CL_B12_CUR_2010"])
    compare(tids, "ucdb_1990_2010_targets", ["CL_B01_CUR_1990", "CL_B01_CUR_2000", "CL_B01_CUR_2010"],
            ["CL_B12_CUR_1990", "CL_B12_CUR_2000", "CL_B12_CUR_2010"])
    compare(rids, "ucdb_1990_2010_reference", ["CL_B01_CUR_1990", "CL_B01_CUR_2000", "CL_B01_CUR_2010"],
            ["CL_B12_CUR_1990", "CL_B12_CUR_2000", "CL_B12_CUR_2010"])

    # ------------------------------------------------ validation 2: elevation and GHCN-M stations
    dz = np.array([rec[c]["elev"] - rec[c]["z_era5"] for c in tids])
    val["elev_targets"] = {
        "mean_dz_m": round(float(np.nanmean(dz)), 1), "mean_abs_dz_m": round(float(np.nanmean(np.abs(dz))), 1),
        "n_abs_dz_gt_100m": int(np.sum(np.abs(dz) > 100)), "n_abs_dz_gt_300m": int(np.sum(np.abs(dz) > 300)),
        "largest": sorted(((c, round(float(d))) for c, d in zip(tids, dz, strict=True)), key=lambda x: -abs(x[1]))[:12],
    }
    stns = ghcnm_normals()
    slat = np.array([s["lat"] for s in stns])
    slon = np.array([s["lon"] for s in stns])
    pairs = []
    for cid in rids:
        r = rec[cid]
        c = r["city"]
        near = np.flatnonzero((np.abs(slat - c.lat) < 1.0) & (np.abs(slon - c.lon) < 1.5))
        if not near.size:
            continue
        inside = shapely.contains_xy(c.geom, slon[near], slat[near])
        if not inside.any():
            continue
        ss = [stns[k] for k in near[inside]]
        t_st = float(np.mean([s["tann"] for s in ss]))
        z_st = float(np.mean([s["elev"] for s in ss]))
        pairs.append((cid, r["t_ann"], t_st, z_st, r["z_era5"], len(ss)))
    if pairs:
        e = np.array([p[1] - p[2] for p in pairs])
        dzs = np.array([p[3] - p[4] for p in pairs])
        ecorr = e + STD_LAPSE * dzs  # ERA5 lapse-adjusted to station height, minus station
        slope = float(np.polyfit(dzs, -e, 1)[0]) if len(pairs) > 5 else float("nan")
        big = np.abs(dzs) > 200
        val["ghcnm_reference"] = {
            "n_centres": len(pairs), "n_stations": int(sum(p[5] for p in pairs)),
            "raw_bias_K": round(float(e.mean()), 3), "raw_mae_K": round(float(np.abs(e).mean()), 3),
            "raw_rmse_K": round(float(np.sqrt((e ** 2).mean())), 3),
            "lapse_bias_K": round(float(ecorr.mean()), 3), "lapse_mae_K": round(float(np.abs(ecorr).mean()), 3),
            "lapse_rmse_K": round(float(np.sqrt((ecorr ** 2).mean())), 3),
            "fitted_lapse_K_per_km": round(-slope * 1000, 2),
            "n_abs_dz_gt_200m": int(big.sum()),
            "raw_mae_K_dz_gt_200m": round(float(np.abs(e[big]).mean()), 3) if big.any() else None,
            "lapse_mae_K_dz_gt_200m": round(float(np.abs(ecorr[big]).mean()), 3) if big.any() else None,
            "targets": [(p[0], round(p[1] - p[2], 2), round(p[1] - p[2] + STD_LAPSE * (p[3] - p[4]), 2),
                         round(p[3] - p[4]), p[5]) for p in pairs if p[0] in set(tids)],
        }

    # ------------------------------------------------ outputs
    inputs = [clim.record("clim", list(VARS.values()) + ["latitude", "longitude", "hour", "dayofyear"],
                          "WB2 ERA5 hourly climatology 1990-2019 (61-day triangular smoothing), streamed; only "
                          "cells for UCDB centres kept"),
              stat.record("static", list(STATIC_VARS.values()), "static fields land_sea_mask, geopotential_at_surface")]
    for u in LICENSE_URLS:
        fetch(u, RAW / ("LICENSE_" + u.split("/")[-2]))
        inputs.append(u)
    fetch(CDS_ERA5_CATALOGUE, RAW / "cds_reanalysis-era5-single-levels.json")
    inputs += [CDS_ERA5_CATALOGUE, GHCNM_URL]

    out = Interim(source_id=SOURCE_ID, inputs=inputs)
    out.notes += [
        ("ERA5 1990-2019, 0.25 deg. Temperature and dewpoint: monthly means of all 00/06/12/18 UTC fields "
         "(WB2 hourly ERA5 copy). Precipitation and cloud cover: WB2 ERA5 climatology (61-day triangular smoothing)."),
        ("City value = cos(lat)-weighted mean of ERA5 land cells (lsm>=0.5) whose centres lie in the UCDB polygon; "
        "else nearest land cell to the representative point (detail.cell_rule)."),
        ("Temperatures are at ERA5 model orography (no lapse-rate correction); detail.elev_diff_m = UCDB mean "
        "elevation - ERA5 orography."),
        ("Contains modified Copernicus Climate Change Service information (ERA5, 1990-2019). Neither the European "
        "Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it "
        "contains."),
        f"validation: {json.dumps(val, ensure_ascii=False)}",
    ]
    q = "observed"
    metrics = ["temp_warmest", "temp_coldest", "seasonal_range", "precip_annual", "cloud_cover_annual",
               "dewpoint_warmest"]
    for c in targets:
        if c.city_id not in rec:
            for m in metrics:
                out.miss(m, c.city_id, "no ERA5 land cell (land_sea_mask >= 0.5) in the polygon or within 2 deg")
            continue
        r = rec[c.city_id]
        s = r["sel"]
        base = {"cell_rule": s["rule"], "n_cells": s["n_cells"], "n_centres_in_polygon": s["n_centres_in_polygon"],
                **({"nearest_km": s["nearest_km"]} if s["nearest_km"] is not None else {}),
                "era5_orography_m": round(r["z_era5"]), "ucdb_elev_m": round(r["elev"]),
                "elev_diff_m": round(r["elev"] - r["z_era5"]),
                "lapse_equiv_K": round(-STD_LAPSE * (r["elev"] - r["z_era5"]), 2)}
        tm, dm, pm = r["tm"], r["dm"], r["pm"]
        out.put("temp_warmest", c.city_id, round(float(tm[r["iw"]]), 2), quality=q, year=PERIOD,
                detail={**base, "month": MONTHS[r["iw"]], "monthly_temp_c": [round(float(x), 2) for x in tm],
                        "annual_mean_c": round(r["t_ann"], 2), "diurnal_sampling_bias_K_2010": round(r["hb_t"], 3)})
        out.put("temp_coldest", c.city_id, round(float(tm[r["ic"]]), 2), quality=q, year=PERIOD,
                detail={"month": MONTHS[r["ic"]], "elev_diff_m": base["elev_diff_m"]})
        out.put("seasonal_range", c.city_id, round(float(tm[r["iw"]] - tm[r["ic"]]), 2), quality=q, year=PERIOD,
                detail={"warmest": MONTHS[r["iw"]], "coldest": MONTHS[r["ic"]]})
        out.put("precip_annual", c.city_id, round(r["p_ann"], 1), quality=q, year=PERIOD,
                detail={"n_cells": s["n_cells"], "cell_rule": s["rule"],
                        "monthly_precip_mm": [round(float(x), 1) for x in pm]})
        out.put("cloud_cover_annual", c.city_id, round(r["cloud"], 1), quality=q, year=PERIOD,
                detail={"n_cells": s["n_cells"], "diurnal_sampling_bias_pct_2010": round(r["hb_c"], 2)})
        out.put("dewpoint_warmest", c.city_id, round(float(dm[r["iw"]]), 2), quality=q, year=PERIOD,
                detail={"month": MONTHS[r["iw"]], "monthly_dewpoint_c": [round(float(x), 2) for x in dm],
                        "max_monthly_dewpoint_c": round(float(dm.max()), 2),
                        "max_dewpoint_month": MONTHS[int(np.argmax(dm))]})
    path = out.write()

    REFERENCE.mkdir(parents=True, exist_ok=True)
    with (REFERENCE / f"{SOURCE_ID}.csv").open("w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["city_id", "ucdb_id", "name_en", "temp_warmest", "temp_coldest", "seasonal_range",
                     "precip_annual", "cloud_cover_annual", "dewpoint_warmest", "temp_annual",
                     "cell_rule", "n_cells", "era5_orography_m", "ucdb_elev_m"])
        for c in refs:
            if c.city_id not in rec:
                wr.writerow([c.city_id, c.ucdb_id, c.name_en] + [""] * 7 + ["no_land_cell_within_2deg", 0, "", ""])
                continue
            r = rec[c.city_id]
            tm = r["tm"]
            wr.writerow([c.city_id, c.ucdb_id, c.name_en, round(float(tm[r["iw"]]), 2), round(float(tm[r["ic"]]), 2),
                         round(float(tm[r["iw"]] - tm[r["ic"]]), 2), round(r["p_ann"], 1), round(r["cloud"], 1),
                         round(float(r["dm"][r["iw"]]), 2), round(r["t_ann"], 2),
                         r["sel"]["rule"], r["sel"]["n_cells"], round(r["z_era5"]), round(r["elev"])])

    (RAW / "validation.json").write_text(json.dumps(val, indent=1, ensure_ascii=False))
    print(json.dumps(val, indent=1, ensure_ascii=False))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
