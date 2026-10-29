"""GHS-UCDB R2024A attributes + population-weighted density from the GHS-POP R2023A 1 km grid.

Outputs
- data/interim/ghsl-ucdb.json   metrics read (or derived arithmetically) from UCDB theme layers
- data/interim/ghsl-pop.json    density_weighted, computed by us from the GHS-POP E2025 1 km raster
- data/interim/city-attributes.json  non-numeric per-city attributes (ISO2, region, income, Köppen, name list)
- data/reference/ghsl-ucdb.csv, data/reference/ghsl-pop.csv  same metrics for the 524 reference centres

Column meanings are taken from the UCDB fact sheets (GHSL_UCDB_R2024_V1_2.pdf); see etl/notes/ghsl-ucdb.md.
"""

from __future__ import annotations

import csv
import json
import re
import zipfile
from functools import cache
from pathlib import Path
from typing import Any

import numpy as np
import pycountry
import pyogrio
import rasterio
import rasterio.features
import rasterio.windows
import shapely

from .cities import GC_LAYER, UCDB_URL, City, load_cities, reference_centres, ucdb_gpkg
from .common import CACHE, INTERIM, REFERENCE, Interim, fetch

POP_URL = (
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/"
    "GHS_POP_E2025_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E2025_GLOBE_R2023A_54009_1000_V1_0.zip"
)
POP_ZIP = CACHE / "ghsl-pop" / "GHS_POP_E2025_GLOBE_R2023A_54009_1000_V1_0.zip"
POP_TIF_NAME = "GHS_POP_E2025_GLOBE_R2023A_54009_1000_V1_0.tif"
COPYRIGHT_URL = "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/copyright.txt"
# Beck et al. 2018 Köppen-Geiger V1 (the map UCDB's CL_KOP_CUR uses); needed only for its legend.txt
KG_URL = "https://ndownloader.figshare.com/files/12407516"
KG_ZIP = CACHE / "ghsl" / "Beck_KG_V1.zip"

L_GHSL = "GHSL_UCDB_THEME_GHSL_GLOBE_R2024A"
L_CLIMATE = "GHSL_UCDB_THEME_CLIMATE_GLOBE_R2024A"
L_GREEN = "GHSL_UCDB_THEME_GREENNESS_GLOBE_R2024A"
L_LULC = "GHSL_UCDB_THEME_LULC_GLOBE_R2024A"
L_EMIS = "GHSL_UCDB_THEME_EMISSIONS_GLOBE_R2024A"
L_GEO = "GHSL_UCDB_THEME_GEOGRAPHY_GLOBE_R2024A"

# Copernicus Global Land Cover (CGLS-LC100) classes as listed in the UCDB LU_HEC_* fact sheets (pp. 143-163)
LC_TREE = ["111", "112", "113", "114", "115", "116", "121", "122", "123", "124", "125", "126"]
LC_ALL = ["020", "030", "040", "050", "060", "070", "080", "090", "100", *LC_TREE]

# Country names (GC_CNT_UNN_2025, WPP2022 naming) that pycountry cannot resolve by exact name/official
# name/common name. These map a *name* to a *name*; no numeric data is typed in.
UN_NAME_ALIASES = {
    "China, Hong Kong SAR": "Hong Kong",
    "China, Macao SAR": "Macao",
    "China, Taiwan Province of China": "Taiwan, Province of China",
    "Dem. People's Republic of Korea": "Korea, Democratic People's Republic of",
    "Republic of Korea": "Korea, Republic of",
    "Turkey": "Türkiye",  # pycountry >= 24 uses the 2022 ISO short name
    "Türkiye": "Türkiye",
    "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
    "State of Palestine": "Palestine, State of",
    "Kosovo (under UNSC res. 1244)": None,  # no ISO 3166-1 code
    "Kosovo": None,
}


