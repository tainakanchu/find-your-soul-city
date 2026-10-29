"""City "chronotype" from OSM `opening_hours`: how late / early / on Sundays shops and eateries are open.

Pipeline (inputs cached under .cache/raw/osm/qlever/planet-<snap>/hours/):
1. Every feature with shop=supermarket|convenience or amenity=restaurant|cafe|fast_food is pulled planet-wide from
   the QLever osm-planet SPARQL endpoint (same access route, snapshot, paging and COUNT-based truncation check as
   `osm.py`), with centroid, `opening_hours`, `brand`, `brand:wikidata` and `name`. Points are assigned to the
   GHS-UCDB polygons locally (shapely).
2. `opening_hours` is evaluated by `parse_oh()` below (own parser for the documented syntax subset, see notes) on a
   fixed reference week (Mon 2026-10-05 .. Sun 2026-10-11) with public/school-holiday rules ignored.
3. Metrics: among POIs whose tag parses, share open at Wed 23:00, Wed 07:00, Sun 12:00, any time Sunday,
   and 24/7. Chain (brand/brand:wikidata) vs non-chain strata; the published value is post-stratified so that the
   chain share equals the chain share among ALL POIs of the group (tagged or not) in that city.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from collections import Counter, defaultdict
from statistics import median
from typing import Any

import numpy as np
import shapely

from .cities import load_cities, reference_centres
from .common import CACHE, REFERENCE, Interim, record_dataset
from .osm import _PT, PFX, QLEVER_OSM, RAW, _count, _qhash, _sparql_tsv_once, _term, osm_stats

SOURCE_ID = "osm-hours"
PAGE = 50_000
TAGS: list[tuple[str, str]] = [("shop", "supermarket"), ("shop", "convenience"), ("amenity", "restaurant"),
                               ("amenity", "cafe"), ("amenity", "fast_food")]
GROUPS: dict[str, list[tuple[str, str]]] = {
    "groceries": [("shop", "supermarket"), ("shop", "convenience")],
    "supermarket": [("shop", "supermarket")],
    "convenience": [("shop", "convenience")],
    "eating": [("amenity", "restaurant"), ("amenity", "cafe"), ("amenity", "fast_food")],
    "restaurant": [("amenity", "restaurant")],
}
# Published metrics: (group, check) -> metric key
CHECKS = ("late23", "late22", "early07", "sun12", "sun_any", "h24", "fri12", "sat12")
PUBLISH = {
    ("groceries", "late23"): "grocery_late_open_share",
    ("groceries", "early07"): "grocery_early_open_share",
    ("groceries", "sun12"): "grocery_sunday_open_share",
    ("groceries", "h24"): "grocery_24h_share",
    ("supermarket", "late23"): "supermarket_late_open_share",
    ("supermarket", "sun12"): "supermarket_sunday_open_share",
    ("eating", "late23"): "eating_late_open_share",
    ("eating", "early07"): "eating_early_open_share",
    ("eating", "h24"): "eating_24h_share",
}
MIN_PARSED = 50        # parsed opening_hours per group per city
MIN_COVERAGE = 0.05    # tagged / all POIs of the group
LOW_COVERAGE = 0.15    # below this the value is flagged coverage_flag="low"
MIN_STRATUM = 10       # parsed POIs per chain stratum for post-stratification
REF_MONDAY = dt.date(2026, 10, 5)  # reference week Mo 2026-10-05 .. Su 2026-10-11 (ISO week 41)

# =============================================================================================================
# opening_hours parser (subset of https://wiki.openstreetmap.org/wiki/Key:opening_hours/specification)
# =============================================================================================================
DAYS = ["mo", "tu", "we", "th", "fr", "sa", "su"]
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
_TOK = re.compile(r"""\s*(?:
    (?P<str>"[^"]*")|
    (?P<t247>24/7)|
    (?P<time>\d{1,2}:\d{2})|
    (?P<num>\d+)|
    (?P<word>[A-Za-z]+)|
    (?P<op>\|\||[-;,:\[\]+/()])
)""", re.VERBOSE)
DAY_MIN = 1440


class OHError(ValueError):
    """Tag cannot be evaluated; `code` is a short category for the unparseable statistics."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _tokens(s: str) -> list[tuple[str, str]]:
    s = s.replace("–", "-").replace("—", "-").replace("−", "-").replace("：", ":")
    out, i = [], 0
    while i < len(s):
        if s[i:].strip() == "":
            break
        m = _TOK.match(s, i)
        if not m or m.end() == i:
            raise OHError("bad_char")
        kind = m.lastgroup
        val = m.group(kind)
        if kind == "word":
            w = val.lower()
            if w in DAYS:
                kind = "wd"
            elif w in MONTHS:
                kind = "mon"
            elif val in ("PH", "SH"):
                kind = "hol"
            elif w in ("off", "closed", "open", "unknown"):
                kind = "mod"
            elif w == "week":
                kind = "week"
            elif w in ("sunrise", "sunset", "dawn", "dusk"):
                raise OHError("event_time")
            elif w == "easter":
                kind = "easter"
            elif w in ("day", "days"):
                kind = "dayword"
            else:
                raise OHError("unknown_word")
            val = w if kind != "hol" else val
        out.append((kind, val))
        i = m.end()
    return out


