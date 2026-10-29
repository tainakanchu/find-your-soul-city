"""OpenStreetMap culture / nightlife POI density per GHS-UCDB urban centre, with coverage validation.

Pipeline (all inputs cached under .cache/raw/osm/):
1. OSM POIs: every feature (node/way/relation) carrying one of the tags in CULTURE_TAGS / NIGHTLIFE_TAGS is
   pulled planet-wide from the QLever OSM-planet SPARQL endpoint (osm2rdf conversion of a dated planet PBF),
   one paged query per tag, with the feature centroid (geof:centroid of its full geometry, equivalent to
   Overpass `out center`). The public Overpass mirrors were unreachable or overloaded when this was built
   (see notes). Points are then assigned to UCDB polygons locally with shapely (point-in-polygon).
2. Metrics: de-duplicated venue counts / polygon area (km²) and / population (per 100k).
3. Validation (independent of OSM):
   a. Wikidata museums / theatre buildings / concert halls with coordinates inside the polygon (QLever Wikidata
      endpoint): recall = share found in OSM's culture set (wikidata-tag link or name+proximity match).
   b. Overture Maps places (non-OSM sources: Meta, Microsoft, Foursquare, ...): OSM/Overture count ratio per
      comparable category, for the 86 target cities.
   c. Consistency of the QLever snapshot against the live OSM API for a few small boxes.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import math
import re
import time
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any

import numpy as np
import requests
import shapely

from .cities import City, load_cities, reference_centres
from .common import CACHE, REFERENCE, Interim, fetch, record_dataset

SOURCE_ID = "osm"
RAW = CACHE / "osm"
QLEVER_OSM = "https://qlever.cs.uni-freiburg.de/api/osm-planet"
QLEVER_WD = "https://qlever.cs.uni-freiburg.de/api/wikidata"
OSM_API = "https://api.openstreetmap.org/api/0.6/map"
OVERTURE_RELEASE = "2026-10-21.0"
OVERTURE_URL = f"s3://overturemaps-us-west-2/release/{OVERTURE_RELEASE}/theme=places/type=place/*.parquet"
UA = {"User-Agent": "soulcity-etl/0.1 (research ETL; github.com/find-your-soul-city)"}
PAGE = 50_000

# --- tag set (wiki status checked on wiki.openstreetmap.org, see notes) -------------------------------------
CULTURE_TAGS: list[tuple[str, str]] = [
    ("tourism", "museum"),       # approved
    ("tourism", "gallery"),      # approved (art exhibitions; commercial galleries should be shop=art)
    ("amenity", "theatre"),      # approved (plays, musicals, formal concerts)
    ("amenity", "arts_centre"),  # de facto
    ("amenity", "cinema"),       # approved
    ("amenity", "music_venue"),  # in use: "indoor place to hear live music which is not a theatre"
    ("amenity", "concert_hall"),  # in use (rare; most halls are amenity=theatre + theatre:type=concert_hall)
]
NIGHTLIFE_TAGS: list[tuple[str, str]] = [
    ("amenity", "nightclub"),    # approved
    ("amenity", "bar"),          # de facto
    ("amenity", "pub"),          # de facto
]
GROUPS = {"culture": CULTURE_TAGS, "nightlife": NIGHTLIFE_TAGS}
DEDUP_M = 150.0  # same group + same normalised name within this distance -> one venue (node + building mapped twice)

# Wikidata classes used as the independent culture benchmark (instances of the class or any subclass).
WD_CLASSES = {"Q33506": "museum", "Q24354": "theatre building", "Q1060829": "concert hall"}
MATCH_M = 250.0  # name+proximity match radius between a Wikidata item and an OSM culture feature
NAME_SIM = 0.75

# Overture basic_category -> comparable OSM tag subset
OVERTURE_PAIRS = {
    "museum": (["museum"], [("tourism", "museum")]),
    "performing_arts": (["theatre_venue", "performing_arts_venue", "music_venue"],
                        [("amenity", "theatre"), ("amenity", "arts_centre"), ("amenity", "music_venue"),
                         ("amenity", "concert_hall")]),
    "cinema": (["movie_theater"], [("amenity", "cinema")]),
    "gallery": (["art_gallery"], [("tourism", "gallery")]),
    "bar_pub": (["bar"], [("amenity", "bar"), ("amenity", "pub")]),
    "nightclub": (["dance_club"], [("amenity", "nightclub")]),
}
OVERTURE_MIN_CONF = 0.5


# --- SPARQL plumbing ------------------------------------------------------------------------------------------
def _sparql_tsv(endpoint: str, query: str, dest: Path, *, retries: int = 5, timeout: float = 600,
                expected: int | None = None) -> list[list[str]]:
    """Run `query` against a QLever endpoint, cache the TSV at `dest`, return parsed rows (header dropped).

    `expected`: row count the result must have (from a COUNT query) - responses can be silently truncated by the
    server or proxy, so a mismatching cache file is discarded and the query re-run."""
    for _ in range(3):
        rows = _sparql_tsv_once(endpoint, query, dest, retries=retries, timeout=timeout)
        if expected is None or len(rows) == expected:
            return rows
        print(f"    truncated response ({len(rows)} rows, expected {expected}); retrying {dest.name}")
        dest.unlink()
        time.sleep(30)
    raise RuntimeError(f"{dest}: could not obtain a complete result")


def _count(endpoint: str, where: str, prefixes: str, dest: Path) -> int:
    rows = _sparql_tsv_once(endpoint, prefixes + f"SELECT (COUNT(DISTINCT ?x) AS ?n) WHERE {{ {where} }}", dest)
    return _int(rows[0][0])


def _sparql_tsv_once(endpoint: str, query: str, dest: Path, *, retries: int = 5,
                     timeout: float = 600) -> list[list[str]]:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(retries + 1):
            try:
                r = requests.post(endpoint, data={"query": query}, timeout=timeout,
                                  headers={**UA, "Accept": "text/tab-separated-values"})
                r.raise_for_status()
                text = r.content.decode("utf-8")  # QLever sends no charset; requests would guess latin-1
                if not text.startswith("?"):
                    raise ValueError(f"unexpected response: {text[:200]}")
                tmp = dest.with_suffix(".part")
                tmp.write_text(text)
                tmp.replace(dest)
                break
            except (requests.RequestException, ValueError):
                if attempt == retries:
                    raise
                time.sleep(5 * 2 ** attempt)
        time.sleep(3.0)  # be polite: strictly sequential with a pause
    lines = dest.read_text().split("\n")
    return [[_term(v) for v in ln.split("\t")] for ln in lines[1:] if ln]


def _term(v: str) -> str:
    if v.startswith("<") and v.endswith(">"):
        return v[1:-1]
    if v.startswith('"'):
        end = v.rfind('"')
        s = v[1:end]
        return s.replace("\\t", "\t").replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
    return v


def _qhash(q: str) -> str:
    return hashlib.sha256(q.encode()).hexdigest()[:16]


PFX = """PREFIX osmkey: <https://www.openstreetmap.org/wiki/Key:>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
"""


def _osm_tag_query(k: str, v: str, offset: int) -> str:
    return PFX + f"""SELECT ?x (geof:centroid(?w) AS ?c) ?name ?name_en ?wd WHERE {{
  ?x osmkey:{k} "{v}" .
  ?x geo:hasGeometry/geo:asWKT ?w .
  OPTIONAL {{ ?x osmkey:name ?name }}
  OPTIONAL {{ ?x osmkey:name:en ?name_en }}
  OPTIONAL {{ ?x osmkey:wikidata ?wd }}
}} ORDER BY ?x LIMIT {PAGE} OFFSET {offset}"""


_PT = re.compile(r"POINT\(([-0-9.eE]+) ([-0-9.eE]+)\)")


def _stats(endpoint: str, name: str) -> dict[str, Any]:
    """Index metadata of a QLever endpoint (dataset name = dump version). Retries on 429; falls back to the last
    cached copy only if the endpoint stays unreachable."""
    dest = RAW / f"{name}_stats.json"
    for attempt in range(6):
        try:
            r = requests.get(endpoint, params={"cmd": "stats"}, headers=UA, timeout=60)
            r.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(r.text)
            return r.json()
        except requests.RequestException:
            time.sleep(10 * 2 ** attempt)
    if dest.exists():
        return json.loads(dest.read_text())
    raise RuntimeError(f"{endpoint} stats unavailable")


def osm_stats() -> dict[str, Any]:
    return _stats(QLEVER_OSM, "qlever_osm")


def load_osm_features(stats: dict[str, Any]) -> dict[tuple[str, str], dict[str, np.ndarray | list]]:
    """Planet-wide features per tag: ids, lon, lat, name, name_en, wikidata. Cached per page."""
    snap = re.search(r"planet-(\d{6})\.osm\.pbf", stats["name-index"]).group(1)
    out = {}
    hashes = {}
    for k, v in CULTURE_TAGS + NIGHTLIFE_TAGS:
        rows: list[list[str]] = []
        base = RAW / "qlever" / f"planet-{snap}"
        total = _count(QLEVER_OSM, f'?x osmkey:{k} "{v}" . ?x geo:hasGeometry/geo:asWKT ?w .', PFX,
                       base / f"{k}={v}.count.tsv")
        for off in range(0, total, PAGE):
            q = _osm_tag_query(k, v, off)
            hashes[f"{k}={v}@{off}"] = _qhash(q)
            rows += _sparql_tsv(QLEVER_OSM, q, base / f"{k}={v}.{off:07d}.tsv", expected=min(PAGE, total - off))
        ids, lon, lat, nm, nme, wd = [], [], [], [], [], []
        for row in rows:
            row += [""] * (5 - len(row))
            m = _PT.match(row[1])
            if not m:
                continue  # feature without usable geometry
            ids.append(row[0].replace("https://www.openstreetmap.org/", ""))
            lon.append(float(m.group(1)))
            lat.append(float(m.group(2)))
            nm.append(row[2])
            nme.append(row[3])
            wd.append(row[4].strip())
        # an OSM object may carry e.g. both amenity=bar and amenity=pub? (impossible: one value per key) -> unique
        out[(k, v)] = {"id": ids, "lon": np.array(lon), "lat": np.array(lat), "name": nm, "name_en": nme, "wd": wd}
        print(f"  osm {k}={v}: {len(ids):,} features ({len(rows) - len(ids)} without geometry)")
    record_dataset(
        f"{QLEVER_OSM}#{snap}",
        endpoint=QLEVER_OSM,
        dataset=stats["name-index"],
        osm_base=f"planet-{snap}.osm.pbf",
        server_version=stats.get("version-server"),
        tags=[f"{k}={v}" for k, v in CULTURE_TAGS + NIGHTLIFE_TAGS],
        query_sha256_16=hashes,
        path=str((RAW / "qlever" / f"planet-{snap}").relative_to(CACHE.parents[1])),
        license="ODbL 1.0 (c) OpenStreetMap contributors",
    )
    return out


# --- geometry helpers -----------------------------------------------------------------------------------------
def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^\w]+", " ", s).strip()


def _dist_m(lon1, lat1, lon2, lat2):
    x = np.radians(np.asarray(lon2) - lon1) * math.cos(math.radians(lat1))
    y = np.radians(np.asarray(lat2) - lat1)
    return 6_371_000 * np.hypot(x, y)


class PointIndex:
    """All features of all tags in one STRtree for polygon assignment."""

    def __init__(self, feats: dict[tuple[str, str], dict]):
        self.tag, self.idx, lon, lat = [], [], [], []
        for t, f in feats.items():
            n = len(f["id"])
            self.tag += [t] * n
            self.idx += list(range(n))
            lon.append(f["lon"])
            lat.append(f["lat"])
        self.lon = np.concatenate(lon)
        self.lat = np.concatenate(lat)
        self.tree = shapely.STRtree(shapely.points(self.lon, self.lat))

    def inside(self, geom) -> np.ndarray:
        cand = self.tree.query(geom)
        if len(cand) == 0:
            return cand
        ok = shapely.contains_xy(geom, self.lon[cand], self.lat[cand])
        return cand[ok]


def _dedup_count(items: list[tuple[str, float, float]]) -> int:
    """items: (normalised name, lon, lat). Unnamed items always count; named duplicates within DEDUP_M merge."""
    by_name: dict[str, list[tuple[float, float]]] = defaultdict(list)
    n = 0
    for name, lo, la in items:
        if not name:
            n += 1
        else:
            by_name[name].append((lo, la))
    for pts in by_name.values():
        kept: list[tuple[float, float]] = []
        for lo, la in pts:
            if not any(_dist_m(lo, la, k[0], k[1]) < DEDUP_M for k in kept):
                kept.append((lo, la))
        n += len(kept)
    return n


def city_counts(c: City, feats, pidx: PointIndex) -> dict[str, Any]:
    sel = pidx.inside(c.geom)
    raw = defaultdict(int)
    group_items: dict[str, list] = {g: [] for g in GROUPS}
    tag_group = {t: g for g, ts in GROUPS.items() for t in ts}
    for j in sel:
        t, i = pidx.tag[j], pidx.idx[j]
        raw[f"{t[0]}={t[1]}"] += 1
        f = feats[t]
        group_items[tag_group[t]].append((_norm(f["name"][i]), f["lon"][i], f["lat"][i]))
    res = {"raw_counts": {f"{k}={v}": raw.get(f"{k}={v}", 0) for k, v in CULTURE_TAGS + NIGHTLIFE_TAGS}}
    for g, items in group_items.items():
        res[f"{g}_raw"] = len(items)
        res[f"{g}_dedup"] = _dedup_count(items)
        res[f"{g}_named_share"] = round(sum(1 for x in items if x[0]) / len(items), 3) if items else None
    return res


# --- Wikidata benchmark ---------------------------------------------------------------------------------------
WPFX = """PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
"""


def wd_stats() -> dict[str, Any]:
    return _stats(QLEVER_WD, "qlever_wikidata")


def load_wikidata(stats) -> dict[str, dict]:
    """Global Wikidata items of WD_CLASSES with P625, excluding dissolved/closed ones (P576, P3999)."""
    tag = _qhash(stats["name-index"])
    items: dict[str, dict] = {}
    qh = {}
    for qc, label in WD_CLASSES.items():
        q = WPFX + f"""PREFIX wikibase: <http://wikiba.se/ontology#>
