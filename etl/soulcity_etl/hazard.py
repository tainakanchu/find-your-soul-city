"""Natural-hazard exposure per urban centre, from the GHS-UCDB R2024A EXPOSURE and HAZARD_RISK themes.

Outputs
- data/interim/ghsl-hazard.json    metrics for the target cities (source_id "ghsl-hazard")
- data/reference/ghsl-hazard.csv   same metrics for the 524 reference centres (pop >= 1M)

All numbers are read from (or computed arithmetically on) UCDB columns whose meaning is taken from the fact sheets
in GHSL_UCDB_R2024_V1_2.pdf; see etl/notes/ghsl-hazard.md for the column dictionary, the checks behind each rule
below and the columns we rejected (the cyclone-wind exposure columns EX_*_S1P/S3P fail basic plausibility).

Metrics (lower = fewer natural hazards)
- quake_pop_share_mmi6plus_pct    EX_SHA_POP_2025: % of 2025 population in GEM 475-yr hazard class MMI >= 6
- quake_mmi_excess_popweighted    Σ max(0, MMI-5)·pop / Σ pop over EX_E01..E10_POP_2025 — our derivation: mean MMI
                                  steps above V (VI = first damaging class), 0 where no one lives at MMI >= VI
- river_flood_pop_share_100y_pct  EX_100_SHP_2025: % of population inside the GloFAS 100-yr river-flood extent
- coastal_flood_pop_share_100y_pct EX_CF1_SHP_2025: % of population inside the JRC 100-yr coastal-flood extent
- flood_pop_share_100y_pct        max(river, coastal): lower bound of the union (overlap is not published)
- tropical_cyclone_hazards_per_year  Σ HZ_CEV_TCY_{2005,2010,2015} / 9: MYRIAD-HES tropical-cyclone footprints
                                     overlapping the centre in 2004-06, 2009-11, 2014-16
"""

from __future__ import annotations

import csv
import json
from functools import cache
from typing import Any

import numpy as np
import pyogrio

from .cities import UCDB_URL, City, load_cities, reference_centres, ucdb_gpkg
from .common import CACHE, INTERIM, REFERENCE, Interim, fetch

SOURCE_ID = "ghsl-hazard"
L_EXP = "GHSL_UCDB_THEME_EXPOSURE_GLOBE_R2024A"
L_HZ = "GHSL_UCDB_THEME_HAZARD_RISK_GLOBE_R2024A"
EPOCH = "2025"

# Upstream licence / metadata documents (read for the notes; recorded in provenance so the run is traceable).
DOCS = {
    "https://zenodo.org/api/records/8409647": "zenodo_8409647_gem_gshm.json",  # GEM GSHM 2023.1
    "https://zenodo.org/api/records/8269680": "zenodo_8269680_myriad_hes.json",  # MYRIAD-HES
    "https://zenodo.org/api/records/8269680/files/METADATA.pdf/content": "MYRIAD-HES_METADATA.pdf",
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/copyright.txt":
        "glofas_flood_hazard_copyright.txt",
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/README.txt":
        "glofas_flood_hazard_README.txt",
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/CHANGELOG.txt":
        "glofas_flood_hazard_CHANGELOG.txt",
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LISCOAST/copyright.txt": "liscoast_copyright.txt",
}

# GEM-derived MMI classes as published (fact sheets pp.176-184): E01=1, E02="2-3", E04..E10 = 4..10.
# "2-3" is one class, coded 2.5; it never matters because only classes >= 6 enter the excess index.
MMI_CLASSES = {"E01": 1.0, "E02": 2.5, "E04": 4.0, "E05": 5.0, "E06": 6.0, "E07": 7.0, "E08": 8.0, "E09": 9.0,
               "E10": 10.0}
MMI_FLOOR = 5.0  # MMI V; excess index counts steps above it (VI "slight damage" .. X)
TC_EPOCHS = ("2005", "2010", "2015")  # each = previous, same and next year (fact sheet p.345)
TC_YEARS = 3 * len(TC_EPOCHS)
TOL_PCT = 0.01  # UCDB shares are rounded to 2 decimals
YEAR_TC = "2004-2016"