class _P:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self, k=0):
        j = self.i + k
        return self.t[j] if j < len(self.t) else ("eof", "")

    def take(self, kind=None, val=None):
        tk = self.peek()
        if (kind and tk[0] != kind) or (val and tk[1] != val):
            raise OHError("syntax")
        self.i += 1
        return tk


def _time(v: str) -> int:
    h, m = v.split(":")
    h, m = int(h), int(m)
    if m >= 60 or h > 48:
        raise OHError("bad_time")
    return h * 60 + m


def _parse_rule(p: _P) -> dict[str, Any]:
    r: dict[str, Any] = {"years": None, "dates": None, "weeks": None, "wdays": None, "hol": False, "nth": False,
                         "times": None, "mod": "open", "comment": False, "any_selector": False}
    if p.peek()[0] == "t247":
        p.take()
        r["times"] = [(0, DAY_MIN)]
    # --- wide range selectors: year / month / monthday / week (any order, tolerant) -------------------------
    while True:
        k, v = p.peek()
        if k == "num" and len(v) == 4 and p.peek(1)[0] != "mon":
            r["years"] = r["years"] or []
            while True:
                y1 = int(p.take("num")[1])
                y2 = y1
                if p.peek()[0] == "op" and p.peek()[1] == "-" and p.peek(1)[0] == "num":
                    p.take()
                    y2 = int(p.take("num")[1])
                if p.peek()[0] == "op" and p.peek()[1] == "/":
                    raise OHError("year_period")
                r["years"].append((y1, y2))
                if p.peek() == ("op", ",") and p.peek(1)[0] == "num" and len(p.peek(1)[1]) == 4:
                    p.take()
                    continue
                break
        elif k == "mon" or (k == "num" and len(v) == 4 and p.peek(1)[0] == "mon"):
            r["dates"] = r["dates"] or []
            while True:
                a = _monthday(p)
                b = None
                if p.peek() == ("op", "-"):
                    p.take()
                    if p.peek()[0] == "num" and len(p.peek()[1]) <= 2 and a[2] is not None:
                        b = (a[0], a[1], int(p.take()[1]))
                    else:
                        b = _monthday(p)
                r["dates"].append((a, b))
                while p.peek() == ("op", ",") and p.peek(1)[0] == "num" and len(p.peek(1)[1]) <= 2 \
                        and a[2] is not None:
                    # "Dec 25,26" -> another day of the same month
                    p.take()
                    r["dates"].append(((a[0], a[1], int(p.take("num")[1])), None))
                if p.peek() == ("op", ",") and (p.peek(1)[0] == "mon" or
                                                 (p.peek(1)[0] == "num" and len(p.peek(1)[1]) == 4)):
                    p.take()
                    continue
                break
        elif k == "easter":
            # easter [+-n day(s)] [- easter [+-n day(s)]]: never inside the October reference week
            p.take()
            _offset(p)
            if p.peek() == ("op", "-") and p.peek(1)[0] == "easter":
                p.take()
                p.take()
                _offset(p)
            r["never"] = True
            while p.peek() == ("op", ",") and p.peek(1)[0] in ("mon", "easter"):
                p.take()
                if p.peek()[0] == "easter":
                    p.take()
                    _offset(p)
                else:
                    a = _monthday(p)
                    r["dates"] = (r["dates"] or []) + [(a, None)]
        elif k == "week":
            p.take()
            r["weeks"] = []
            while True:
                w1 = int(p.take("num")[1])
                w2, step = w1, 1
                if p.peek() == ("op", "-"):
                    p.take()
                    w2 = int(p.take("num")[1])
                if p.peek() == ("op", "/"):
                    p.take()
                    step = int(p.take("num")[1])
                r["weeks"].append((w1, w2, step))
                if p.peek() == ("op", ",") and p.peek(1)[0] == "num":
                    p.take()
                    continue
                break
        else:
            break
        r["any_selector"] = True
    # --- weekday / holiday selector ---------------------------------------------------------------------------
    if r["any_selector"] and p.peek() == ("op", ":") and p.peek(1)[0] in ("wd", "hol"):
        p.take()  # "Sep-Jun: Mo-Fr ..."
    if p.peek()[0] in ("wd", "hol"):
        r["any_selector"] = True
        days: set[int] = set()
        n_days_tokens = 0
        while True:
            k, v = p.peek()
            if k == "hol":
                p.take()
                r["hol"] = True
                if _offset(p):
                    r["hol_offset"] = True  # "PH -1 day": a day adjacent to a holiday -> treated like PH
            elif k == "wd":
                p.take()
                n_days_tokens += 1
                d1 = DAYS.index(v)
                d2 = d1
                if p.peek() == ("op", "-") and p.peek(1)[0] == "wd":
                    p.take()
                    d2 = DAYS.index(p.take("wd")[1])
                if p.peek() == ("op", "["):
                    r["nth"] = True
                    while p.peek()[0] != "eof" and p.peek() != ("op", "]"):
                        p.take()
                    p.take("op", "]")
                    if p.peek() in (("op", "+"), ("op", "-")) and p.peek(1)[0] == "num":
                        raise OHError("weekday_offset")
                d = d1
                while True:
                    days.add(d)
                    if d == d2:
                        break
                    d = (d + 1) % 7
            else:
                raise OHError("syntax")
            if p.peek() == ("op", ",") and p.peek(1)[0] in ("wd", "hol"):
                p.take()
                continue
            break
        r["wdays"] = days if n_days_tokens else None
        if n_days_tokens == 0:
            r["hol_only"] = True
    if p.peek() == ("op", ":") and r["any_selector"]:
        p.take()
    # --- time selector --------------------------------------------------------------------------------------
    if p.peek()[0] == "time":
        r["times"] = []
        while True:
            a = _time(p.take("time")[1])
            if p.peek() == ("op", "-") and p.peek(1)[0] == "time":
                p.take()
                b = _time(p.take("time")[1])
                if p.peek() == ("op", "/"):
                    raise OHError("periodic_time")
                if p.peek() == ("op", "+"):
                    raise OHError("open_end")
                if b <= a:
                    b += DAY_MIN  # past midnight (also 00:00-00:00 -> 24 h)
                r["times"].append((a, b))
            elif p.peek() == ("op", "+"):
                raise OHError("open_end")
            else:
                raise OHError("point_in_time")
            if p.peek() == ("op", ",") and p.peek(1)[0] == "time":
                p.take()
                continue
            if p.peek()[0] == "time":  # tolerate a missing comma between time ranges
                continue
            break
    elif p.peek()[0] == "op" and p.peek()[1] == "(":
        raise OHError("event_time")
    if p.peek()[0] == "mod":
        r["mod"] = p.take()[1]
    if p.peek()[0] == "str":
        p.take()
        r["comment"] = True
    return r