SELECT ?x (SAMPLE(?c) AS ?coord) (SAMPLE(?n) AS ?node) (SAMPLE(?w) AS ?way) (SAMPLE(?r) AS ?rel)
       (MAX(?sl) AS ?sitelinks) (COUNT(?part) AS ?n_part_of)
WHERE {{
  ?x wdt:P31/wdt:P279* wd:{qc} .
  ?x wdt:P625 ?c .
  FILTER NOT EXISTS {{ ?x wdt:P576 ?d }}
  FILTER NOT EXISTS {{ ?x wdt:P3999 ?e }}
  OPTIONAL {{ ?x wdt:P11693 ?n }}
  OPTIONAL {{ ?x wdt:P10689 ?w }}
  OPTIONAL {{ ?x wdt:P402 ?r }}
  OPTIONAL {{ ?x wikibase:sitelinks ?sl }}
  OPTIONAL {{ ?x wdt:P361 ?part . ?part wdt:P31/wdt:P279* wd:{qc} }}
}} GROUP BY ?x"""
        qh[qc] = _qhash(q)
        n = _count(QLEVER_WD, f"?x wdt:P31/wdt:P279* wd:{qc} . ?x wdt:P625 ?c . "
                   "FILTER NOT EXISTS { ?x wdt:P576 ?d } FILTER NOT EXISTS { ?x wdt:P3999 ?e }", WPFX,
                   RAW / "wikidata" / tag / f"{qc}.count.tsv")
        rows = _sparql_tsv(QLEVER_WD, q, RAW / "wikidata" / tag / f"{qc}.{qh[qc]}.tsv", expected=n)
        for row in rows:
            row += [""] * (7 - len(row))
            m = _PT.search(row[1].replace("Point(", "POINT("))
            if not m:
                continue
            qid = row[0].rsplit("/", 1)[-1]
            osm_ids = {p + x for p, x in (("node/", row[2]), ("way/", row[3]), ("relation/", row[4])) if x}
            it = items.setdefault(qid, {"lon": float(m.group(1)), "lat": float(m.group(2)), "classes": set(),
                                        "osm": set()})
            it["classes"].add(label)
            it["osm"] |= osm_ids
            # "notable, stand-alone": has >= 1 Wikimedia sitelink and is not `part of` (P361) another item of the
            # same class (drops e.g. the individual buildings of the Skansen open-air museum, rooms of Versailles)
            it["notable"] = _int(row[5]) >= 1 and _int(row[6]) == 0
        print(f"  wikidata {label}: {len(rows):,} items")
    record_dataset(
        f"{QLEVER_WD}#{tag}",
        endpoint=QLEVER_WD,
        dataset=stats["name-index"],
        classes=WD_CLASSES,
        query_sha256_16=qh,
        path=str((RAW / "wikidata" / tag).relative_to(CACHE.parents[1])),
        license="CC0 1.0 (Wikidata structured data)",
    )
    return items


def _int(v: str) -> int:
    m = re.match(r"-?\d+", v.strip())
    return int(m.group(0)) if m else 0


def wd_labels(qids: list[str], stats) -> dict[str, list[str]]:
    tag = _qhash(stats["name-index"])
    out: dict[str, list[str]] = defaultdict(list)
    qids = sorted(qids)
    for i in range(0, len(qids), 400):
        chunk = qids[i:i + 400]
        q = WPFX + "SELECT ?x ?l WHERE { VALUES ?x { " + " ".join(f"wd:{x}" for x in chunk) + \
            " } { ?x rdfs:label ?l } UNION { ?x <http://www.w3.org/2004/02/skos/core#altLabel> ?l } }"
        rows = _sparql_tsv(QLEVER_WD, q, RAW / "wikidata" / tag / "labels" / f"{_qhash(q)}.tsv")
        for row in rows:
            if len(row) >= 2:
                lab = row[1]
                lab = re.sub(r'"@[\w-]+$', "", lab)
                out[row[0].rsplit("/", 1)[-1]].append(_norm(lab))
    return out


def osm_wikidata_any(qids: list[str], stats) -> set[str]:
    """QIDs referenced by ANY OSM object's wikidata tag (to separate 'not mapped' from 'mapped, other tag')."""
    snap = re.search(r"planet-(\d{6})", stats["name-index"]).group(1)
    found = set()
    qids = sorted(qids)
    for i in range(0, len(qids), 400):
        chunk = qids[i:i + 400]
        q = PFX + "SELECT DISTINCT ?q WHERE { VALUES ?q { " + " ".join(f'"{x}"' for x in chunk) + \
            " } ?o osmkey:wikidata ?q }"
        rows = _sparql_tsv(QLEVER_OSM, q, RAW / "qlever" / f"planet-{snap}" / "wdlinks" / f"{_qhash(q)}.tsv")
        found |= {r[0] for r in rows if r}
    return found


