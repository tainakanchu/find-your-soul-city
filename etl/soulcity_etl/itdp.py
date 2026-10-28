"""ITDP Atlas of Sustainable City Transport -> "people near" accessibility indicators per urban centre.

Source: ITDP publishes the full data behind atlas.itdp.org as a GitHub release of its open-source
frontend repo (github.com/ITDP/atlas, release `update_2024`, asset `data_final` split into a 5-part
zip: data_final.z01..z04 + data_final.zip, ~4.2 GB). We do NOT download the whole archive:
- the zip64 central directory (end of z04 + data_final.zip) is read once to index the ~311k members;
- each needed member (`data_final/ghsl_<ID_UC_G0:05d>/indicators_<id>.rds`) is fetched with an
  HTTP Range request, inflated, and verified against the CRC-32 and size in the central directory.
Each per-city .rds is an R `sf` data.frame: one row per analysis area; the row with admin_level "0"
is the urban agglomeration itself (polygon + indicator values). Atlas ids (`hdc`) are GHS-UCDB R2024A
ID_UC_G0 (zero-padded), so the crosswalk is by id and then verified geometrically (IoU, area ratio).
The .rds files are parsed with the pure-python `rdata` parser (no R needed); helpers below turn the
parsed R objects into columns and shapely geometries.

See etl/notes/itdp-atlas.md for definitions, license (ODbL 1.0) and caveats.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import zlib
from concurrent.futures import ThreadPoolExecutor
from functools import cache
from pathlib import Path
from typing import Any

import numpy as np
import requests
import shapely
from pyproj import Transformer

from .cities import City, load_cities, reference_centres
from .common import CACHE, REFERENCE, Interim, fetch, record_dataset, sha256_file

SOURCE_ID = "itdp-atlas"
RELEASE = "update_2024"
REPO_URL = "https://github.com/ITDP/atlas"
BASE = f"{REPO_URL}/releases/download/{RELEASE}/data_final"
SEGMENTS = ["z01", "z02", "z03", "z04", "zip"]  # disk 0..4 of the split archive
RAW = CACHE / SOURCE_ID
MEMBERS = RAW / RELEASE / "members"
LICENSE = "ODbL 1.0 (database) + DbCL 1.0 (contents) - https://atlas.itdp.org/about/about_data.html"
ATTRIBUTION = (
    "Atlas of Sustainable City Transport, ITDP (Reich & Braga 2024), atlas.itdp.org, data release "
    "update_2024, ODbL 1.0; contains information from OpenStreetMap © OpenStreetMap contributors (ODbL), "
    "GHSL (European Commission JRC, CC BY 4.0), Mobility Database GTFS feeds, Transit Explorer"
)
ATLAS_MIN_POP = 500_000  # "We include all urban agglomerations with a population above 500,000 people."
MIN_STATIONS_PER_KM = 0.2  # rapid-transit station density screen (stations per line-km)
IOU_MIN = 0.5  # boundary acceptance threshold (Atlas agglomeration polygon vs our UCDB polygon)
MOLL = Transformer.from_crs("EPSG:4326", "ESRI:54009", always_xy=True)

# metric key -> (Atlas column prefix, year, scale, unit, description)
# Atlas stores shares as fractions 0..1; we publish percent.
METRICS: dict[str, tuple[str, int, float, str, str]] = {
    "walk_services": ("walk_pns", 2024, 100, "%", ("People Near Services: pop. share within 1 km walk of both "
                      "healthcare and education")),
    "walk_healthcare": ("walk_pnspnh", 2024, 100, "%", "People Near Healthcare (1 km walk)"),
    "walk_education": ("walk_pnspne", 2024, 100, "%", "People Near Education (1 km walk)"),
    "bike_protected": ("bike_pnpb", 2024, 100, "%", "People Near Protected Bikeways (300 m walk)"),
    "bike_any": ("bike_pnpbpnab", 2024, 100, "%", "People Near All Bikeways incl. painted lanes (300 m walk)"),
    "rapid_transit": ("transit_pnrt", 2024, 100, "%", "People Near Rapid Transport (BRT/LRT/metro, 1 km walk)"),
    "frequent_transit": ("transit_pnft", 2024, 100, "%", ("People Near Frequent Transport (<=10 min headway "
                         "stop, 500 m walk; GTFS)")),
    "sustainable_transport": ("transit_pnst", 2024, 100, "%", ("People Near Sustainable Transport: protected "
                              "bikeway AND (frequent OR rapid transport)")),
    "car_free_places": ("walk_pncf", 2024, 100, "%", "People Near Car-Free Places (100 m)"),
    "safe_from_highways": ("walk_pnnhighways", 2024, 100, "%", "People >= 500 m from a grade-separated highway"),
    "block_density": ("city_blockdensity", 2024, 1, "blocks/km2", "Walkable blocks per km2"),
    "weighted_density": ("city_popdensity", 2024, 1, "people/km2", "Population-weighted density (1 km cells)"),
    "rapid_transit_km_per_mpop": ("transit_pnrtrtrall", 2024, 1, "km per million people",
                                  "Rapid Transit to Resident Ratio (all modes)"),
}
POP_COL = "city_popdensitytotal_2025"  # Atlas GHS-POP sum in its polygon, compared with UCDB GC_POP_TOT_2025


# ---------------------------------------------------------------- split-zip access over HTTP Range


def _seg_url(disk: int) -> str:
    return f"{BASE}.{SEGMENTS[disk]}"


@cache
def _seg_sizes() -> tuple[int, ...]:
    sizes = []
    for d in range(len(SEGMENTS)):
        r = requests.head(_seg_url(d), allow_redirects=True, timeout=60)
        r.raise_for_status()
        sizes.append(int(r.headers["Content-Length"]))
    return tuple(sizes)


def _range(disk: int, off: int, n: int) -> bytes:
    """Read n bytes starting at (disk, off), continuing into following segments if needed."""
    sizes = _seg_sizes()
    out = bytearray()
    while n > 0:
        k = min(n, sizes[disk] - off)
        for attempt in range(5):
            try:
                r = requests.get(_seg_url(disk), headers={"Range": f"bytes={off}-{off + k - 1}"}, timeout=300)
                if r.status_code != 206 or len(r.content) != k:
                    raise requests.RequestException(f"range {disk}:{off}+{k} -> {r.status_code} {len(r.content)}")
                break
            except requests.RequestException:
                if attempt == 4:
                    raise
        out += r.content
        n -= k
        disk, off = disk + 1, 0
    return bytes(out)


@cache
def _central_directory() -> dict[str, tuple[int, int, int, int, int, int]]:
    """name -> (method, compressed size, uncompressed size, crc32, disk, local header offset)."""
    last = fetch(f"{BASE}.zip", RAW / RELEASE / "data_final.zip", timeout=600)
    tail = last.read_bytes()
    j = tail.rfind(b"PK\x06\x06")  # zip64 end of central directory record
    if j < 0:
        raise RuntimeError("zip64 EOCD not found")
    (_sig, _sz, _vm, _vn, _disk, cd_disk, _n_disk, n_total, cd_size, cd_off) = struct.unpack(
        "<IQHHIIQQQQ", tail[j:j + 56])
    head_cache = RAW / RELEASE / f"cd_{SEGMENTS[cd_disk]}_{cd_off}.bin"
    if cd_disk == len(SEGMENTS) - 1:
        cd = tail[cd_off:cd_off + cd_size]
    else:
        if not head_cache.exists():
            head_cache.write_bytes(_range(cd_disk, cd_off, _seg_sizes()[cd_disk] - cd_off))
        cd = (head_cache.read_bytes() + tail)[:cd_size]
    ents: dict[str, tuple[int, int, int, int, int, int]] = {}
    p = 0
    while p < len(cd):
        (sig, _vm, _vn, _fl, meth, _t, _d, crc, cs, us, nl, el, cl, disk, _ia, _ea, off) = struct.unpack(
            "<IHHHHHHIIIHHHHHII", cd[p:p + 46])
        if sig != 0x02014B50:
            raise RuntimeError(f"bad central directory signature at {p}")
        name = cd[p + 46:p + 46 + nl].decode("utf-8", "replace")
        ex = cd[p + 46 + nl:p + 46 + nl + el]
        q = 0
        while q < len(ex):
            hid, sz = struct.unpack("<HH", ex[q:q + 4])
            if hid == 1:  # zip64 extra: fields present only when the 32-bit value is saturated
                dat, k = ex[q + 4:q + 4 + sz], 0
                if us == 0xFFFFFFFF:
                    us = struct.unpack("<Q", dat[k:k + 8])[0]
                    k += 8
                if cs == 0xFFFFFFFF:
                    cs = struct.unpack("<Q", dat[k:k + 8])[0]
                    k += 8
                if off == 0xFFFFFFFF:
                    off = struct.unpack("<Q", dat[k:k + 8])[0]
                    k += 8
                if disk == 0xFFFF:
                    disk = struct.unpack("<I", dat[k:k + 4])[0]
            q += 4 + sz
        ents[name] = (meth, cs, us, crc, disk, off)
        p += 46 + nl + el + cl
    if len(ents) != n_total:
        raise RuntimeError(f"central directory has {len(ents)} entries, EOCD says {n_total}")
    return ents


def member(name: str) -> Path:
    """Extract one archive member to the cache (Range read + inflate + CRC check)."""
    dest = MEMBERS / name
    if dest.exists():
        return dest
    meth, cs, us, crc, disk, off = _central_directory()[name]
    sizes = _seg_sizes()
    nb = name.encode()
    # In this archive the recorded local-header offsets drift by a few bytes in parts of segment z01
    # (observed: -47). Locate the local header whose file name matches, nearest to the recorded offset.
    pos = None
    for win in (512, 8192, 1 << 20):
        s = max(0, off - win)
        b = _range(disk, s, min(2 * win + 30 + len(nb), sum(sizes[disk:]) - s))
        hits = [m.start() for m in re.finditer(re.escape(b"PK\x03\x04"), b)
                if b[m.start() + 30:m.start() + 30 + len(nb)] == nb]
        if hits:
            i = min(hits, key=lambda h: abs(s + h - off))
            pos, h = s + i, b[i:i + 30]
            break
    if pos is None:
        raise RuntimeError(f"{name}: local header not found near offset {off}")
    nl, el = struct.unpack("<HH", h[26:30])
    g = sum(sizes[:disk]) + pos + 30 + nl + el
    d2 = 0
    while g >= sizes[d2]:
        g -= sizes[d2]
        d2 += 1
    data = _range(d2, g, cs)
    raw = zlib.decompress(data, -15) if meth == 8 else data
    if len(raw) != us or zlib.crc32(raw) != crc:
        raise RuntimeError(f"{name}: size/CRC mismatch")
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".part")
    tmp.write_bytes(raw)
    tmp.replace(dest)
    return dest


# ---------------------------------------------------------------- minimal RDS (sf data.frame) reader


def _rconv(o: Any) -> Any:
    import rdata

    T = rdata.parser.RObjectType
    t = o.info.type
    if t == T.REF:
        return _rconv(o.referenced_object)
    if t == T.NILVALUE:
        return None
    if t in (T.REAL, T.INT, T.LGL):
        v: Any = np.asarray(o.value)
    elif t == T.STR:
        v = [x.value.decode() if x.value is not None else None for x in o.value]
    elif t == T.VEC:
        v = [_rconv(x) for x in o.value]
    elif t == T.CHAR:
        return o.value.decode() if o.value is not None else None
    elif t == T.SYM:
        return _rconv(o.value)
    else:
        v = f"<{t.name}>"
    if o.info.attributes:
        attrs = {}
        a = o.attributes
        while a is not None and a.info.type == T.LIST:
            tag = a.tag
            if tag is not None and tag.info.type == T.REF:
                tag = tag.referenced_object
            key = _rconv(tag) if tag is not None else None
            attrs[key] = _rconv(a.value[0])
            a = a.value[1]
        return {"v": v, "a": attrs}
    return v


def read_sf(path: Path) -> tuple[dict[str, Any], list[shapely.Geometry]]:
    """Columns (name -> list/array) and the geometry column of an sf data.frame saved as .rds."""
    import rdata

    obj = _rconv(rdata.parser.parse_file(path).object)
    names = obj["a"]["names"]
    cols = dict(zip(names, obj["v"], strict=True))
    gcol = obj["a"].get("sf_column", ["geom"])[0]
    sfc = cols.pop(gcol)
    geoms = [_sfg(g) for g in sfc["v"]]
    out = {k: (v["v"] if isinstance(v, dict) else v) for k, v in cols.items()}
    return out, geoms


def _ring(m: dict) -> np.ndarray:
    n, k = (int(x) for x in m["a"]["dim"])
    return np.asarray(m["v"], dtype=float).reshape((k, n)).T[:, :2]  # R matrices are column-major


def _sfg(g: dict) -> shapely.Geometry:
    kind = g["a"]["class"][1]
    if kind == "MULTIPOLYGON":
        polys = [shapely.Polygon(_ring(p[0]), [_ring(h) for h in p[1:]]) for p in
                 (pp["v"] if isinstance(pp, dict) else pp for pp in g["v"]) if p]
        return shapely.MultiPolygon(polys)
    if kind == "POLYGON":
        return shapely.Polygon(_ring(g["v"][0]), [_ring(h) for h in g["v"][1:]])
    raise ValueError(f"unsupported sfg {kind}")


# ---------------------------------------------------------------- per-city extraction


def _moll(g: shapely.Geometry) -> shapely.Geometry:
    g = shapely.make_valid(g)
    return shapely.make_valid(shapely.transform(g, lambda xy: np.column_stack(MOLL.transform(xy[:, 0], xy[:, 1]))))


def member_name(ucdb_id: int) -> str:
    return f"data_final/ghsl_{ucdb_id:05d}/indicators_{ucdb_id:05d}.rds"


def city_record(c: City) -> dict[str, Any]:
    """Atlas agglomeration row for one UCDB centre + boundary diagnostics (or a 'missing' reason)."""
    name = member_name(c.ucdb_id)
    if name not in _central_directory():
        why = f"not in Atlas release {RELEASE} (no {name})"
        if c.pop_2025 < ATLAS_MIN_POP:
            why += (f"; UCDB 2025 population {c.pop_2025:,.0f} is below the Atlas inclusion threshold of "
                    f"{ATLAS_MIN_POP:,} (methodology, General Topic 1a)")
        return {"missing": why}
    cols, geoms = read_sf(member(name))
    lvl = [str(x) for x in cols["admin_level"]]
    if lvl.count("0") != 1:
        return {"missing": f"Atlas file has {lvl.count('0')} agglomeration rows (admin_level 0)"}
    i = lvl.index("0")
    hdc = cols["hdc"][i]
    if int(hdc) != c.ucdb_id:
        return {"missing": f"Atlas hdc {hdc} != ucdb_id {c.ucdb_id}"}
    a, b = _moll(geoms[i]), _moll(c.geom)
    inter = shapely.area(shapely.intersection(a, b))
    union = shapely.area(shapely.union(a, b))
    rec: dict[str, Any] = {
        "atlas_name": cols["name"][i],
        "atlas_country": cols["country"][i],
        "hdc": hdc,
        "iou": round(float(inter / union), 4),
        "area_ratio": round(float(shapely.area(a) / shapely.area(b)), 4),  # Atlas / UCDB
        "atlas_area_km2": round(float(shapely.area(a)) / 1e6, 1),
        "ucdb_area_km2": round(float(shapely.area(b)) / 1e6, 1),
        "n_analysis_areas": len(lvl),
        "values": {},
    }
    pop = cols.get(POP_COL)
    if pop is not None and np.isfinite(pop[i]):
        rec["atlas_pop_2025"] = float(pop[i])
        rec["pop_ratio_vs_ucdb"] = round(float(pop[i]) / c.pop_2025, 4)
    for key, (prefix, year, _scale, _u, _d) in METRICS.items():
        col = cols.get(f"{prefix}_{year}")
        rec["values"][key] = None if col is None else (float(col[i]) if np.isfinite(col[i]) else None)
        if col is None:
            rec.setdefault("absent_columns", []).append(f"{prefix}_{year}")
    # inputs of the plausibility screen (see screen()): frequent stops found, rapid-transit km and stations
    pts = cols.get("transit_pnftpoints_2024")
    rec["frequent_stops"] = float(pts[i]) if pts is not None and np.isfinite(pts[i]) else None
    km = cols.get("transit_pnrtkmall_2024")
    rec["rt_km"] = float(km[i]) if km is not None and np.isfinite(km[i]) else None
    rec["members"] = [name]
    n_st = 0
    for mode in ("mrt", "lrt", "brt"):
        sname = f"data_final/ghsl_{c.ucdb_id:05d}/overlays/temp/{mode}_stations_ll_{c.ucdb_id:05d}_2024.geojson"
        if sname not in _central_directory():
            n_st = None
            break
        feats = json.loads(member(sname).read_text())["features"]
        n_st += sum(int(shapely.get_num_geometries(shapely.from_geojson(json.dumps(f["geometry"]))))
                    for f in feats if f.get("geometry"))
        rec["members"].append(sname)
    rec["rt_stations"] = n_st
    return rec


def screen(rec: dict[str, Any]) -> dict[str, str]:
    """Metrics whose published Atlas value fails an internal-consistency check -> reason.

    1. frequent_transit: ITDP found zero frequent stops (transit_pnftpoints_2024 == 0) although a GTFS feed was
       processed (value 0, not NA). For the large centres in our set that signals a GTFS ingestion/coverage failure
       (e.g. Tokyo, Zurich, Amsterdam = 0 %), not an absence of 10-minute service.
    2. rapid_transit (+ km ratio): the Transit Explorer extract has rapid-transit lines but fewer than
       MIN_STATIONS_PER_KM stations per line-km (median of the 86 targets ~0.6/km). People Near Rapid Transport is
       computed from station isochrones, so missing stations make it collapse (London 508 km of metro, 3 stations,
       0.5 %).
    3. sustainable_transport needs both frequent and rapid transport; if either is NA or screened out it is an
       underestimate.
    """
    bad: dict[str, str] = {}
    v = rec["values"]
    if v.get("frequent_transit") == 0 and rec.get("frequent_stops") == 0:
        bad["frequent_transit"] = ("Atlas reports 0 % with 0 frequent stops found (transit_pnftpoints_2024 = 0): "
                                   "treated as a GTFS ingestion/coverage failure, not a measurement")
    km, st = rec.get("rt_km"), rec.get("rt_stations")
    if km and st is not None and st / km < MIN_STATIONS_PER_KM:
        why = (f"Atlas rapid-transit station data incomplete: {st} stations on {km:.0f} line-km "
               f"({st / km:.2f}/km < {MIN_STATIONS_PER_KM}/km); People Near Rapid Transport is computed from "
               f"stations, so the published {100 * (v.get('rapid_transit') or 0):.1f} % is not credible")
        bad["rapid_transit"] = why
    for dep in ("frequent_transit", "rapid_transit"):
        if dep in bad or v.get(dep) is None:
            bad.setdefault("sustainable_transport", f"component {dep} is NA or failed the screen "
                                                    f"({bad.get(dep, 'NA in Atlas')}); value would be an underestimate")
    return bad


def collect(cities: tuple[City, ...], workers: int = 6) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(workers) as ex:
        for c, rec in zip(cities, ex.map(city_record, cities), strict=True):
            out[c.city_id] = rec
    return out


def _record_inputs(names: list[str]) -> str:
    key = f"{REPO_URL}/releases/tag/{RELEASE}#data_final"
    ents = _central_directory()
    record_dataset(
        key,
        kind="GitHub release asset (5-part split zip), members read by HTTP Range and CRC-checked",
        segments={f"data_final.{s}": n for s, n in zip(SEGMENTS, _seg_sizes(), strict=True)},
        n_members_in_archive=len(ents),
        members={n: {"crc32": f"{ents[n][3]:08x}", "bytes": ents[n][2],
                     "sha256": sha256_file(MEMBERS / n)} for n in sorted(names) if (MEMBERS / n).exists()},
        license=LICENSE,
    )
    return key


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", action="store_true", help="also write data/reference/itdp-atlas.csv (524 centres)")
    args = ap.parse_args()

    cities = load_cities()
    recs = collect(cities)
    names = [m for r in recs.values() for m in r.get("members", [])]

    out = Interim(source_id=SOURCE_ID)
    out.notes += [
        (f"ITDP Atlas of Sustainable City Transport, GitHub release {RELEASE} of {REPO_URL} (asset published "
        "2025-01-10); indicators for the 2024 data year computed by ITDP from OpenStreetMap, GHS-POP R2023A, "
        "Mobility Database GTFS and Transit Explorer. Values are ITDP's, copied (fractions x100 -> %), not recomputed."),
        ("Atlas agglomerations are GHS-UCDB R2024A urban centres (hdc == ID_UC_G0); each match is verified "
        f"geometrically, accepted only if IoU >= {IOU_MIN} (see detail.iou / detail.area_ratio)."),
        f"License: {LICENSE}. Attribution: {ATTRIBUTION}.",
        ("quality=observed means 'computed indicator taken as published by ITDP' (method: network isochrones on "
        "OSM + GHSL population); OSM completeness varies by country - see etl/notes/itdp-atlas.md."),
    ]
    for c in cities:
        rec = recs[c.city_id]
        if "missing" in rec:
            for key in METRICS:
                out.miss(key, c.city_id, rec["missing"])
            continue
        geo = {k: rec[k] for k in ("hdc", "atlas_name", "iou", "area_ratio", "atlas_area_km2", "ucdb_area_km2")}
        if "pop_ratio_vs_ucdb" in rec:
            geo["atlas_pop_2025_vs_ucdb"] = rec["pop_ratio_vs_ucdb"]
        if rec["iou"] < IOU_MIN:
            for key in METRICS:
                out.miss(key, c.city_id, f"Atlas boundary mismatch: IoU {rec['iou']} < {IOU_MIN} "
                                         f"(area ratio {rec['area_ratio']})")
            continue
        bad = screen(rec)
        for key, (prefix, year, scale, unit, _d) in METRICS.items():
            v = rec["values"][key]
            if key in bad and v is not None:
                out.miss(key, c.city_id, bad[key])
                continue
            if v is None:
                why = (f"Atlas value is NA for {prefix}_{year}"
                       + (" (ITDP computes it only from GTFS feeds listed in the Mobility Database; NA = no "
                          "usable feed covering the agglomeration)" if prefix == "transit_pnft" else ""))
                out.miss(key, c.city_id, why)
                continue
            extra: dict[str, Any] = {}
            if key in ("rapid_transit", "rapid_transit_km_per_mpop"):
                extra = {"rt_line_km": rec["rt_km"], "rt_stations": rec["rt_stations"]}
            if key == "frequent_transit":
                extra = {"frequent_stops": rec["frequent_stops"]}
            out.put(key, c.city_id, v * scale, quality="observed", year=year,
                    detail={**geo, "atlas_column": f"{prefix}_{year}", "unit": unit, **extra})
    out.inputs = [_record_inputs(names), f"{BASE}.zip"]
    p = out.write()
    n_ok = sum(1 for r in recs.values() if "missing" not in r and r["iou"] >= IOU_MIN)
    print(f"wrote {p}: {n_ok}/{len(cities)} cities matched")
    diag = RAW / "boundary_match.json"
    diag.write_text(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "values"} for k, v in recs.items()},
                               indent=1, ensure_ascii=False))
    print(f"boundary diagnostics: {diag}")

    if args.reference:
        refs = reference_centres()
        rrecs = collect(refs)
        REFERENCE.mkdir(parents=True, exist_ok=True)
        lines = ["city_id,ucdb_id,iou,area_ratio," + ",".join(METRICS)]
        for c in refs:
            r = rrecs[c.city_id]
            if "missing" in r or r["iou"] < IOU_MIN:
                continue
            bad = screen(r)
            vals = [("" if r["values"][k] is None or k in bad else f"{r['values'][k] * METRICS[k][2]:.6g}")
                    for k in METRICS]
            lines.append(f"{c.city_id},{c.ucdb_id},{r['iou']},{r['area_ratio']}," + ",".join(vals))
        (REFERENCE / f"{SOURCE_ID}.csv").write_text("\n".join(lines) + "\n")
        _record_inputs(names + [m for r in rrecs.values() for m in r.get("members", [])])
        print(f"reference: {len(lines) - 1}/{len(refs)} centres")


if __name__ == "__main__":
    main()