def _offset(p: _P) -> bool:
    """Consume an optional '+n day(s)' / '-n day(s)' offset."""
    if p.peek() in (("op", "+"), ("op", "-")) and p.peek(1)[0] == "num" and p.peek(2)[0] == "dayword":
        p.take()
        p.take()
        p.take()
        return True
    return False


def _monthday(p: _P) -> tuple[int | None, int, int | None]:
    y = None
    if p.peek()[0] == "num" and len(p.peek()[1]) == 4:
        y = int(p.take()[1])
    m = MONTHS.index(p.take("mon")[1]) + 1
    d = None
    if p.peek()[0] == "num" and len(p.peek()[1]) <= 2 and p.peek(1) != ("op", ":"):
        d = int(p.take()[1])
        if not 1 <= d <= 31:
            raise OHError("bad_date")
    return (y, m, d)


def _split_rules(s: str) -> list[tuple[str, dict]]:
    """Parse the whole tag into (separator, rule) pairs; separator of the first rule is ';'."""
    p = _P(_tokens(s))
    rules: list[tuple[str, dict]] = []
    sep = ";"
    while True:
        if p.peek()[0] == "eof":
            break
        if p.peek() == ("op", ";"):  # empty rule (e.g. trailing ';')
            p.take()
            sep = ";"
            continue
        start = p.i
        r = _parse_rule(p)
        if p.i == start:
            raise OHError("syntax")
        rules.append((sep, r))
        k, v = p.peek()
        if k == "eof":
            break
        if (k, v) == ("op", ";"):
            sep = ";"
        elif (k, v) == ("op", ","):
            sep = ","
        elif (k, v) == ("op", "||"):
            sep = "||"
        else:
            raise OHError("syntax")
        p.take()
    if not rules:
        raise OHError("empty")
    return rules


def _date_match(r: dict, d: dt.date) -> bool:
    if r.get("never") and not r["dates"]:
        return False
    if r["years"] is not None and not any(a <= d.year <= b for a, b in r["years"]):
        return False
    if r["weeks"] is not None:
        wk = d.isocalendar().week
        if not any(a <= wk <= b and (wk - a) % s == 0 for a, b, s in r["weeks"]):
            return False
    if r["dates"] is not None and not any(_md_match(a, b, d) for a, b in r["dates"]):
        return False
    return not (r["wdays"] is not None and d.weekday() not in r["wdays"])


def _md_match(a, b, d: dt.date) -> bool:
    ya, ma, da = a
    if b is None:
        if ya is not None and ya != d.year:
            return False
        return d.month == ma and (da is None or d.day == da)
    yb, mb, db = b
    lo = (ma, da if da is not None else 1)
    hi = (mb, db if db is not None else 31)
    if ya is not None and yb is not None:
        return dt.date(ya, *lo) <= d <= dt.date(yb, hi[0], min(hi[1], 28 if hi[0] == 2 else 30 if hi[0] in (
            4, 6, 9, 11) else 31))
    x = (d.month, d.day)
    return lo <= x <= hi if lo <= hi else (x >= lo or x <= hi)


def _subtract(iv: list[tuple[int, int]], cut: list[tuple[int, int]]) -> list[tuple[int, int]]:
    out = list(iv)
    for c0, c1 in cut:
        nxt = []
        for a, b in out:
            if c1 <= a or c0 >= b:
                nxt.append((a, b))
                continue
            if a < c0:
                nxt.append((a, c0))
            if c1 < b:
                nxt.append((c1, b))
        out = nxt
    return out