class CultureIndex:
    """All OSM culture features (planet-wide) for Wikidata matching."""

    def __init__(self, feats):
        self.id, self.lon, self.lat, self.names, self.wd = [], [], [], [], {}
        for t in CULTURE_TAGS:
            f = feats[t]
            for i in range(len(f["id"])):
                self.id.append(f["id"][i])
                self.lon.append(f["lon"][i])
                self.lat.append(f["lat"][i])
                self.names.append({x for x in (_norm(f["name"][i]), _norm(f["name_en"][i])) if x})
                for q in re.split(r"[;,]\s*", f["wd"][i]):
                    if q:
                        self.wd.setdefault(q, []).append(len(self.id) - 1)
        self.idset = set(self.id)
        self.lon = np.array(self.lon)
        self.lat = np.array(self.lat)
        self.tree = shapely.STRtree(shapely.points(self.lon, self.lat))

    def match(self, qid: str, it: dict, labels: list[str]) -> str | None:
        if qid in self.wd or (it["osm"] & self.idset):
            return "link"
        lo, la = it["lon"], it["lat"]
        d = MATCH_M / 111_000
        cand = self.tree.query(shapely.box(lo - d / max(math.cos(math.radians(la)), 0.1), la - d,
                                           lo + d / max(math.cos(math.radians(la)), 0.1), la + d))
        if len(cand) == 0:
            return None
        dist = _dist_m(lo, la, self.lon[cand], self.lat[cand])
        labs = [x for x in labels if x]
        for j, dm in zip(cand, dist, strict=True):
            if dm > MATCH_M:
                continue
            for on in self.names[j]:
                for lab in labs:
                    if on == lab or (len(on) > 3 and len(lab) > 3 and (on in lab or lab in on)) or \
                            difflib.SequenceMatcher(None, on, lab).ratio() >= NAME_SIM:
                        return "name"
        return None