EXP_COLS = (
    "GC_POP_TOT_2025",
    *(f"EX_{k}_POP_{EPOCH}" for k in MMI_CLASSES),
    f"EX_SHA_POP_{EPOCH}",
    f"EX_010_POP_{EPOCH}", f"EX_100_POP_{EPOCH}", f"EX_010_SHP_{EPOCH}", f"EX_100_SHP_{EPOCH}",
    f"EX_CF2_SHP_{EPOCH}", f"EX_CF1_SHP_{EPOCH}", f"EX_CF1_POP_{EPOCH}",
    f"EX_LEC_SHP_{EPOCH}",
)
HZ_COLS = (*(f"HZ_CEV_TCY_{y}" for y in TC_EPOCHS), *(f"HZ_CEV_TEV_{y}" for y in TC_EPOCHS))

METRICS = ("quake_pop_share_mmi6plus_pct", "quake_mmi_excess_popweighted", "river_flood_pop_share_100y_pct",
           "coastal_flood_pop_share_100y_pct", "flood_pop_share_100y_pct", "tropical_cyclone_hazards_per_year")


@cache
def table(layer: str, cols: tuple[str, ...]) -> tuple[dict[str, np.ndarray], dict[int, int]]:
    meta, _f, _g, fields = pyogrio.raw.read(ucdb_gpkg(), layer=layer, columns=["ID_UC_G0", *cols],
                                            read_geometry=False)
    d = {k: (np.asarray(v, dtype=float) if k != "ID_UC_G0" else v) for k, v in zip(meta["fields"], fields,
                                                                                    strict=True)}
    return d, {int(v): i for i, v in enumerate(d["ID_UC_G0"])}


def _get(layer: str, cols: tuple[str, ...], uid: int) -> dict[str, float | None]:
    d, idx = table(layer, cols)
    i = idx[uid]
    return {c: (None if np.isnan(d[c][i]) else float(d[c][i])) for c in cols}