def parse_oh(s: str) -> dict[str, Any]:
    """Evaluate an opening_hours value on the reference week.

    Returns {"own": [intervals per weekday 0=Mo..6=Su, minutes, end may exceed 1440 (past midnight)],
             "flags": set of notes ("holiday_rule_ignored", "nth_weekday_ignored", ...)}.
    Raises OHError if the value is outside the supported subset or ambiguous ("unknown" state)."""
    rules = _split_rules(s.strip())
    week = [REF_MONDAY + dt.timedelta(days=i) for i in range(7)]
    own: list[list[tuple[int, int]] | None] = [None] * 7
    flags: set[str] = set()
    n_weekly = 0
    for sep, r in rules:
        if r.get("hol_only"):
            flags.add("holiday_rule_ignored")
            continue
        if r["hol"]:
            flags.add("holiday_rule_ignored")
        if r["nth"]:
            flags.add("nth_weekday_ignored")
            continue
        if r["mod"] == "unknown" or (r["comment"] and r["times"] is None and r["mod"] == "open"):
            if sep == "||":
                flags.add("comment_fallback_ignored")
                continue
            raise OHError("unknown_state")
        n_weekly += 1
        days = [i for i, d in enumerate(week) if _date_match(r, d)]
        if r["any_selector"] and not days:
            flags.add("rule_outside_reference_week")
        iv = r["times"] if r["times"] is not None else [(0, DAY_MIN)]
        closed = r["mod"] in ("off", "closed")
        for i in days:
            if sep == "||":
                if own[i] is not None:
                    continue
                own[i] = [] if closed else list(iv)
            elif closed:
                own[i] = [] if r["times"] is None or own[i] is None else _subtract(own[i], iv)
            elif sep == "," and own[i] is not None:
                own[i] = own[i] + list(iv)
            else:
                own[i] = list(iv)
    if n_weekly == 0:
        raise OHError("no_normal_week_rule")  # e.g. only "PH off" or only Su[1] rules
    return {"own": [x or [] for x in own], "flags": flags}


def is_open(sched: dict, day: int, minute: int) -> bool:
    own = sched["own"]
    if any(a <= minute < b for a, b in own[day]):
        return True
    return any(a <= minute + DAY_MIN < b for a, b in own[(day - 1) % 7])


def open_any(sched: dict, day: int, lo: int = 0, hi: int = DAY_MIN, *, spill: bool = False) -> bool:
    """Any opening inside [lo, hi) of `day` from that day's own rules (spill-over from the previous night only if
    `spill`)."""
    own = sched["own"]
    if any(a < hi and b > lo for a, b in own[day]):
        return True
    return spill and any(a - DAY_MIN < hi and b - DAY_MIN > lo for a, b in own[(day - 1) % 7])


def is_24_7(sched: dict) -> bool:
    own = sched["own"]
    for d in range(7):
        segs = [(max(a, 0), min(b, DAY_MIN)) for a, b in own[d]]
        segs += [(max(a - DAY_MIN, 0), min(b - DAY_MIN, DAY_MIN)) for a, b in own[(d - 1) % 7] if b > DAY_MIN]
        segs = sorted(x for x in segs if x[1] > x[0])
        cur = 0
        for a, b in segs:
            if a > cur:
                return False
            cur = max(cur, b)
        if cur < DAY_MIN:
            return False
    return True


def evaluate(s: str) -> dict[str, bool] | str:
    """Checks for one tag value, or the unparseable category."""
    try:
        sc = parse_oh(s)
    except OHError as e:
        return e.code
    except (ValueError, IndexError):
        return "syntax"
    return {
        "late23": is_open(sc, 2, 23 * 60),
        "late22": is_open(sc, 2, 22 * 60),
        "early07": is_open(sc, 2, 7 * 60),
        "sun12": is_open(sc, 6, 12 * 60),
        "sun_any": open_any(sc, 6, 6 * 60, 22 * 60),
        "h24": is_24_7(sc),
        "fri12": is_open(sc, 4, 12 * 60),  # weekly rest day differs (Fri: much of MENA, Sat: Israel)
        "sat12": is_open(sc, 5, 12 * 60),
        "holiday_rule": "holiday_rule_ignored" in sc["flags"],
    }


# =============================================================================================================
# data
# =============================================================================================================
def _query(k: str, v: str, offset: int) -> str:
    return PFX + f"""SELECT ?x (geof:centroid(?w) AS ?c) ?oh ?brand ?bwd ?name WHERE {{
  ?x osmkey:{k} "{v}" .
  ?x geo:hasGeometry/geo:asWKT ?w .
  OPTIONAL {{ ?x osmkey:opening_hours ?oh }}
  OPTIONAL {{ ?x osmkey:brand ?brand }}
  OPTIONAL {{ ?x <https://www.openstreetmap.org/wiki/Key:brand:wikidata> ?bwd }}
  OPTIONAL {{ ?x osmkey:name ?name }}
}} ORDER BY ?x LIMIT {PAGE} OFFSET {offset}"""