# --- Overture benchmark ---------------------------------------------------------------------------------------
def overture_city(c: City) -> list[tuple]:
    """Overture places of the comparable categories in the polygon bbox (cached CSV per city)."""
    dest = RAW / "overture" / OVERTURE_RELEASE / f"uc{c.ucdb_id}.csv"
    if not dest.exists():
        import duckdb

        dest.parent.mkdir(parents=True, exist_ok=True)
        x0, y0, x1, y1 = shapely.bounds(c.geom)
        cats = sorted({x for v in OVERTURE_PAIRS.values() for x in v[0]})
        con = duckdb.connect()
        con.execute("INSTALL httpfs; LOAD httpfs;")
        con.execute("CREATE SECRET (TYPE s3, KEY_ID '', SECRET '', REGION 'us-west-2')")
        tmp = dest.with_suffix(".part")
        for attempt in range(4):
            try:
                con.execute(f"""COPY (SELECT id, basic_category, confidence, operating_status,
                       bbox.xmin AS lon, bbox.ymin AS lat
                     FROM read_parquet('{OVERTURE_URL}')
                     WHERE bbox.xmin BETWEEN {x0} AND {x1} AND bbox.ymin BETWEEN {y0} AND {y1}
                       AND basic_category IN ({",".join(repr(x) for x in cats)}))
                     TO '{tmp}' (HEADER, DELIMITER ',')""")
                tmp.replace(dest)
                break
            except duckdb.Error:  # network errors surface as duckdb IOException
                if attempt == 3:
                    raise
                time.sleep(10 * 2 ** attempt)
    rows = []
    for ln in dest.read_text().splitlines()[1:]:
        p = ln.split(",")
        rows.append((p[1], float(p[2]) if p[2] else 0.0, p[3], float(p[4]), float(p[5])))
    return rows