# --------------------------------------------------------------------------- UCDB tables
@cache
def theme(layer: str, cols: tuple[str, ...]) -> tuple[dict[str, np.ndarray], dict[int, int]]:
    meta, _f, _g, fields = pyogrio.raw.read(ucdb_gpkg(), layer=layer, columns=["ID_UC_G0", *cols],
                                            read_geometry=False)
    d = dict(zip(meta["fields"], fields, strict=True))
    return d, {int(v): i for i, v in enumerate(d["ID_UC_G0"])}


@cache
def mollweide_geoms() -> tuple[dict[int, Any], str]:
    """Native UCDB geometries (ESRI:54009) keyed by ID_UC_G0 — no reprojection needed for GHS-POP."""
    meta, _f, geoms, fields = pyogrio.raw.read(ucdb_gpkg(), layer=GC_LAYER, columns=["ID_UC_G0"])
    g = shapely.from_wkb(geoms)
    return {int(i): gg for i, gg in zip(fields[0], g, strict=True)}, str(meta["crs"])


def val(layer: str, col: str, uid: int) -> float | None:
    d, idx = theme(layer, (col,))
    v = d[col][idx[uid]]
    if v is None:
        return None
    v = float(v)
    return None if np.isnan(v) else v


def fix_mojibake(s: str) -> str:
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def iso2(un_name: str, gadm_name: str) -> str | None:
    for name in (un_name, fix_mojibake(gadm_name)):
        if name in UN_NAME_ALIASES:
            alias = UN_NAME_ALIASES[name]
            if alias is None:
                return None
            name = alias
        for key in ("name", "official_name", "common_name"):
            c = pycountry.countries.get(**{key: name})
            if c:
                return c.alpha_2
        # WPP style "Iran (Islamic Republic of)" -> "Iran, Islamic Republic of"
        m = re.fullmatch(r"(.+) \((.+)\)", name)
        if m:
            c = pycountry.countries.get(name=f"{m.group(1)}, {m.group(2)}")
            if c:
                return c.alpha_2
    return None


@cache
def koppen_legend() -> dict[int, str]:
    fetch(KG_URL, KG_ZIP, timeout=600)
    with zipfile.ZipFile(KG_ZIP) as z:
        name = next(n for n in z.namelist() if n.endswith("legend.txt"))
        text = z.read(name).decode("utf-8", "replace")
    out = {}
    for line in text.splitlines():
        m = re.match(r"\s*(\d+):\s+([A-Z][A-Za-z]{1,2})\s", line)
        if m:
            out[int(m.group(1))] = m.group(2)
    if len(out) != 30:
        raise ValueError(f"unexpected Köppen legend ({len(out)} classes)")
    return out


# --------------------------------------------------------------------------- GHS-POP
@cache
def pop_tif() -> Path:
    fetch(POP_URL, POP_ZIP, timeout=1800)
    tif = POP_ZIP.parent / POP_TIF_NAME
    if not tif.exists():
        with zipfile.ZipFile(POP_ZIP) as z:
            z.extract(POP_TIF_NAME, POP_ZIP.parent)
    return tif


def weighted_density(src: rasterio.DatasetReader, geom: Any) -> dict[str, float]:
    """Σ p_i·d_i / Σ p_i over the 1 km cells whose centre lies in the polygon, d_i = p_i / cell_area."""
    minx, miny, maxx, maxy = geom.bounds
    win = rasterio.windows.from_bounds(minx, miny, maxx, maxy, src.transform).round_offsets().round_lengths()
    arr = src.read(1, window=win, boundless=True, fill_value=src.nodata)
    tr = src.window_transform(win)
    inside = rasterio.features.geometry_mask([geom], out_shape=arr.shape, transform=tr, invert=True,
                                             all_touched=False)
    cell_km2 = abs(tr.a * tr.e) / 1e6
    p = arr[inside]
    nodata = int(np.sum(p == src.nodata))
    p = np.where(p == src.nodata, 0.0, p)
    tot = float(p.sum())
    d = p / cell_km2
    return {
        "pop_sum": tot,
        "n_cells": int(inside.sum()),
        "n_nodata": nodata,
        "cell_km2": cell_km2,
        "weighted": float((p * d).sum() / tot) if tot > 0 else float("nan"),
        "p90_cell_density": float(np.quantile(d, 0.9)) if d.size else float("nan"),
        "max_cell_density": float(d.max()) if d.size else float("nan"),
    }