def metrics(c: City) -> dict[str, tuple[float | None, int | str, dict | str]]:
    """metric -> (value, year, detail) or (None, year, missing-reason)."""
    e = _get(L_EXP, EXP_COLS, c.ucdb_id)
    h = _get(L_HZ, HZ_COLS, c.ucdb_id)
    out: dict[str, tuple] = {}
    pop = e["GC_POP_TOT_2025"]

    # --- earthquake (GEM GSHM 2023.1, PGA 10 % in 50 yr on rock, as MMI classes by JRC)
    cls = {k: e[f"EX_{k}_POP_{EPOCH}"] for k in MMI_CLASSES}
    if any(v is None for v in cls.values()) or not pop:
        reason = "one or more EX_E*_POP_2025 columns null in UCDB"
        out["quake_pop_share_mmi6plus_pct"] = (None, 2025, reason)
        out["quake_mmi_excess_popweighted"] = (None, 2025, reason)
    else:
        tot = sum(cls.values())
        shares = {k: round(100 * v / tot, 2) for k, v in cls.items() if v > 0}
        sha = e[f"EX_SHA_POP_{EPOCH}"]
        if sha is None:
            out["quake_pop_share_mmi6plus_pct"] = (None, 2025, "EX_SHA_POP_2025 null in UCDB")
        else:
            out["quake_pop_share_mmi6plus_pct"] = (sha, 2025, {
                "column": f"EX_SHA_POP_{EPOCH}",
                "check_100_x_sum_E06_E10_over_pop": round(
                    100 * sum(cls[k] for k in ("E06", "E07", "E08", "E09", "E10")) / pop, 3)})
        if tot <= 0:
            out["quake_mmi_excess_popweighted"] = (None, 2025, "no population in any EX_E*_POP_2025 class")
        else:
            out["quake_mmi_excess_popweighted"] = (
                sum(max(0.0, MMI_CLASSES[k] - MMI_FLOOR) * v for k, v in cls.items()) / tot, 2025, {
                    "class_pop_share_pct": shares, "class_pop_sum_over_ucdb_pop": round(tot / pop, 5),
                    "formula": "sum(max(0, MMI-5)*pop)/sum(pop) over EX_E01..E10_POP_2025"})

    # --- river flood (GloFAS / CEMS global flood hazard maps, Baugh et al. 2024)
    p10, p100 = e[f"EX_010_POP_{EPOCH}"], e[f"EX_100_POP_{EPOCH}"]
    s10, s100 = e[f"EX_010_SHP_{EPOCH}"], e[f"EX_100_SHP_{EPOCH}"]
    river: float | None = None
    if None in (p10, p100, s100):
        out["river_flood_pop_share_100y_pct"] = (None, 2025, "EX_100_SHP_2025 / EX_0x0_POP_2025 null in UCDB")
    elif s10 is not None and s10 > s100 + TOL_PCT:
        # A 10-yr flood extent cannot exceed the 100-yr one; this happens only in one block of north-China
        # centres where EX_100_* is 0 (a gap in the 100-yr layer UCDB used). Treat as not computable.
        out["river_flood_pop_share_100y_pct"] = (None, 2025, (
            f"inconsistent UCDB flood columns: 10-yr share {s10:.2f}% > 100-yr share {s100:.2f}% "
            "(100-yr layer gap upstream)"))
    else:
        river = s100
        out["river_flood_pop_share_100y_pct"] = (s100, 2025, {
            "column": f"EX_100_SHP_{EPOCH}", "share_10y_pct": s10, "pop_100y": round(p100)})

    # --- coastal flood (JRC LISFLOOD-FP coastal inundation, Vousdoukas et al. 2018)
    cf100, cf20 = e[f"EX_CF1_SHP_{EPOCH}"], e[f"EX_CF2_SHP_{EPOCH}"]
    coastal: float | None = None
    if cf100 is None:
        out["coastal_flood_pop_share_100y_pct"] = (None, 2025, "EX_CF1_SHP_2025 null in UCDB")
    else:
        coastal = cf100
        out["coastal_flood_pop_share_100y_pct"] = (cf100, 2025, {
            "column": f"EX_CF1_SHP_{EPOCH}", "share_20y_pct": cf20,
            "lecz_below_10m_pct": e[f"EX_LEC_SHP_{EPOCH}"]})

    if river is None or coastal is None:
        out["flood_pop_share_100y_pct"] = (None, 2025, "river or coastal 100-yr flood share not available")
    else:
        out["flood_pop_share_100y_pct"] = (max(river, coastal), 2025, {
            "formula": "max(EX_100_SHP, EX_CF1_SHP): lower bound of the union (overlap not published)",
            "upper_bound_pct": round(min(100.0, river + coastal), 2)})

    # --- tropical cyclones (MYRIAD-HES event footprints, Claassen et al. 2023)
    # A hazard count is null when the spatial join found no hazard of that type; no 0 ever occurs in any
    # HZ_CEV_* column (checked over all 11,422 centres), so null -> 0 — but only if the centre took part in the
    # join that epoch (HZ_CEV_TEV, total events, non-null). Otherwise we cannot tell.
    if any(h[f"HZ_CEV_TEV_{y}"] is None for y in TC_EPOCHS):
        out["tropical_cyclone_hazards_per_year"] = (None, YEAR_TC,
                                                    "HZ_CEV_TEV null for an epoch: centre not covered by the join")
    else:
        per = {y: h[f"HZ_CEV_TCY_{y}"] or 0.0 for y in TC_EPOCHS}
        out["tropical_cyclone_hazards_per_year"] = (sum(per.values()) / TC_YEARS, YEAR_TC, {
            "counts_by_window": {f"{int(y) - 1}-{int(y) + 1}": int(v) for y, v in per.items()},
            "null_read_as_zero": [y for y in TC_EPOCHS if h[f"HZ_CEV_TCY_{y}"] is None]})
    return out


def run(cities: tuple[City, ...]) -> Interim:
    it = Interim(source_id=SOURCE_ID, inputs=[UCDB_URL, *DOCS])
    for c in cities:
        for m, (v, y, det) in metrics(c).items():
            if v is None:
                it.miss(m, c.city_id, det)
            else:
                it.put(m, c.city_id, v, quality="estimated", year=y, detail=det)
    return it