# --- live OSM API consistency check ---------------------------------------------------------------------------
CHECK_BOXES = {  # small boxes (< 0.25 deg², API limit) in three regions: (min_lon, min_lat, max_lon, max_lat)
    "reykjavik-centre": (-21.95, 64.14, -21.92, 64.15),
    "nairobi-cbd": (36.81, -1.295, 36.83, -1.28),
    "bangkok-silom": (100.52, 13.72, 100.54, 13.735),
}


def api_check(feats) -> dict[str, Any]:
    out = {}
    tags = set(CULTURE_TAGS + NIGHTLIFE_TAGS)
    for name, (x0, y0, x1, y1) in CHECK_BOXES.items():
        url = f"{OSM_API}?bbox={x0},{y0},{x1},{y1}"
        try:
            p = fetch(url, RAW / "api" / f"{name}.osm", headers=UA, timeout=180)
        except requests.RequestException as e:
            out[name] = {"error": str(e)[:200]}
            continue
        root = ET.parse(p).getroot()
        nodes = {n.get("id"): (float(n.get("lon")), float(n.get("lat"))) for n in root.iter("node")}
        live = 0
        for el in list(root.iter("node")) + list(root.iter("way")):
            kv = {(t.get("k"), t.get("v")) for t in el.iter("tag")}
            if not (kv & tags):
                continue
            if el.tag == "node":
                lo, la = nodes[el.get("id")]
            else:
                pts = [nodes[nd.get("ref")] for nd in el.iter("nd") if nd.get("ref") in nodes]
                if not pts:
                    continue
                lo, la = float(np.mean([q[0] for q in pts])), float(np.mean([q[1] for q in pts]))
            live += x0 <= lo <= x1 and y0 <= la <= y1
        snap = 0
        for t in tags:
            f = feats[t]
            m = (f["lon"] >= x0) & (f["lon"] <= x1) & (f["lat"] >= y0) & (f["lat"] <= y1)
            snap += int(m.sum() - sum(1 for i in np.flatnonzero(m) if f["id"][i].startswith("relation/")))
        out[name] = {"live_api_nodes_ways": live, "qlever_snapshot_nodes_ways": snap}
    return out