# --------------------------------------------------------------------------- metrics
def ucdb_metrics(c: City) -> dict[str, tuple[float | None, str, int | str, dict | str]]:
    """metric -> (value, quality, year, detail-or-missing-reason)."""
    u = c.ucdb_id
    out: dict[str, tuple] = {}
    pop = val(GC_LAYER, "GC_POP_TOT_2025", u)
    area = val(GC_LAYER, "GC_UCA_KM2_2025", u)
    out["urban_pop"] = (pop, "estimated", 2025, {"column": "GC_POP_TOT_2025"})
    out["urban_area_km2"] = (area, "estimated", 2025, {"column": "GC_UCA_KM2_2025"})
    out["density_mean"] = (pop / area if pop and area else None, "estimated", 2025,
                           {"formula": "GC_POP_TOT_2025 / GC_UCA_KM2_2025"})
    # Built-up height: GHS-BUILT-H R2023A is derived from 2018 imagery; UCDB labels it epoch 2020.
    out["building_height_mean_m"] = (val(L_GHSL, "GH_BUH_AVG_2020", u), "estimated", 2018,
                                     {"column": "GH_BUH_AVG_2020", "ucdb_epoch_label": 2020})
    out["pm25_popweighted_ugm3"] = (val(L_EMIS, "EM_PM2_CON_2020", u), "estimated", 2020,
                                    {"column": "EM_PM2_CON_2020", "rounded_to_integer_upstream": True})
    out["ndvi_builtup_mean"] = (val(L_GREEN, "GR_AVG_GRN_2020", u), "observed", 2020,
                                {"column": "GR_AVG_GRN_2020"})
    out["elevation_mean_m"] = (val(L_GEO, "GE_ELV_AVG_2025", u), "observed", 2025, {"column": "GE_ELV_AVG_2025"})
    # Land cover 2019 (CGLS-LC100): hectares per class -> % of the sum of all listed classes. The listed classes
    # omit open sea (CGLS class 200), so coastal centres sum to < UC area; denominator = classified land + inland water.
    ha = {k: val(L_LULC, f"LU_HEC_{k}_2019", u) for k in LC_ALL}
    if any(v is None for v in ha.values()):
        out["tree_cover_share_pct"] = (None, "", 2019, "one or more LU_HEC_*_2019 classes null in UCDB")
    else:
        tot = sum(ha.values())
        det = {"lc_total_ha": round(tot, 1), "uc_area_ha": round(area * 100, 1) if area else None,
               "lc_total_over_uc_area": round(tot / (area * 100), 4) if area else None}
        out["tree_cover_share_pct"] = (100 * sum(ha[k] for k in LC_TREE) / tot, "observed", 2019,
                                       {**det, "classes": "CGLS-LC100 111-126 (closed+open forest)"})
    return out


def attributes(c: City) -> dict[str, Any]:
    u = c.ucdb_id
    d, idx = theme(GC_LAYER, ("GC_CNT_UNN_2025", "GC_CNT_GAD_2025", "GC_UCN_LIS_2025", "GC_UCM_CAP",
                              "GC_PLS_SCR_2025"))
    i = idx[u]
    un, gad = fix_mojibake(str(d["GC_CNT_UNN_2025"][i])), str(d["GC_CNT_GAD_2025"][i])
    kop = val(L_CLIMATE, "CL_KOP_CUR_2025", u)
    names = [fix_mojibake(s.strip()) for s in str(d["GC_UCN_LIS_2025"][i]).split(";") if s.strip()]
    return {
        "iso2": iso2(un, gad),
        "country_name": un,
        "country_name_gadm": fix_mojibake(gad),
        "region": c.region,
        "income": c.income,
        "ucdb_id": u,
        "name_en": c.name_en,
        "lat": c.lat,
        "lon": c.lon,
        "area_km2": c.area_km2,
        "capital": int(d["GC_UCM_CAP"][i]) == 1 if d["GC_UCM_CAP"][i] is not None else None,
        "plausibility": d["GC_PLS_SCR_2025"][i],
        "koppen_code": int(kop) if kop is not None else None,
        "koppen_class": koppen_legend().get(int(kop)) if kop is not None else None,
        "ucdb_names": names,
    }