def _tsv_rows(dest) -> list[list[str]]:
    """Parse a cached QLever TSV splitting on '\\n' only: some OSM values contain a raw carriage return, which
    universal-newline reading (Path.read_text) would turn into an extra line."""
    with open(dest, encoding="utf-8", newline="") as f:
        lines = f.read().split("\n")
    return [[_term(x) for x in ln.split("\t")] for ln in lines[1:] if ln]


def _page(q: str, dest, expected: int) -> list[list[str]]:
    """One page; HTTP errors are not retried (external-access policy: stop on distress). A row-count mismatch
    against the COUNT query (silent truncation, seen in osm.py) discards the cache file and fetches once more."""
    for attempt in range(2):
        _sparql_tsv_once(QLEVER_OSM, q, dest, retries=0)
        rows = _tsv_rows(dest)
        if len(rows) == expected:
            return rows
        print(f"    {dest.name}: {len(rows)} rows, expected {expected}")
        dest.unlink()
    raise RuntimeError(f"{dest}: incomplete result twice; stopping")


def load_features(stats: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    snap = re.search(r"planet-(\d{6})\.osm\.pbf", stats["name-index"]).group(1)
    base = RAW / "qlever" / f"planet-{snap}"
    out, hashes, totals = {}, {}, {}
    for k, v in TAGS:
        total = _count(QLEVER_OSM, f'?x osmkey:{k} "{v}" . ?x geo:hasGeometry/geo:asWKT ?w .', PFX,
                       base / f"{k}={v}.count.tsv")
        totals[f"{k}={v}"] = total
        ids, lon, lat, oh, chain, name = [], [], [], [], [], []
        for off in range(0, total, PAGE):
            q = _query(k, v, off)
            hashes[f"{k}={v}@{off}"] = _qhash(q)
            rows = _page(q, base / "hours" / f"{k}={v}.{off:07d}.tsv", min(PAGE, total - off))
            for row in rows:
                row += [""] * (6 - len(row))
                m = _PT.match(row[1])
                if not m:
                    continue
                ids.append(row[0].replace("https://www.openstreetmap.org/", ""))
                lon.append(float(m.group(1)))
                lat.append(float(m.group(2)))
                oh.append(row[2])
                chain.append(bool(row[3].strip() or row[4].strip()))
                name.append(row[5])
            print(f"  {k}={v} @{off}: {len(ids):,}/{total:,}", flush=True)
        out[(k, v)] = {"id": ids, "lon": np.array(lon), "lat": np.array(lat), "oh": oh,
                       "chain": np.array(chain, bool), "name": name}
    record_dataset(
        f"{QLEVER_OSM}#{snap}#opening_hours",
        endpoint=QLEVER_OSM,
        dataset=stats["name-index"],
        osm_base=f"planet-{snap}.osm.pbf",
        server_version=stats.get("version-server"),
        tags=[f"{k}={v}" for k, v in TAGS],
        keys=["opening_hours", "brand", "brand:wikidata", "name"],
        feature_counts=totals,
        query_sha256_16=hashes,
        path=str((base / "hours").relative_to(CACHE.parents[1])),
        license="ODbL 1.0 (c) OpenStreetMap contributors",
    )
    return out


def _norm_name(s: str) -> str:
    return re.sub(r"\W+", " ", s.lower()).strip()


# =============================================================================================================
# aggregation
# =============================================================================================================
def _share(xs: list[dict], key: str) -> float | None:
    return sum(1 for x in xs if x[key]) / len(xs) if xs else None


def group_stats(pois: list[dict]) -> dict[str, Any]:
    """pois: dicts with keys chain (bool), chain_name (bool), tagged (bool), ev (dict | str | None)."""
    n = len(pois)
    tagged = [p for p in pois if p["tagged"]]
    parsed = [p["ev"] | {"chain": p["chain"]} for p in tagged if isinstance(p["ev"], dict)]
    unp = Counter(p["ev"] for p in tagged if isinstance(p["ev"], str))
    n_chain = sum(p["chain"] for p in pois)
    res: dict[str, Any] = {
        "n_all": n, "n_tagged": len(tagged), "n_parsed": len(parsed), "n_unparseable": sum(unp.values()),
        "unparseable_by_reason": dict(unp.most_common()),
        "coverage": round(len(tagged) / n, 4) if n else None,
        "parse_rate": round(len(parsed) / len(tagged), 4) if tagged else None,
        "chain_share_all": round(n_chain / n, 4) if n else None,
        "chain_share_parsed": round(sum(p["chain"] for p in parsed) / len(parsed), 4) if parsed else None,
        "coverage_chain": round(sum(p["chain"] for p in tagged) / n_chain, 4) if n_chain else None,
        "coverage_nonchain": round(sum(not p["chain"] for p in tagged) / (n - n_chain), 4) if n - n_chain else None,
        "chain_name_share_all": round(sum(p["chain_name"] for p in pois) / n, 4) if n else None,
        "holiday_rule_share": round(_share(parsed, "holiday_rule"), 4) if parsed else None,
    }
    ch = [p for p in parsed if p["chain"]]
    nc = [p for p in parsed if not p["chain"]]
    res["n_parsed_chain"], res["n_parsed_nonchain"] = len(ch), len(nc)
    w = n_chain / n if n else 0.0
    for c in CHECKS:
        raw = _share(parsed, c)
        sc, sn = _share(ch, c), _share(nc, c)
        res[f"{c}_raw"] = None if raw is None else round(100 * raw, 2)
        res[f"{c}_chain"] = None if sc is None else round(100 * sc, 2)
        res[f"{c}_nonchain"] = None if sn is None else round(100 * sn, 2)
        if len(ch) >= MIN_STRATUM and len(nc) >= MIN_STRATUM:
            res[f"{c}_post"] = round(100 * (w * sc + (1 - w) * sn), 2)
        elif len(nc) >= MIN_STRATUM and w < 0.05:
            res[f"{c}_post"] = round(100 * sn, 2)  # chains negligible: the non-chain rate is the city rate
        elif len(ch) >= MIN_STRATUM and w > 0.95:
            res[f"{c}_post"] = round(100 * sc, 2)
        else:
            res[f"{c}_post"] = None
    return res


def city_pois(feats, sel_by_tag: dict[tuple[str, str], np.ndarray], evcache: dict[str, Any]) -> dict[str, list]:
    out: dict[str, list] = {}
    per_tag: dict[tuple[str, str], list] = {}
    for t, idx in sel_by_tag.items():
        f = feats[t]
        lst = []
        names = Counter(_norm_name(f["name"][i]) for i in idx if f["name"][i])
        for i in idx:
            s = f["oh"][i]
            ev = None
            if s:
                ev = evcache.get(s)
                if ev is None:
                    ev = evcache[s] = evaluate(s)
            nm = _norm_name(f["name"][i]) if f["name"][i] else ""
            lst.append({"chain": bool(f["chain"][i]), "tagged": bool(s), "ev": ev,
                        "chain_name": bool(f["chain"][i]) or (bool(nm) and names[nm] >= 5)})
        per_tag[t] = lst
    for g, ts in GROUPS.items():
        out[g] = [p for t in ts for p in per_tag[t]]
    return out


def _region_summary(rows: list[dict], fn) -> dict[str, dict]:
    by = defaultdict(list)
    for r in rows:
        v = fn(r)
        if v is not None:
            by[r["region"]].append(v)
    return {g: {"n": len(v), "median": round(median(v), 3), "min": round(min(v), 3), "max": round(max(v), 3)}
            for g, v in sorted(by.items())}


def _spearman(a, b) -> float | None:
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 5:
        return None
    ra = np.argsort(np.argsort(a))
    rb = np.argsort(np.argsort(b))
    return round(float(np.corrcoef(ra, rb)[0, 1]), 3)


def main() -> None:
    targets = load_cities()
    refs = reference_centres()
    allc = {c.city_id: c for c in list(refs) + list(targets)}
    target_ids = {c.city_id for c in targets}

    print("OSM shops/eateries with opening_hours (QLever osm-planet)")
    st = osm_stats()
    snap = re.search(r"planet-(\d{6})", st["name-index"]).group(1)
    year = 2000 + int(snap[:2])
    feats = load_features(st)

    cids = list(allc)
    tree = shapely.STRtree([allc[c].geom for c in cids])
    sel: dict[str, dict] = {c: {} for c in cids}
    for t, f in feats.items():
        pts = shapely.points(f["lon"], f["lat"])
        pi, gi = tree.query(pts, predicate="within")
        for c in cids:
            sel[c][t] = np.array([], int)
        order = np.argsort(gi, kind="stable")
        pi, gi = pi[order], gi[order]
        for g in np.unique(gi):
            sel[cids[g]][t] = pi[gi == g]
        print(f"  {t}: {len(pi):,} of {len(pts):,} inside the {len(cids)} polygons")

    # planet-wide parse statistics over every distinct tag value inside the polygons
    evcache: dict[str, Any] = {}
    rows = []
    for cid in cids:
        c = allc[cid]
        pois = city_pois(feats, sel[cid], evcache)
        rows.append({"city_id": cid, "region": c.region, "country": c.country, "target": cid in target_ids,
                     "pop": c.pop_2025, "groups": {g: group_stats(p) for g, p in pois.items()},
                     "groups_namechain": {g: _namechain_post(p) for g, p in pois.items() if g in
                                          ("groceries", "eating")}})
    n_vals = len(evcache)
    unp_vals = Counter(v for v in evcache.values() if isinstance(v, str))
    print(f"  distinct opening_hours values in polygons: {n_vals:,}; unparseable distinct: {sum(unp_vals.values()):,}"
          f" {dict(unp_vals.most_common(8))}")

    osm_flags = _osm_flags()
    out = Interim(source_id=SOURCE_ID, inputs=[f"{QLEVER_OSM}#{snap}#opening_hours"])
    for r in rows:
        if not r["target"]:
            continue
        cid = r["city_id"]
        for (g, chk), key in PUBLISH.items():
            s = r["groups"][g]
            reason = None
            if s["n_parsed"] < MIN_PARSED:
                reason = (f"only {s['n_parsed']} {g} POIs with a parseable opening_hours tag in the polygon "
                          f"(minimum {MIN_PARSED}; {s['n_all']} POIs in total)")
            elif s["coverage"] < MIN_COVERAGE:
                reason = (f"opening_hours tagged on {100 * s['coverage']:.1f}% of {s['n_all']} {g} POIs "
                          f"(minimum {100 * MIN_COVERAGE:.0f}%)")
            elif s[f"{chk}_post"] is None:
                reason = (f"chain/non-chain strata too small for post-stratification "
                          f"({s['n_parsed_chain']} chain, {s['n_parsed_nonchain']} non-chain parsed)")
            if reason:
                out.miss(key, cid, reason)
                continue
            det = {k: s[k] for k in ("n_all", "n_tagged", "n_parsed", "n_unparseable", "coverage", "parse_rate",
                                     "chain_share_all", "chain_share_parsed", "coverage_chain",
                                     "coverage_nonchain", "n_parsed_chain", "n_parsed_nonchain")}
            det |= {"raw_share": s[f"{chk}_raw"], "chain_share_value": s[f"{chk}_chain"],
                    "nonchain_share_value": s[f"{chk}_nonchain"], "osm_snapshot": f"planet-{snap}",
                    "check": chk, "coverage_flag": "low" if s["coverage"] < LOW_COVERAGE else "ok",
                    "late22_share": s["late22_post"], "fri12_share": s["fri12_post"], "sat12_share": s["sat12_post"],
                    "osm_nightlife_coverage_flag": osm_flags.get(cid, {}).get("nightlife"),
                    "osm_culture_coverage_flag": osm_flags.get(cid, {}).get("culture")}
            out.put(key, cid, s[f"{chk}_post"], quality="estimated", year=year, detail=det)

    summary = _validation(rows, osm_flags, unp_vals, n_vals)
    (RAW / "hours_validation_summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    out.notes = [
        (f"OSM snapshot planet-{snap}.osm.pbf via QLever osm-planet (osm2rdf). (c) OpenStreetMap contributors, "
         "ODbL 1.0, https://www.openstreetmap.org/copyright. Values are a Produced Work (ODbL 4.3)."),
        ("groceries = shop=supermarket|convenience; eating = amenity=restaurant|cafe|fast_food. Share (%) of POIs "
         "with a parseable opening_hours tag that are open at the check time on the reference week Mo 2026-10-05.."
         "Su 2026-10-11, PH/SH rules ignored: late = Wed 23:00, early = Wed 07:00, sunday = Sun 12:00, 24h = open "
         "every minute of the week."),
        ("Value is post-stratified by chain status (brand or brand:wikidata tag): chain_share_all * rate_chain + "
         "(1 - chain_share_all) * rate_nonchain, correcting for chains being tagged more often. raw/strata values "
         "in detail."),
        (f"Missing when < {MIN_PARSED} parsed tags or tag coverage < {100 * MIN_COVERAGE:.0f}% of the group's POIs. "
         "quality=estimated: tagged POIs are a non-random sample; see etl/notes/osm-hours.md."),
    ]
    p = out.write()
    print(f"wrote {p}")

    REFERENCE.mkdir(parents=True, exist_ok=True)
    cols = ["groceries", "supermarket", "eating"]
    with (REFERENCE / f"{SOURCE_ID}.csv").open("w") as f:
        hdr = ["city_id", "region", "pop_2025"]
        for g in cols:
            hdr += [f"{g}_n_all", f"{g}_n_parsed", f"{g}_coverage", f"{g}_chain_share_all"]
            hdr += [f"{g}_{c}_post" for c in CHECKS] + [f"{g}_{c}_raw" for c in ("late23", "early07", "sun12", "h24")]
        f.write(",".join(hdr) + "\n")
        for r in sorted(rows, key=lambda r: r["city_id"]):
            vals: list[Any] = [r["city_id"], f"\"{r['region']}\"", f"{r['pop']:.0f}"]
            for g in cols:
                s = r["groups"][g]
                vals += [s["n_all"], s["n_parsed"], s["coverage"], s["chain_share_all"]]
                vals += [s[f"{c}_post"] for c in CHECKS] + [s[f"{c}_raw"] for c in ("late23", "early07", "sun12",
                                                                                     "h24")]
            f.write(",".join("" if v is None else str(v) for v in vals) + "\n")
    _print_summary(summary)


def _namechain_post(pois: list[dict]) -> dict[str, Any]:
    """Sensitivity: post-stratify with chain := brand tag OR name repeated >= 5 times in the city."""
    alt = [p | {"chain": p["chain_name"]} for p in pois]
    s = group_stats(alt)
    return {f"{c}_post": s[f"{c}_post"] for c in CHECKS} | {"chain_share_all": s["chain_share_all"]}


def _osm_flags() -> dict[str, dict[str, str]]:
    from .common import INTERIM

    p = INTERIM / "osm.json"
    if not p.exists():
        return {}
    d = json.loads(p.read_text())
    out: dict[str, dict[str, str]] = defaultdict(dict)
    for g in ("culture", "nightlife"):
        for cid, e in d["values"].get(f"{g}_venues_per_km2", {}).items():
            out[cid][g] = e.get("detail", {}).get("coverage_flag")
    return out


def _validation(rows, osm_flags, unp_vals, n_vals) -> dict[str, Any]:
    tgt = [r for r in rows if r["target"]]
    S: dict[str, Any] = {"distinct_values_in_polygons": n_vals, "distinct_unparseable": dict(unp_vals.most_common())}
    for setname, rs in (("targets", tgt), ("reference", rows)):
        for g in ("groceries", "supermarket", "eating"):
            S[f"{setname}/{g}/coverage"] = _region_summary(rs, lambda r, g=g: r["groups"][g]["coverage"])
            S[f"{setname}/{g}/n_parsed"] = _region_summary(rs, lambda r, g=g: r["groups"][g]["n_parsed"])
            S[f"{setname}/{g}/parse_rate"] = _region_summary(rs, lambda r, g=g: r["groups"][g]["parse_rate"])
            S[f"{setname}/{g}/chain_share_all"] = _region_summary(rs, lambda r, g=g: r["groups"][g]["chain_share_all"])
            S[f"{setname}/{g}/coverage_chain"] = _region_summary(rs, lambda r, g=g: r["groups"][g]["coverage_chain"])
            S[f"{setname}/{g}/coverage_nonchain"] = _region_summary(
                rs, lambda r, g=g: r["groups"][g]["coverage_nonchain"])
            for c in CHECKS:
                S[f"{setname}/{g}/{c}_post"] = _region_summary(rs, lambda r, g=g, c=c: r["groups"][g][f"{c}_post"])
                S[f"{setname}/{g}/{c}_post_minus_raw"] = _region_summary(
                    rs, lambda r, g=g, c=c: None if r["groups"][g][f"{c}_post"] is None else
                    r["groups"][g][f"{c}_post"] - r["groups"][g][f"{c}_raw"])
                S[f"{setname}/{g}/{c}_chain_minus_nonchain"] = _region_summary(
                    rs, lambda r, g=g, c=c: None if r["groups"][g]["n_parsed_chain"] < MIN_STRATUM or
                    r["groups"][g]["n_parsed_nonchain"] < MIN_STRATUM else
                    r["groups"][g][f"{c}_chain"] - r["groups"][g][f"{c}_nonchain"])
    # does tag coverage relate to the metric? (Spearman across cities with enough data, reference set)
    corr = {}
    for g in ("groceries", "eating"):
        for c in CHECKS:
            ok = [r for r in rows if r["groups"][g]["n_parsed"] >= MIN_PARSED and r["groups"][g][f"{c}_post"]
                  is not None]
            corr[f"{g}/{c}"] = {
                "n": len(ok),
                "spearman_coverage_vs_post": _spearman([r["groups"][g]["coverage"] for r in ok],
                                                       [r["groups"][g][f"{c}_post"] for r in ok]),
                "spearman_raw_vs_post": _spearman([r["groups"][g][f"{c}_raw"] for r in ok],
                                                  [r["groups"][g][f"{c}_post"] for r in ok]),
                "spearman_post_vs_namechain_post": _spearman(
                    [r["groups"][g][f"{c}_post"] for r in ok if r["groups_namechain"][g][f"{c}_post"] is not None],
                    [r["groups_namechain"][g][f"{c}_post"] for r in ok
                     if r["groups_namechain"][g][f"{c}_post"] is not None]),
                "spearman_chain_vs_nonchain": _spearman(
                    [r["groups"][g][f"{c}_chain"] for r in ok if r["groups"][g]["n_parsed_chain"] >= 30
                     and r["groups"][g]["n_parsed_nonchain"] >= 30],
                    [r["groups"][g][f"{c}_nonchain"] for r in ok if r["groups"][g]["n_parsed_chain"] >= 30
                     and r["groups"][g]["n_parsed_nonchain"] >= 30]),
            }
    S["correlations_reference"] = corr
    # per-target table (compact) for the notes
    S["targets_table"] = {
        r["city_id"]: {
            "region": r["region"],
            **{f"{g}.{k}": r["groups"][g][k] for g in ("groceries", "supermarket", "eating")
               for k in ("n_all", "n_parsed", "coverage", "chain_share_all", "coverage_chain", "coverage_nonchain",
                         "late23_post", "late23_raw", "late23_chain", "late23_nonchain", "early07_post", "sun12_post",
                         "sun12_raw", "sun_any_post", "h24_post", "h24_raw", "late22_post", "fri12_post",
                         "sat12_post")},
            "osm_flags": osm_flags.get(r["city_id"]),
        } for r in sorted(tgt, key=lambda r: r["city_id"])}
    # tag coverage vs osm.json nightlife flag
    by_flag = defaultdict(list)
    for r in tgt:
        fl = (osm_flags.get(r["city_id"]) or {}).get("nightlife")
        by_flag[fl].append(r["groups"]["eating"]["coverage"])
    S["eating_coverage_by_osm_nightlife_flag"] = {str(k): {"n": len(v), "median": round(median(v), 3)}
                                                  for k, v in by_flag.items()}
    return S


def _print_summary(S):
    for k in ("targets/groceries/coverage", "targets/eating/coverage", "targets/groceries/late23_post",
              "targets/groceries/sun12_post", "targets/eating/late23_post", "targets/eating/early07_post"):
        print(k, json.dumps(S[k]))
    print(json.dumps(S["correlations_reference"], indent=1))


if __name__ == "__main__":
    main()
