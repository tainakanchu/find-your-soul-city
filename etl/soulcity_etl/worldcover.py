"""ESA WorldCover 10 m 2021 v200 -> land-cover shares inside each GHS-UCDB urban-centre polygon.

Method (see etl/notes/esa-worldcover.md):
- The COG tiles (3x3 degree, EPSG:4326, 36000x36000 px, tile name = lower-left corner) are read over
  HTTPS (/vsicurl, windowed by polygon bbox, in row strips so memory stays bounded).
- Pixels whose centre lies inside the polygon are selected (rasterio.features.geometry_mask).
- Each pixel is weighted by its true spherical area (R^2 * dlon * (sin lat_top - sin lat_bottom)),
  i.e. proportional to cos(latitude).
- Value 0 (no data) and tiles absent from the product (open ocean) are "no data", not land cover.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from concurrent.futures import ThreadPoolExecutor
from functools import cache

import numpy as np
import rasterio
import shapely
from affine import Affine
from rasterio import features

from .cities import City, load_cities, reference_centres
from .common import CACHE, Interim, fetch, record_dataset

SOURCE_ID = "esa-worldcover"
YEAR = 2021
BASE = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021"
GRID_URL = f"{BASE}/esa_worldcover_grid.geojson"
PVR_URL = f"{BASE}/docs/WorldCover_PVR_V2.0.pdf"
PUM_URL = f"{BASE}/docs/WorldCover_PUM_V2.0.pdf"
DOI = "10.5281/zenodo.7254221"
ATTRIBUTION = (
    "© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by "
    "ESA WorldCover consortium"
)
LICENSE = "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)"
RAW = CACHE / "esa-worldcover"
COUNTS = RAW / "counts"

TILE_DEG = 3
TILE_PX = 36000
RES = TILE_DEG / TILE_PX  # 1/12000 degree = 8.333e-5
R_KM = 6371.0088  # mean Earth radius; spherical-zone pixel area

CLASSES = {
    10: "tree",
    20: "shrub",
    30: "grass",
    40: "crop",
    50: "built",
    60: "bare",
    70: "snow",
    80: "water",
    90: "wetland",
    95: "mangrove",
    100: "moss",
}
GREEN = (10, 20, 30, 90, 95)  # tree, shrubland, grassland, herbaceous wetland, mangroves
MIN_COVERAGE = 0.5  # share of polygon area with valid WorldCover pixels needed to report a value
STRIP = 3000  # rows per read strip


def tile_name(lat_ll: int, lon_ll: int) -> str:
    return f"{'N' if lat_ll >= 0 else 'S'}{abs(lat_ll):02d}{'E' if lon_ll >= 0 else 'W'}{abs(lon_ll):03d}"


def tile_url(name: str) -> str:
    return f"{BASE}/map/ESA_WorldCover_10m_2021_v200_{name}_Map.tif"


@cache
def grid_tiles() -> frozenset[str]:
    p = fetch(GRID_URL, RAW / "esa_worldcover_grid.geojson")
    return frozenset(f["properties"]["ll_tile"] for f in json.loads(p.read_text())["features"])


def _open(url: str):
    last: Exception | None = None
    for k in range(5):
        try:
            return rasterio.open("/vsicurl/" + url)
        except Exception as e:  # noqa: BLE001 - network flakiness
            last = e
            time.sleep(2 * (k + 1))
    raise RuntimeError(f"cannot open {url}: {last}")


def _read(ds, window):
    last: Exception | None = None
    for k in range(5):
        try:
            return ds.read(1, window=window)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (k + 1))
    raise RuntimeError(f"read failed: {last}")


def class_areas(geom: shapely.Geometry) -> dict:
    """Spherical-area (km2) of each WorldCover class inside `geom`, plus no-data area and tile list."""
    minx, miny, maxx, maxy = geom.bounds
    tiles_present = grid_tiles()
    area = np.zeros(256)  # km2 per raw pixel value (0 = nodata / missing tile)
    used: list[str] = []
    absent: list[str] = []
    la0 = math.floor(miny / TILE_DEG) * TILE_DEG
    lo0 = math.floor(minx / TILE_DEG) * TILE_DEG
    for lat_ll in range(la0, math.ceil(maxy / TILE_DEG) * TILE_DEG, TILE_DEG):
        for lon_ll in range(lo0, math.ceil(maxx / TILE_DEG) * TILE_DEG, TILE_DEG):
            box = shapely.box(lon_ll, lat_ll, lon_ll + TILE_DEG, lat_ll + TILE_DEG)
            if not geom.intersects(box):
                continue
            g = geom.intersection(box)
            if g.is_empty:
                continue
            name = tile_name(lat_ll, lon_ll)
            gx0, gy0, gx1, gy1 = g.bounds
            c0 = max(0, int(math.floor((gx0 - lon_ll) / RES)))
            c1 = min(TILE_PX, int(math.ceil((gx1 - lon_ll) / RES)))
            r0 = max(0, int(math.floor((lat_ll + TILE_DEG - gy1) / RES)))
            r1 = min(TILE_PX, int(math.ceil((lat_ll + TILE_DEG - gy0) / RES)))
            ds = None
            if name in tiles_present:
                ds = _open(tile_url(name))
                if (ds.width, ds.height) != (TILE_PX, TILE_PX) or abs(ds.transform.a - RES) > 1e-12:
                    raise RuntimeError(f"unexpected grid in tile {name}")
                used.append(name)
            else:
                absent.append(name)
            try:
                for rs in range(r0, r1, STRIP):
                    re_ = min(r1, rs + STRIP)
                    top = lat_ll + TILE_DEG - rs * RES
                    tr = Affine(RES, 0, lon_ll + c0 * RES, 0, -RES, top)
                    shape = (re_ - rs, c1 - c0)
                    inside = features.geometry_mask([g], out_shape=shape, transform=tr, invert=True)
                    if not inside.any():
                        continue
                    if ds is not None:
                        vals = _read(ds, ((rs, re_), (c0, c1)))
                    else:
                        vals = np.zeros(shape, dtype=np.uint8)
                    rows = np.arange(rs, re_)
                    lat_t = lat_ll + TILE_DEG - rows * RES
                    pix_km2 = R_KM**2 * np.radians(RES) * (np.sin(np.radians(lat_t)) - np.sin(np.radians(lat_t - RES)))
                    ridx = np.broadcast_to(np.arange(shape[0])[:, None], shape)[inside]
                    h = np.bincount(ridx * 256 + vals[inside].astype(np.int64), minlength=shape[0] * 256)
                    area += h.reshape(shape[0], 256).T @ pix_km2
            finally:
                if ds is not None:
                    ds.close()
    return {"area_km2": area, "tiles": used, "tiles_absent": absent}


def summarise(city: City, res: dict) -> dict:
    a = res["area_km2"]
    nodata = float(a[0])
    other = float(a[[i for i in range(1, 256) if i not in CLASSES]].sum())
    cls = {k: float(a[k]) for k in CLASSES}
    valid = sum(cls.values())
    total = valid + nodata + other
    water = cls[80]
    land = valid - water
    out = {
        "polygon_area_pixels_km2": total,
        "valid_km2": valid,
        "nodata_km2": nodata,
        "unknown_value_km2": other,
        "coverage": valid / total if total else 0.0,
        "water_km2": water,
        "land_km2": land,
        "classes_km2": cls,
        "tiles": res["tiles"],
        "tiles_absent": res["tiles_absent"],
        "ucdb_area_km2": city.area_km2,
    }
    if land > 0:
        out["land_share_pct"] = {CLASSES[k]: 100 * cls[k] / land for k in CLASSES if k != 80}
        out["tree_share"] = 100 * cls[10] / land
        out["green_share"] = 100 * sum(cls[k] for k in GREEN) / land
        out["green_incl_crop_share"] = 100 * (sum(cls[k] for k in GREEN) + cls[40]) / land
        out["built_share"] = 100 * cls[50] / land
    if valid > 0:
        out["water_share"] = 100 * water / valid
    return out


def city_summary(city: City) -> dict:
    COUNTS.mkdir(parents=True, exist_ok=True)
    cache_f = COUNTS / f"uc{city.ucdb_id}.json"
    if cache_f.exists():
        return json.loads(cache_f.read_text())
    s = summarise(city, class_areas(city.geom))
    cache_f.write_text(json.dumps(s))
    return s


def run(cities: tuple[City, ...], workers: int = 4) -> dict[str, dict]:
    def one(c: City):
        t = time.time()
        s = city_summary(c)
        print(
            f"  {c.city_id:16} {c.name_en:18} cov={s['coverage']:.3f} tree={s.get('tree_share', float('nan')):5.1f} "
            f"green={s.get('green_share', float('nan')):5.1f} built={s.get('built_share', float('nan')):5.1f} "
            f"water={s.get('water_share', float('nan')):5.1f} tiles={len(s['tiles'])} ({time.time() - t:.0f}s)",
            flush=True,
        )
        return c.city_id, s

    with ThreadPoolExecutor(workers) as ex:
        return dict(ex.map(one, cities))


def build_interim(cities: tuple[City, ...], sums: dict[str, dict]) -> Interim:
    it = Interim(SOURCE_ID)
    for u in (GRID_URL, PVR_URL, PUM_URL):
        fetch(u, RAW / "docs" / u.rsplit("/", 1)[1] if u != GRID_URL else RAW / "esa_worldcover_grid.geojson")
        it.inputs.append(u)
    all_tiles = sorted({t for s in sums.values() for t in s["tiles"]})
    for t in all_tiles:
        record_dataset(
            tile_url(t),
            source="ESA WorldCover 10m 2021 v200 (COG tile, read windowed via /vsicurl)",
            version="v200",
            doi=DOI,
            license=LICENSE,
            attribution=ATTRIBUTION,
            tile=t,
        )
        it.inputs.append(tile_url(t))
    it.notes += [
        f"ESA WorldCover 10 m 2021 v200, DOI {DOI}. License {LICENSE}. Attribution: {ATTRIBUTION}",
        "Shares are spherical-area weighted (cos latitude) over pixels whose centre lies in the GHS-UCDB polygon. "
        "tree/green/built shares use land (valid minus class 80 water) as denominator; water_share uses all valid pixels.",
        "green_share = classes 10,20,30,90,95; cropland (40) excluded (see detail.green_incl_crop_share).",
        "Global overall accuracy of v200 is 76.7+-0.5% (PVR V2.0); built-up user's accuracy 65.9%, producer's 73.2%.",
    ]
    for c in cities:
        s = sums[c.city_id]
        detail_common = {
            "coverage": round(s["coverage"], 4),
            "land_km2": round(s["land_km2"], 2),
            "water_km2": round(s["water_km2"], 2),
            "polygon_area_pixels_km2": round(s["polygon_area_pixels_km2"], 2),
            "ucdb_area_km2": round(s["ucdb_area_km2"], 2),
            "tiles": s["tiles"],
            "tiles_absent": s["tiles_absent"],
            "nodata_km2": round(s["nodata_km2"], 3),
        }
        if s["coverage"] < MIN_COVERAGE or "tree_share" not in s:
            for m in ("tree_share", "green_share", "water_share", "built_share"):
                it.miss(
                    m,
                    c.city_id,
                    f"WorldCover valid-pixel coverage of polygon only {s['coverage']:.2f} "
                    f"(< {MIN_COVERAGE}); tiles absent: {s['tiles_absent']}",
                )
            continue
        det = {
            **detail_common,
            "land_share_pct": {k: round(v, 3) for k, v in s["land_share_pct"].items()},
            "water_pct_of_valid_area": round(s["water_share"], 3),
            "green_incl_crop_share": round(s["green_incl_crop_share"], 3),
        }
        for m in ("tree_share", "green_share", "water_share", "built_share"):
            it.put(m, c.city_id, s[m], quality="observed", year=YEAR, detail=det)
    return it


def _rank(x: np.ndarray) -> np.ndarray:
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    r[order] = np.arange(len(x))
    for v in np.unique(x):  # average ranks for ties
        m = x == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def spearman(a, b) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    return float(np.corrcoef(_rank(a[ok]), _rank(b[ok]))[0, 1])


def validate(cities: tuple[City, ...], sums: dict[str, dict]) -> dict:
    """Compare with GHS-UCDB LULC (Copernicus CGLS-LC100, 2019, ha) and GREENNESS (Landsat NDVI, 2020) themes."""
    import pyogrio

    from .cities import ucdb_gpkg

    gp = ucdb_gpkg()
    ids = [c.ucdb_id for c in cities]

    def table(layer: str, cols: list[str]) -> dict[str, np.ndarray]:
        _m, _f, _g, fl = pyogrio.raw.read(gp, layer=layer, columns=["ID_UC_G0", *cols], read_geometry=False)
        idx = {int(v): i for i, v in enumerate(fl[0])}
        return {c: np.array([float(fl[1 + j][idx[u]]) for u in ids]) for j, c in enumerate(cols)}

    forest = ["111", "112", "113", "114", "115", "116", "121", "122", "123", "124", "125", "126"]
    lu_cols = [f"LU_HEC_{k}_2019" for k in ["020", "030", "040", "050", "060", "070", "080", "090", "100", *forest]]
    lu = table("GHSL_UCDB_THEME_LULC_GLOBE_R2024A", lu_cols)
    gr_cols = ["GR_AVG_GRN_2020", "GR_SHB_GRN_2020", "GR_SHB_HGR_2020", "GR_CTH_AVG_2020"]
    gr = table("GHSL_UCDB_THEME_GREENNESS_GLOBE_R2024A", gr_cols)
    tot = sum(lu[c] for c in lu_cols)
    water = lu["LU_HEC_080_2019"]
    land = tot - water
    tree_c = sum(lu[f"LU_HEC_{k}_2019"] for k in forest)
    cg = {
        "tree_share": 100 * tree_c / land,
        "green_share": 100 * (tree_c + lu["LU_HEC_020_2019"] + lu["LU_HEC_030_2019"] + lu["LU_HEC_090_2019"]) / land,
        "built_share": 100 * lu["LU_HEC_050_2019"] / land,
        "water_share": 100 * water / tot,
    }
    wc = {m: np.array([sums[c.city_id].get(m, np.nan) for c in cities]) for m in cg}
    res: dict = {
        "lulc_total_vs_ucdb_area_ratio_median": float(np.median(tot / 100 / np.array([c.area_km2 for c in cities])))
    }
    res["vs_cgls"] = {
        m: {
            "spearman": spearman(wc[m], cg[m]),
            "pearson": float(np.corrcoef(wc[m], cg[m])[0, 1]),
            "mean_wc": float(wc[m].mean()),
            "mean_cgls": float(cg[m].mean()),
        }
        for m in cg
    }
    res["vs_greenness"] = {}
    for gname, gv in gr.items():
        res["vs_greenness"][gname] = {m: spearman(wc[m], gv) for m in ("tree_share", "green_share", "built_share")}
    # outliers: largest rank disagreement between WC and CGLS green_share
    d = _rank(wc["green_share"]) - _rank(cg["green_share"])
    res["green_outliers"] = [
        {
            "city": cities[i].name_en,
            "wc": float(wc["green_share"][i]),
            "cgls": float(cg["green_share"][i]),
            "rank_diff": float(d[i]),
        }
        for i in np.argsort(-np.abs(d))[:10]
    ]
    dt_ = _rank(wc["tree_share"]) - _rank(cg["tree_share"])
    res["tree_outliers"] = [
        {
            "city": cities[i].name_en,
            "wc": float(wc["tree_share"][i]),
            "cgls": float(cg["tree_share"][i]),
            "rank_diff": float(dt_[i]),
        }
        for i in np.argsort(-np.abs(dt_))[:10]
    ]
    res["table"] = [
        {
            "city": c.name_en,
            **{f"wc_{m}": float(wc[m][i]) for m in cg},
            **{f"cgls_{m}": float(cg[m][i]) for m in cg},
            "GR_AVG_GRN_2020": float(gr["GR_AVG_GRN_2020"][i]),
            "GR_SHB_GRN_2020": float(gr["GR_SHB_GRN_2020"][i]),
        }
        for i, c in enumerate(cities)
    ]
    rk = sorted(res["table"], key=lambda r: r["wc_green_share"])
    res["lowest_green"] = [(r["city"], round(r["wc_green_share"], 1)) for r in rk[:10]]
    res["highest_green"] = [(r["city"], round(r["wc_green_share"], 1)) for r in rk[-10:]]
    rk = sorted(res["table"], key=lambda r: r["wc_water_share"])
    res["highest_water"] = [(r["city"], round(r["wc_water_share"], 1)) for r in rk[-10:]]
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", action="store_true", help="also compute all >=1M centres (cached, slow)")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    cities = load_cities()
    print(f"WorldCover v200: {len(cities)} target cities")
    sums = run(cities, args.workers)
    it = build_interim(cities, sums)
    path = it.write()
    n = len(cities)
    print(f"wrote {path}")
    for m, v in it.values.items():
        print(f"  {m}: {len(v)}/{n} values, missing {n - len(v)}")
    v = validate(cities, sums)
    (RAW / "validation.json").write_text(json.dumps(v, indent=1, ensure_ascii=False))
    print(json.dumps({k: v[k] for k in v if k != "table"}, indent=1, ensure_ascii=False))
    if args.reference:
        ref = tuple(c for c in reference_centres() if c.city_id.startswith("uc-"))
        print(f"reference: {len(ref)} extra centres")
        rs = run(ref, args.workers)
        import csv

        from .common import REFERENCE

        REFERENCE.mkdir(parents=True, exist_ok=True)
        allr = {**sums, **rs}
        with (REFERENCE / f"{SOURCE_ID}.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["city_id", "ucdb_id", "coverage", "tree_share", "green_share", "water_share", "built_share"])
            by_id = {c.city_id: c for c in reference_centres()}
            for cid, s in sorted(allr.items()):
                w.writerow(
                    [cid, by_id[cid].ucdb_id, round(s["coverage"], 4)]
                    + [
                        round(s[m], 3) if m in s and s["coverage"] >= MIN_COVERAGE else ""
                        for m in ("tree_share", "green_share", "water_share", "built_share")
                    ]
                )


if __name__ == "__main__":
    main()