def write_reference(it: Interim, cities: tuple[City, ...]) -> None:
    REFERENCE.mkdir(parents=True, exist_ok=True)
    with (REFERENCE / f"{SOURCE_ID}.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["city_id", "ucdb_id", "name_en", "region", *METRICS])
        for c in cities:
            row: list[Any] = [c.city_id, c.ucdb_id, c.name_en, c.region]
            for m in METRICS:
                e = it.values.get(m, {}).get(c.city_id)
                row.append("" if e is None else f"{e['value']:.6g}")
            w.writerow(row)


def main() -> None:
    for url, name in DOCS.items():
        fetch(url, CACHE / SOURCE_ID / name, timeout=120)
    it = run(load_cities())
    it.notes += [
        ("GHS-UCDB R2024A V1.2 EXPOSURE + HAZARD_RISK themes (doi:10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd); "
         "column meanings per GHSL_UCDB_R2024_V1_2.pdf pp.164-185, 294-301, 337-350 — see etl/notes/ghsl-hazard.md."),
        ("All metrics are modelled hazard footprints/maps overlaid on GHS-POP R2023A epoch 2025 -> "
         "quality=estimated. Hazard maps ignore flood defences and building codes: this is exposure, not risk."),
        ("Earthquake columns derive from the GEM Global Seismic Hazard Map 2023.1, licensed CC BY-NC-SA 4.0 "
         "(non-commercial, share-alike) — check before commercial use."),
        ("Cyclone-wind exposure columns (EX_*_S1P/S3P, STORM) were NOT used: implausible values (shares up to 200 %, "
         "zero for Tokyo/Hong Kong/Miami, non-zero for Marrakesh/Caracas). Typhoon exposure uses MYRIAD-HES counts."),
    ]
    print("wrote", it.write())
    ref = reference_centres()
    write_reference(run(ref), ref)
    print("wrote", REFERENCE / f"{SOURCE_ID}.csv")


# --------------------------------------------------------------------------- validation (numbers quoted in notes)
def _rank(x: np.ndarray) -> np.ndarray:
    o = np.argsort(x, kind="stable")
    r = np.empty(len(x))
    r[o] = np.arange(len(x))
    # average ties
    for v in np.unique(x):
        m = x == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ok = ~(np.isnan(a) | np.isnan(b))
    if ok.sum() <= 10 or np.ptp(a[ok]) == 0 or np.ptp(b[ok]) == 0:
        return float("nan")
    return float(np.corrcoef(_rank(a[ok]), _rank(b[ok]))[0, 1])


def _read_ref(name: str) -> dict[str, dict[str, str]]:
    with (REFERENCE / name).open() as f:
        return {r["city_id"]: r for r in csv.DictReader(f)}


def validate() -> None:
    d = json.loads((INTERIM / f"{SOURCE_ID}.json").read_text())
    v, miss = d["values"], d["missing"]
    print("== targets: n / missing / min / median / max")
    for m in METRICS:
        items = sorted(v.get(m, {}).items(), key=lambda kv: kv[1]["value"])
        x = np.array([e["value"] for _, e in items])
        print(f"  {m:34} n={len(x):3} miss={len(miss.get(m, {}))}  min={x[0]:.3g} ({items[0][0]})  "
              f"median={np.median(x):.3g}  max={x[-1]:.3g} ({items[-1][0]})  zeros={int((x == 0).sum())}")
    for m, cs in miss.items():
        for c, r in cs.items():
            print(f"  missing {m}/{c}: {r}")
    print("== sanity cities")
    for c in ["tokyo", "osaka", "manila", "taipei", "dhaka", "kolkata", "shanghai", "bangkok", "amsterdam",
              "istanbul", "los-angeles", "miami", "hong-kong", "madrid", "denver", "paris", "london", "berlin",
              "moscow", "riyadh"]:
        if c not in d["values"]["quake_mmi_excess_popweighted"] and c not in miss.get("quake_mmi_excess_popweighted", {}):
            continue
        print(f"  {c:12}", "  ".join(f"{m.split('_')[0][:5]}{m.split('_')[1][:4]}="
                                     f"{v[m][c]['value']:.2f}" if c in v.get(m, {}) else f"{m}=NA" for m in METRICS))
    ref = _read_ref(f"{SOURCE_ID}.csv")
    ids = sorted(ref)
    cols = {m: np.array([float(ref[i][m]) if ref[i][m] else np.nan for i in ids]) for m in METRICS}
    print(f"== reference {len(ids)}: missing per metric",
          {m: int(np.isnan(x).sum()) for m, x in cols.items()})
    for m, x in cols.items():
        q = np.nanpercentile(x, [10, 25, 50, 75, 90])
        print(f"  {m:34} p10/25/50/75/90 = {' / '.join(f'{a:.3g}' for a in q)}  share zero={np.nanmean(x == 0):.2f}")
    print("== reference: mean by UN SDG region (n)")
    regions = sorted({ref[i]["region"] for i in ids})
    for r in regions:
        msk = np.array([ref[i]["region"] == r for i in ids])
        print(f"  {r:40} n={msk.sum():3} " + " ".join(f"{np.nanmean(cols[m][msk]):6.2f}" for m in METRICS))
    print("   columns:", ", ".join(METRICS))
    print("== Spearman among hazard metrics (reference)")
    for i, a in enumerate(METRICS):
        print(f"  {a:34}", " ".join(f"{spearman(cols[a], cols[b]):5.2f}" for b in METRICS[: i + 1]))
    print("== Spearman vs existing reference metrics (|rho| >= 0.25 shown)")
    for fname in sorted(p.name for p in REFERENCE.glob("*.csv")):
        if fname == f"{SOURCE_ID}.csv":
            continue
        other = _read_ref(fname)
        for col in list(next(iter(other.values())).keys()):
            if col in ("city_id", "ucdb_id", "name_en", "iso2", "region", "cell_rule"):
                continue
            try:
                y = np.array([float(other[i][col]) if i in other and other[i][col] not in ("", "nan") else np.nan
                              for i in ids])
            except ValueError:
                continue
            rs = {m: spearman(cols[m], y) for m in METRICS}
            if any(abs(r) >= 0.25 for r in rs.values()):
                print(f"  {fname:20} {col:26}", " ".join(f"{m[:12]}={r:+.2f}" for m, r in rs.items()))
    # Cross-check of the modelled river-flood share against MYRIAD-HES observed flood-hazard counts.
    hz, idx = table(L_HZ, (*(f"HZ_CEV_FLO_{y}" for y in TC_EPOCHS), *(f"HZ_CEV_TEV_{y}" for y in TC_EPOCHS)))
    flo = np.array([np.nansum([hz[f"HZ_CEV_FLO_{y}"][idx[int(ref[i]["ucdb_id"])]] for y in TC_EPOCHS]) for i in ids])
    print(f"== Spearman(river_flood_share_100y, MYRIAD flood hazards 2004-16) = "
          f"{spearman(cols['river_flood_pop_share_100y_pct'], flo):.2f}")
    # Composite used only to illustrate the recommendation: mean percentile of quake MMI, flood, cyclone.
    fam = ["quake_mmi_excess_popweighted", "flood_pop_share_100y_pct", "tropical_cyclone_hazards_per_year"]
    ok = ~np.any([np.isnan(cols[m]) for m in fam], axis=0)  # complete rows only; nothing is filled
    pct = {m: np.full(len(ids), np.nan) for m in fam}
    for m in fam:
        pct[m][ok] = _rank(cols[m][ok]) / (ok.sum() - 1)
    comp = np.mean([pct[m] for m in fam], axis=0)
    tgt = {c.city_id for c in load_cities()}
    order = sorted((i for i in range(len(ids)) if ids[i] in tgt and ok[i]), key=lambda k: comp[k])
    print("== illustrative composite (mean reference percentile of", fam, ") targets lowest 12:",
          ", ".join(f"{ids[k]} {comp[k]:.2f}" for k in order[:12]))
    print("   highest 12:", ", ".join(f"{ids[k]} {comp[k]:.2f}" for k in order[-12:]))


if __name__ == "__main__":
    main()
    validate()
