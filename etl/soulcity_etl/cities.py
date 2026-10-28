"""City master: config/cities.yaml joined to GHS-UCDB R2024A urban-centre polygons.

The GHS-UCDB polygon is the single geographic definition of a "city" in this project. Every
source module computes its values on this polygon (or must document why it cannot).
"""

from __future__ import annotations

import zipfile
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import numpy as np
import pyogrio
import shapely
import yaml

from .common import CACHE, REPO, fetch

UCDB_URL = (
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_UCDB_GLOBE_R2024A/"
    "GHS_UCDB_GLOBE_R2024A/V1-2/GHS_UCDB_GLOBE_R2024A_V1_2.zip"
)
UCDB_ZIP = CACHE / "ghsl" / "GHS_UCDB_GLOBE_R2024A_V1_2.zip"
UCDB_GPKG = CACHE / "ghsl" / "GHS_UCDB_GLOBE_R2024A.gpkg"
GC_LAYER = "GHSL_UCDB_THEME_GENERAL_CHARACTERISTICS_GLOBE_R2024A"
CONFIG = REPO / "etl" / "config" / "cities.yaml"
# Reference population for normalisation checks: all urban centres with >= this many inhabitants.
REFERENCE_MIN_POP = 1_000_000


@dataclass(frozen=True)
class City:
    city_id: str
    name_ja: str
    name_en: str
    country: str
    ucdb_id: int
    region: str  # UN SDG region (GC_DEV_USR_2025)
    income: str  # World Bank income group (GC_DEV_WIG_2025)
    pop_2025: float
    area_km2: float
    lat: float
    lon: float
    geom: shapely.Geometry  # EPSG:4326 (MultiPolygon)


def ucdb_gpkg() -> Path:
    if not UCDB_GPKG.exists():
        fetch(UCDB_URL, UCDB_ZIP, timeout=600)
        with zipfile.ZipFile(UCDB_ZIP) as z:
            z.extract(UCDB_GPKG.name, UCDB_GPKG.parent)
    else:
        fetch(UCDB_URL, UCDB_ZIP, timeout=600) if UCDB_ZIP.exists() else None
    return UCDB_GPKG


@cache
def _ucdb_table() -> dict[str, np.ndarray]:
    path = ucdb_gpkg()
    meta, _fids, geoms, fields = pyogrio.raw.read(
        path,
        layer=GC_LAYER,
        columns=["ID_UC_G0", "GC_UCN_MAI_2025", "GC_CNT_GAD_2025", "GC_UCA_KM2_2025", "GC_POP_TOT_2025",
                 "GC_DEV_USR_2025", "GC_DEV_WIG_2025"],
    )
    crs = meta["crs"]
    cols = dict(zip(meta["fields"], fields, strict=True))
    g = shapely.from_wkb(geoms)
    if crs and "4326" not in str(crs):
        from pyproj import Transformer

        tr = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
        g = shapely.transform(g, lambda xy: np.column_stack(tr.transform(xy[:, 0], xy[:, 1])))
    cols["geometry"] = g
    return cols


def all_centres() -> dict[str, np.ndarray]:
    """Raw UCDB general-characteristics table (all 11k+ centres), geometry in EPSG:4326."""
    return _ucdb_table()


def _make(entry: dict, t: dict[str, np.ndarray], i: int) -> City:
    g = t["geometry"][i]
    # representative point is guaranteed inside the polygon (centroid may fall outside)
    p = shapely.point_on_surface(g)
    return City(
        city_id=entry["city_id"],
        name_ja=entry["name_ja"],
        name_en=str(t["GC_UCN_MAI_2025"][i]),
        country=str(t["GC_CNT_GAD_2025"][i]),
        ucdb_id=int(t["ID_UC_G0"][i]),
        region=str(t["GC_DEV_USR_2025"][i]),
        income=str(t["GC_DEV_WIG_2025"][i]),
        pop_2025=float(t["GC_POP_TOT_2025"][i]),
        area_km2=float(t["GC_UCA_KM2_2025"][i]),
        lat=round(p.y, 4),
        lon=round(p.x, 4),
        geom=g,
    )


@cache
def load_cities() -> tuple[City, ...]:
    cfg = yaml.safe_load(CONFIG.read_text())["cities"]
    t = _ucdb_table()
    index = {int(v): i for i, v in enumerate(t["ID_UC_G0"])}
    out = []
    seen: set[str] = set()
    for e in cfg:
        if e["city_id"] in seen:
            raise ValueError(f"duplicate city_id {e['city_id']}")
        seen.add(e["city_id"])
        i = index.get(int(e["ucdb_id"]))
        if i is None:
            raise ValueError(f"{e['city_id']}: ucdb_id {e['ucdb_id']} not in GHS-UCDB")
        if str(t["GC_UCN_MAI_2025"][i]) != e["ucdb_name"]:
            raise ValueError(f"{e['city_id']}: ucdb_id {e['ucdb_id']} is {t['GC_UCN_MAI_2025'][i]!r}, "
                             f"expected {e['ucdb_name']!r}")
        out.append(_make(e, t, i))
    return tuple(out)


@cache
def reference_centres() -> tuple[City, ...]:
    """All urban centres with population >= REFERENCE_MIN_POP (for normalisation-sensitivity checks).

    city_id is `uc-<ID_UC_G0>`; the target cities are included under their own ids.
    """
    t = _ucdb_table()
    targets = {c.ucdb_id: c for c in load_cities()}
    out = []
    for i in np.flatnonzero(t["GC_POP_TOT_2025"] >= REFERENCE_MIN_POP):
        uid = int(t["ID_UC_G0"][i])
        out.append(targets.get(uid) or _make({"city_id": f"uc-{uid}", "name_ja": ""}, t, int(i)))
    return tuple(out)


if __name__ == "__main__":
    cs = load_cities()
    print(f"{len(cs)} cities OK; reference set {len(reference_centres())} centres >= {REFERENCE_MIN_POP:,}")
    for c in cs:
        print(f"  {c.city_id:16} {c.ucdb_id:6} {c.name_en:20} {c.country:16} {c.region:28} pop={c.pop_2025:,.0f}")