def run(cities: tuple[City, ...], src: rasterio.DatasetReader, geoms: dict[int, Any]):
    ucdb = Interim(source_id="ghsl-ucdb", inputs=[UCDB_URL, KG_URL])
    popi = Interim(source_id="ghsl-pop", inputs=[POP_URL, UCDB_URL])
    attrs: dict[str, dict] = {}
    for c in cities:
        for m, (v, q, y, det) in ucdb_metrics(c).items():
            if v is None:
                ucdb.miss(m, c.city_id, det if isinstance(det, str) else f"{det.get('column', m)} is null in UCDB")
            else:
                ucdb.put(m, c.city_id, v, quality=q, year=y, detail=det)
        w = weighted_density(src, geoms[c.ucdb_id])
        if w["pop_sum"] > 0:
            popi.put("density_weighted", c.city_id, w["weighted"], quality="estimated", year=2025, detail={
                "n_cells_1km": w["n_cells"], "n_nodata": w["n_nodata"], "grid_pop_sum": round(w["pop_sum"]),
                "grid_pop_over_ucdb_pop": round(w["pop_sum"] / c.pop_2025, 6),
                "p90_cell_density": round(w["p90_cell_density"]), "max_cell_density": round(w["max_cell_density"]),
            })
        else:
            popi.miss("density_weighted", c.city_id, "no population in GHS-POP cells inside polygon")
        attrs[c.city_id] = attributes(c)
    return ucdb, popi, attrs


def write_reference(path: Path, it: Interim, attrs: dict[str, dict]) -> None:
    metrics = sorted(it.values)
    REFERENCE.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["city_id", "ucdb_id", "name_en", "iso2", "region", *metrics])
        for cid, a in attrs.items():
            row = [cid, a["ucdb_id"], a["name_en"], a["iso2"] or "", a["region"]]
            for m in metrics:
                e = it.values[m].get(cid)
                row.append("" if e is None else f"{e['value']:.6g}")
            w.writerow(row)


def main() -> None:
    fetch(COPYRIGHT_URL, CACHE / "ghsl" / "copyright.txt")
    geoms, crs = mollweide_geoms()
    tif = pop_tif()
    with rasterio.open(tif) as src:
        if "54009" not in str(src.crs) or "54009" not in crs:
            raise ValueError(f"CRS mismatch: raster {src.crs} vs UCDB {crs[:40]}")
        targets = load_cities()
        ucdb, popi, attrs = run(targets, src, geoms)
        ref = reference_centres()
        r_ucdb, r_pop, r_attrs = run(ref, src, geoms)

    nmiss = [c for c, a in attrs.items() if a["iso2"] is None]
    ucdb.notes += [
        ("GHS-UCDB R2024A V1.2 (doi:10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd); column meanings per "
         "GHSL_UCDB_R2024_V1_2.pdf fact sheets — see etl/notes/ghsl-ucdb.md."),
        ("urban_pop/density_mean derive from GHS-POP R2023A epoch 2025, which is a model extrapolation "
         "(census growth rates, WPP2022, WUP2018) -> quality=estimated."),
        f"iso2 unresolved for: {nmiss}" if nmiss else "iso2 resolved for all target cities.",
    ]
    popi.notes += [
        ("density_weighted = Σ p_i² / Σ p_i over 1 km GHS-POP E2025 cells (ESRI:54009, 1 km² cells) whose "
         "centre lies inside the native-Mollweide UCDB polygon; polygons are unions of the same 1 km grid."),
    ]
    for it in (ucdb, popi):
        print("wrote", it.write())
    INTERIM.mkdir(parents=True, exist_ok=True)
    (INTERIM / "city-attributes.json").write_text(json.dumps(attrs, indent=2, ensure_ascii=False, default=str) + "\n")
    write_reference(REFERENCE / "ghsl-ucdb.csv", r_ucdb, r_attrs)
    write_reference(REFERENCE / "ghsl-pop.csv", r_pop, r_attrs)
    rmiss = [c for c, a in r_attrs.items() if a["iso2"] is None]
    print(f"targets {len(targets)}; reference {len(ref)}; iso2 missing targets={nmiss} reference={len(rmiss)} "
          f"{[r_attrs[c]['country_name'] for c in rmiss]}")