# --- main -----------------------------------------------------------------------------------------------------
def _region_summary(rows: list[dict], key: str) -> dict[str, dict]:
    by = defaultdict(list)
    for r in rows:
        if r.get(key) is not None:
            by[r["region"]].append(r[key])
    return {g: {"n_cities": len(v), "median": round(median(v), 3), "min": round(min(v), 3),
                "max": round(max(v), 3)} for g, v in sorted(by.items())}


def _spearman(a, b) -> float:
    ra = np.argsort(np.argsort(a))
    rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def _agreement(tgt: list[dict]) -> dict[str, Any]:
    """Does coverage noise swamp the signal? Rank agreement of densities between OSM and the independent sources,
    and the spread of the OSM/Overture ratio (log10 sd) versus the spread of the metric itself."""
    out: dict[str, Any] = {}
    for name, keys in (("culture_core", ("museum", "cinema")), ("nightlife", ("bar_pub", "nightclub"))):
        rs = [r for r in tgt if r["overture"][name]["overture"] > 0 and r["overture"][name]["osm"] > 0]
        osm_d = np.array([r["overture"][name]["osm"] / r["area"] for r in rs])
        ov_d = np.array([r["overture"][name]["overture"] / r["area"] for r in rs])
        ratio = osm_d / ov_d
        out[name] = {
            "n_cities": len(rs),
            "spearman_osm_vs_overture_density": round(_spearman(osm_d, ov_d), 3),
            "log10_sd_osm_density": round(float(np.std(np.log10(osm_d))), 3),
            "log10_sd_overture_density": round(float(np.std(np.log10(ov_d))), 3),
            "log10_sd_ratio": round(float(np.std(np.log10(ratio))), 3),
            "ratio_p10_p50_p90": [round(float(x), 3) for x in np.percentile(ratio, [10, 50, 90])],
            "osm_density_p90_over_p10": round(float(np.percentile(osm_d, 90) / np.percentile(osm_d, 10)), 1),
        }
        if name == "culture_core":
            rw = [(r["culture_dedup"] / r["area"], r["wikidata"]["n_notable"] / r["area"]) for r in tgt
                  if r["wikidata"]["n_notable"] > 0]
            out["culture_osm_vs_wikidata_notable_density_spearman"] = round(
                _spearman(np.array([x[0] for x in rw]), np.array([x[1] for x in rw])), 3)
    return out


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    targets = load_cities()
    refs = reference_centres()
    allc = {c.city_id: c for c in list(refs) + list(targets)}
    target_ids = {c.city_id for c in targets}

    print("OSM features (QLever osm-planet)")
    st = osm_stats()
    snap = re.search(r"planet-(\d{6})", st["name-index"]).group(1)
    year = 2000 + int(snap[:2])
    feats = load_osm_features(st)
    pidx = PointIndex(feats)

    print("Wikidata benchmark")
    wst = wd_stats()
    wd = load_wikidata(wst)
    wq = list(wd)
    wtree = shapely.STRtree(shapely.points([wd[q]["lon"] for q in wq], [wd[q]["lat"] for q in wq]))
    wlon = np.array([wd[q]["lon"] for q in wq])
    wlat = np.array([wd[q]["lat"] for q in wq])

    counts, wd_in = {}, {}
    for c in allc.values():
        counts[c.city_id] = city_counts(c, feats, pidx)
        cand = wtree.query(c.geom)
        ok = shapely.contains_xy(c.geom, wlon[cand], wlat[cand]) if len(cand) else np.array([], bool)
        wd_in[c.city_id] = [wq[j] for j in cand[ok]]
    need = sorted({q for v in wd_in.values() for q in v})
    print(f"  {len(need):,} Wikidata items inside the {len(allc)} polygons; fetching labels / OSM links")
    labels = wd_labels(need, wst)
    anylink = osm_wikidata_any(need, st)
    cidx = CultureIndex(feats)

    rows = []
    for cid, c in allc.items():
        res = counts[cid]
        items = wd_in[cid]
        mt = {q: cidx.match(q, wd[q], labels.get(q, [])) for q in items}
        n = len(items)
        n_link = sum(1 for v in mt.values() if v == "link")
        n_name = sum(1 for v in mt.values() if v == "name")
        n_other = sum(1 for q, v in mt.items() if v is None and q in anylink)
        mus = [q for q in items if "museum" in wd[q]["classes"]]
        nb = [q for q in items if wd[q]["notable"]]
        res["wikidata"] = {
            "n_items": n, "n_museums": len(mus), "n_notable": len(nb),
            "matched_by_wikidata_link": n_link, "matched_by_name_250m": n_name,
            "unmatched_but_linked_from_other_osm_object": n_other,
            "recall_all": round((n_link + n_name) / n, 3) if n else None,
            "recall": round(sum(1 for q in nb if mt[q]) / len(nb), 3) if nb else None,
            "recall_museums": round(sum(1 for q in mus if mt[q]) / len(mus), 3) if mus else None,
            "osm_culture_to_wikidata_ratio": round(res["culture_dedup"] / n, 2) if n else None,
        }
        rows.append({"city_id": cid, "region": c.region, "target": cid in target_ids,
                     "pop": c.pop_2025, "area": c.area_km2, **res})

    print("Overture benchmark (86 targets)")
    for r in rows:
        if not r["target"]:
            continue
        c = allc[r["city_id"]]
        ov = overture_city(c)
        ok = shapely.contains_xy(c.geom, np.array([x[3] for x in ov]), np.array([x[4] for x in ov])) if ov else []
        ov_in = [x for x, k in zip(ov, ok, strict=True) if k and x[2] != "permanently_closed"
                 and x[1] >= OVERTURE_MIN_CONF]
        cmp = {}
        for key, (ocats, otags) in OVERTURE_PAIRS.items():
            n_ov = sum(1 for x in ov_in if x[0] in ocats)
            n_osm = sum(r["raw_counts"][f"{k}={v}"] for k, v in otags)
            cmp[key] = {"osm": n_osm, "overture": n_ov, "ratio": round(n_osm / n_ov, 3) if n_ov else None}
        r["overture"] = cmp
        print(f"  {r['city_id']:16} museum {cmp['museum']}  bar {cmp['bar_pub']['ratio']}")
    record_dataset(
        f"{OVERTURE_URL}",
        release=OVERTURE_RELEASE,
        categories={k: v[0] for k, v in OVERTURE_PAIRS.items()},
        filter=f"bbox of each target polygon, then point-in-polygon; confidence >= {OVERTURE_MIN_CONF}; "
               "operating_status != permanently_closed",
        path=str((RAW / "overture" / OVERTURE_RELEASE).relative_to(CACHE.parents[1])),
        license="Places theme: CDLA-Permissive-2.0 (Meta, Microsoft, ...), Apache-2.0 (Foursquare), CC0 "
                "(AllThePlaces); https://docs.overturemaps.org/attribution/",
    )

    print("OSM API consistency check")
    chk = api_check(feats)
    print("  ", chk)

    # --- summaries & output ----------------------------------------------------------------------------------
    for r in rows:
        w = r["wikidata"]
        r["wd_recall"] = w["recall"] if w["n_notable"] >= 5 else None
        r["wd_recall_all"] = w["recall_all"] if w["n_items"] >= 5 else None
        r["wd_recall_museums"] = w["recall_museums"] if w["n_museums"] >= 5 else None
        if "overture" in r:
            for k in OVERTURE_PAIRS:
                r[f"ov_{k}"] = r["overture"][k]["ratio"] if r["overture"][k]["overture"] >= 10 else None
            for name, keys in (("culture_core", ("museum", "cinema")),
                               ("nightlife", ("bar_pub", "nightclub"))):
                a = sum(r["overture"][k]["osm"] for k in keys)
                b = sum(r["overture"][k]["overture"] for k in keys)
                r["overture"][name] = {"osm": a, "overture": b, "ratio": round(a / b, 3) if b else None}
                r[f"ov_{name}"] = r["overture"][name]["ratio"] if b >= 10 else None
    tgt = [r for r in rows if r["target"]]
    summary = {
        "wikidata_recall_reference_524": _region_summary(rows, "wd_recall"),
        "wikidata_recall_targets_86": _region_summary(tgt, "wd_recall"),
        "wikidata_recall_all_items_reference_524": _region_summary(rows, "wd_recall_all"),
        "wikidata_museum_recall_reference_524": _region_summary(rows, "wd_recall_museums"),
        **{f"osm_over_overture_{k}_targets_86": _region_summary(tgt, f"ov_{k}") for k in OVERTURE_PAIRS},
        "osm_over_overture_culture_core_targets_86": _region_summary(tgt, "ov_culture_core"),
        "osm_over_overture_nightlife_targets_86": _region_summary(tgt, "ov_nightlife"),
        "agreement_targets_86": _agreement(tgt),
        "api_consistency": chk,
    }
    (RAW / "validation_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    REFERENCE.mkdir(parents=True, exist_ok=True)
    with (REFERENCE / f"{SOURCE_ID}.csv").open("w") as f:
        f.write("city_id,region,pop_2025,area_km2,culture_dedup,nightlife_dedup,culture_per_km2,"
                "nightlife_per_km2,culture_per_100k,nightlife_per_100k,wd_items,wd_notable,wd_recall_notable\n")
        for r in sorted(rows, key=lambda r: r["city_id"]):
            f.write(f"{r['city_id']},\"{r['region']}\",{r['pop']:.0f},{r['area']:.1f},{r['culture_dedup']},"
                    f"{r['nightlife_dedup']},{r['culture_dedup'] / r['area']:.4f},"
                    f"{r['nightlife_dedup'] / r['area']:.4f},{r['culture_dedup'] / r['pop'] * 1e5:.3f},"
                    f"{r['nightlife_dedup'] / r['pop'] * 1e5:.3f},{r['wikidata']['n_items']},{r['wikidata']['n_notable']},"
                    f"{'' if r['wikidata']['recall'] is None else r['wikidata']['recall']}\n")

    out = Interim(source_id=SOURCE_ID, inputs=[f"{QLEVER_OSM}#{snap}", f"{QLEVER_WD}#{_qhash(wst['name-index'])}",
                                                OVERTURE_URL])
    out.notes = [
        (f"OSM snapshot planet-{snap}.osm.pbf via QLever osm-planet (osm2rdf). (c) OpenStreetMap contributors, "
         "ODbL 1.0, https://www.openstreetmap.org/copyright. Values are a Produced Work (ODbL 4.3)."),
        ("culture = tourism=museum|gallery, amenity=theatre|arts_centre|cinema|music_venue|concert_hall; "
         "nightlife = amenity=nightclub|bar|pub. Counts de-duplicated (same group, same name, <150 m)."),
        ("quality=estimated: OSM POI completeness varies by city and region (OSM/Overture ratio p10-p90 spans ~3-5x); "
         "see detail.coverage_flag and etl/notes/osm.md before using."),
        ("Recommendation: culture_venues_per_km2 usable (estimated); nightlife_* NOT recommended for ranking - OSM "
         "bar/club coverage is regionally biased (OSM/Overture median Europe ~0.6 vs E/SE Asia ~0.25)."),
    ]
    ov_key = {"culture": "culture_core", "nightlife": "nightlife"}
    med_ratio = {g: median(r[f"ov_{k}"] for r in tgt if r.get(f"ov_{k}") is not None) for g, k in ov_key.items()}
    flags: dict[str, dict[str, list[str]]] = {g: defaultdict(list) for g in GROUPS}
    for r in tgt:
        cid = r["city_id"]
        cov = {"wikidata": r["wikidata"], "overture": r["overture"]}
        for g, tags in GROUPS.items():
            o = r["overture"][ov_key[g]]
            if o["overture"] < 10:
                flag = "unverified_overture_sparse"
            elif o["ratio"] < med_ratio[g] / 2:
                flag = "osm_low_vs_overture"  # OSM likely undercounts >= 2x relative to the typical target city
            elif o["ratio"] > med_ratio[g] * 2:
                flag = "overture_low_vs_osm"  # Overture sparse here (e.g. Meta absent); OSM not contradicted
            else:
                flag = "ok"
            flags[g][flag].append(cid)
            det = {"count_dedup": r[f"{g}_dedup"], "count_raw": r[f"{g}_raw"],
                   "named_share": r[f"{g}_named_share"],
                   "raw_counts": {k: v for k, v in r["raw_counts"].items() if tuple(k.split("=")) in tags},
                   "area_km2": round(r["area"], 2), "pop_2025": round(r["pop"]),
                   "osm_snapshot": f"planet-{snap}",
                   "coverage_flag": flag,
                   "osm_over_overture": o["ratio"], "median_osm_over_overture_86": round(med_ratio[g], 3),
                   "overture_density_per_km2": round(o["overture"] / r["area"], 4),
                   "coverage": cov}
            out.put(f"{g}_venues_per_km2", cid, r[f"{g}_dedup"] / r["area"], quality="estimated", year=year,
                    detail=det)
            out.put(f"{g}_venues_per_100k", cid, r[f"{g}_dedup"] / r["pop"] * 1e5, quality="estimated",
                    year=year, detail={"count_dedup": r[f"{g}_dedup"], "pop_2025": round(r["pop"])})
    summary["coverage_flags_targets_86"] = {g: {k: sorted(v) for k, v in f.items()} for g, f in flags.items()}
    (RAW / "validation_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    p = out.write()
    print(f"wrote {p}")
    print(json.dumps(summary["coverage_flags_targets_86"], indent=1))
    print(json.dumps({k: v for k, v in summary.items() if "targets" in k or "reference" in k}, indent=1))


if __name__ == "__main__":
    main()