# --------------------------------------------------------------------------- validation (prints numbers quoted in notes)
def _rank(x: np.ndarray) -> np.ndarray:
    return np.argsort(np.argsort(x)).astype(float)


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.corrcoef(_rank(a), _rank(b))[0, 1])


def validate() -> None:
    import csv as _csv

    u = json.loads((INTERIM / "ghsl-ucdb.json").read_text())["values"]
    p = json.loads((INTERIM / "ghsl-pop.json").read_text())["values"]
    attrs = json.loads((INTERIM / "city-attributes.json").read_text())
    allm = {**u, **p}
    print("== distributions over 86 targets: min / median / max (city)")
    for m, vals in sorted(allm.items()):
        items = sorted(vals.items(), key=lambda kv: kv[1]["value"])
        v = np.array([e["value"] for _, e in items])
        print(f"  {m:24} n={len(v):3}  min={v[0]:.4g} ({items[0][0]})  median={np.median(v):.4g}  "
              f"max={v[-1]:.4g} ({items[-1][0]})")
    ids = sorted(p["density_weighted"])
    dm = np.array([u["density_mean"][c]["value"] for c in ids])
    dw = np.array([p["density_weighted"][c]["value"] for c in ids])
    print(f"== Spearman(mean, weighted) targets: {spearman(dm, dw):.3f}; ratio weighted/mean "
          f"min={np.min(dw / dm):.2f} median={np.median(dw / dm):.2f} max={np.max(dw / dm):.2f}")
    rm, rw = _rank(-dm), _rank(-dw)
    shift = sorted(zip(ids, rm - rw, rm, rw, strict=True), key=lambda t: -abs(t[1]))[:12]
    print("  largest rank shifts (rank 0 = densest):",
          ", ".join(f"{c} {int(a)}->{int(b)}" for c, _, a, b in shift))
    ref = list(_csv.DictReader((REFERENCE / "ghsl-ucdb.csv").open()))
    refp = {r["city_id"]: r for r in _csv.DictReader((REFERENCE / "ghsl-pop.csv").open())}
    a = np.array([float(r["density_mean"]) for r in ref])
    b = np.array([float(refp[r["city_id"]]["density_weighted"]) for r in ref])
    print(f"== reference 524: Spearman(mean, weighted)={spearman(a, b):.3f}; weighted p10/p50/p90 = "
          f"{np.percentile(b, 10):.0f}/{np.percentile(b, 50):.0f}/{np.percentile(b, 90):.0f}")
    lc = np.array([u["tree_cover_share_pct"][c]["detail"]["lc_total_over_uc_area"] for c in ids])
    print(f"== land-cover hectares sum / UC area: min={lc.min():.3f} median={np.median(lc):.3f} max={lc.max():.3f}")
    print("== polygons listing >= 5 named places (GC_UCN_LIS_2025):")
    for c in sorted(attrs, key=lambda c: -len(attrs[c]["ucdb_names"])):
        n = attrs[c]["ucdb_names"]
        if len(n) >= 5:
            print(f"  {c:14} names={len(n):3} pop={u['urban_pop'][c]['value'] / 1e6:6.2f}M "
                  f"area={u['urban_area_km2'][c]['value']:6.0f}km2  {'; '.join(n[:12])}")


if __name__ == "__main__":
    main()
    validate()
