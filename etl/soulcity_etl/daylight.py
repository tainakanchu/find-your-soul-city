"""Daylight-timing metrics per city: computed from coordinates + IANA time-zone rules (no remote data).

Inputs (all Python packages, pinned in uv.lock):
  - timezonefinder (MIT code) + timezonefinder-data (ODbL; timezone-boundary-builder boundaries): point -> IANA zone.
  - tzdata (public domain IANA tz database) loaded explicitly (not the OS copy) for the 2025 UTC-offset rules.
  - astral (Apache-2.0): NOAA-style solar position -> sunset / solar noon.
Independent cross-check (validation only): the "sunrise equation" (Meeus / Astronomical Almanac formulation, own
implementation below) compared for every city.

Metrics (year 2025, evaluated at City.lat/lon = representative point of the GHS-UCDB polygon):
  sunset_summer_local   local clock time (hours since local midnight, DST as in force) of sunset on the local
                        summer solstice date (21 June north of the equator, 21 December south). Sunset = upper limb
                        at the horizon with standard refraction (zenith 90.833 deg), sea-level horizon. The sunset is
                        the first one after 12:00 local clock time of that date; if it happens after midnight it is
                        reported as 24 + x (e.g. Reykjavik 24.07 = 00:04 the next day).
  sunset_winter_local   same for the winter solstice date (21 Dec north, 21 June south).
  solar_noon_offset_h   local solar noon on 20 March 2025 (March equinox date) expressed in zone *standard* time
                        (lower of the 15 Jan / 15 Jul offsets, i.e. DST removed) minus 12 h. Positive: the standard-time clock runs ahead of the
                        sun (noon sun comes after 12:00); e.g. Madrid (UTC+1 standard, lon -3.7) = +1.4 h.
                        Add 1 h for the summer clock where DST is in use.
"""

from __future__ import annotations

import csv
import datetime as dt
import importlib.metadata as md
import math
import zoneinfo
from functools import cache
from importlib import resources

from astral import Observer
from astral.sun import noon as astral_noon
from astral.sun import sunset as astral_sunset
from timezonefinder import TimezoneFinder

from .cities import City, load_cities, reference_centres
from .common import REFERENCE, Interim, record_dataset

SOURCE_ID = "daylight"
YEAR = 2025
EQUINOX = dt.date(YEAR, 3, 20)  # March equinox 2025 = 20 Mar 09:01 UTC
JUNE = dt.date(YEAR, 6, 21)
DECEMBER = dt.date(YEAR, 12, 21)
QUALITY = "estimated"  # deterministic calculation for one representative point; see notes/daylight.md
UTC = dt.UTC


def _versions() -> dict[str, str]:
    return {p: md.version(p) for p in ("timezonefinder", "timezonefinder-data", "tzdata", "astral")}


@cache
def _tf() -> TimezoneFinder:
    return TimezoneFinder()


@cache
def _zone(name: str) -> zoneinfo.ZoneInfo:
    """Zone rules from the pinned `tzdata` package (not the OS tz database)."""
    pkg, _, res = ("tzdata.zoneinfo/" + name).partition("/")
    parts = res.split("/")
    path = resources.files(pkg)
    for p in parts:
        path = path / p
    with path.open("rb") as f:
        return zoneinfo.ZoneInfo.from_file(f, key=name)


def zone_name(lat: float, lon: float) -> str | None:
    return _tf().timezone_at(lat=lat, lng=lon)


def _decimal_hours(t: dt.datetime, day: dt.date) -> float:
    """Wall-clock hours from 00:00 of `day` (naive wall-clock difference; no DST change on these dates)."""
    wall = t.replace(tzinfo=None)
    return (wall - dt.datetime.combine(day, dt.time())).total_seconds() / 3600


def sunset_local(lat: float, lon: float, tz: zoneinfo.ZoneInfo, day: dt.date) -> dt.datetime:
    """First sunset after 12:00 local clock time on `day`. Raises ValueError if the sun does not set."""
    obs = Observer(latitude=lat, longitude=lon)
    noon_clock = dt.datetime.combine(day, dt.time(12), tzinfo=tz)
    found = []
    for d in (day - dt.timedelta(days=1), day, day + dt.timedelta(days=1)):
        try:
            found.append(astral_sunset(obs, d, tzinfo=tz))
        except ValueError:
            continue
    found = sorted(t for t in found if noon_clock <= t < noon_clock + dt.timedelta(hours=24))
    if not found:
        raise ValueError("no sunset within 24 h after local 12:00 (sun stays above or below the horizon)")
    return found[0]


def standard_offset_h(tz: zoneinfo.ZoneInfo) -> float:
    """Non-DST ("standard") UTC offset: the lower of the offsets on 15 Jan and 15 Jul 2025.

    Not `utcoffset - dst()`: the tzdata package encodes Ireland (winter) and Morocco (Ramadan) with *negative* DST on
    top of a +1 base, which would make Dublin "standard" UTC+1. Taking the lower of the two mid-season offsets gives
    GMT for Ireland, UTC+1 for Morocco and the winter offset in both hemispheres.
    """
    offs = [dt.datetime(YEAR, m, 15, 12, tzinfo=tz).utcoffset() for m in (1, 7)]
    return min(offs).total_seconds() / 3600


def solar_noon_offset(lat: float, lon: float, tz: zoneinfo.ZoneInfo) -> tuple[float, float]:
    """(solar-noon clock time on the equinox date in standard time - 12, standard UTC offset in h)."""
    n = astral_noon(Observer(latitude=lat, longitude=lon), EQUINOX, tzinfo=UTC)
    std = standard_offset_h(tz)
    h = (n.hour + n.minute / 60 + n.second / 3600 + std) % 24
    off = h - 12
    # solar noon within a few hours of 12:00 clock for every legal zone, but wrap defensively
    if off > 12:
        off -= 24
    return off, std


# --- independent implementation (validation only) -------------------------------------------------------------

def sunrise_equation_sunset_utc_h(lat: float, lon: float, day: dt.date) -> float:
    """Sunset (UTC hours since 00:00 UTC of the solar day starting near `day`) from the textbook sunrise equation.

    n = ceil(JD - 2451545.0 + 0.0008); J* = n - lon/360; M = 357.5291 + 0.98560028 J*;
    C = 1.9148 sin M + 0.02 sin 2M + 0.0003 sin 3M; lambda = M + C + 180 + 102.9372;
    J_transit = 2451545 + J* + 0.0053 sin M - 0.0069 sin 2 lambda; sin d = sin lambda sin 23.4397;
    cos w0 = (sin(-0.833) - sin phi sin d) / (cos phi cos d); J_set = J_transit + w0/360.
    Returns the sunset as hours since 00:00 UTC of `day` (can be <0 or >24 for far-from-Greenwich longitudes).
    """
    jd = (dt.datetime.combine(day, dt.time(12)) - dt.datetime(2000, 1, 1, 12)).total_seconds() / 86400 + 2451545.0
    n = math.ceil(jd - 2451545.0 + 0.0008)
    jstar = n - lon / 360
    m = math.radians((357.5291 + 0.98560028 * jstar) % 360)
    c = 1.9148 * math.sin(m) + 0.02 * math.sin(2 * m) + 0.0003 * math.sin(3 * m)
    lam = math.radians((math.degrees(m) + c + 180 + 102.9372) % 360)
    jtr = 2451545.0 + jstar + 0.0053 * math.sin(m) - 0.0069 * math.sin(2 * lam)
    sind = math.sin(lam) * math.sin(math.radians(23.4397))
    cosd = math.sqrt(1 - sind * sind)
    phi = math.radians(lat)
    cosw = (math.sin(math.radians(-0.833)) - math.sin(phi) * sind) / (math.cos(phi) * cosd)
    if not -1 <= cosw <= 1:
        raise ValueError("no sunset")
    jset = jtr + math.degrees(math.acos(cosw)) / 360
    # Julian date -> hours since 00:00 UTC of `day` (JD of 00:00 UTC of day = jd - 0.5)
    return (jset - (jd - 0.5)) * 24


def independent_sunset_local_h(lat: float, lon: float, tz: zoneinfo.ZoneInfo, day: dt.date) -> float:
    """Local clock decimal hours of the first sunset after 12:00 local, via the sunrise equation."""
    cands = []
    for k in (-1, 0, 1):
        d = day + dt.timedelta(days=k)
        t_utc = dt.datetime.combine(d, dt.time(), tzinfo=UTC) + dt.timedelta(hours=sunset_equation_h(lat, lon, d))
        loc = t_utc.astimezone(tz)
        cands.append(loc)
    noon_clock = dt.datetime.combine(day, dt.time(12), tzinfo=tz)
    ok = sorted(t for t in cands if noon_clock <= t < noon_clock + dt.timedelta(hours=24))
    if not ok:
        raise ValueError("no sunset")
    return _decimal_hours(ok[0], day)


def sunset_equation_h(lat: float, lon: float, day: dt.date) -> float:
    return sunrise_equation_sunset_utc_h(lat, lon, day)


# --- metric computation ---------------------------------------------------------------------------------------

def compute(c: City) -> dict:
    """Returns dict with tz, lat, lon, std offset and the three metrics (or reasons they are missing)."""
    out: dict = {"lat": c.lat, "lon": c.lon, "tz": None, "miss": {}}
    name = zone_name(c.lat, c.lon)
    if name is None:
        reason = "timezonefinder returned no zone for the representative point"
        out["miss"] = dict.fromkeys(("sunset_summer_local", "sunset_winter_local", "solar_noon_offset_h"), reason)
        return out
    out["tz"] = name
    tz = _zone(name)
    north = c.lat >= 0
    summer_day, winter_day = (JUNE, DECEMBER) if north else (DECEMBER, JUNE)
    out["summer_day"], out["winter_day"] = summer_day.isoformat(), winter_day.isoformat()
    for key, day in (("sunset_summer_local", summer_day), ("sunset_winter_local", winter_day)):
        try:
            t = sunset_local(c.lat, c.lon, tz, day)
            out[key] = _decimal_hours(t, day)
            out[key + "_iso"] = t.isoformat()
            out[key + "_utc_offset_h"] = t.utcoffset().total_seconds() / 3600
            try:
                out[key + "_xcheck_h"] = independent_sunset_local_h(c.lat, c.lon, tz, day)
            except ValueError:
                out[key + "_xcheck_h"] = None
        except ValueError as e:
            out["miss"][key] = (f"{e}: at lat {c.lat:.2f} on {day.isoformat()} the sun does not set "
                                f"(or never rises) under the -0.833 deg horizon definition")
    off, std = solar_noon_offset(c.lat, c.lon, tz)
    out["solar_noon_offset_h"], out["std_utc_offset_h"] = off, std
    return out


def _detail(r: dict, key: str) -> dict:
    d: dict = {"tz": r["tz"], "lat": r["lat"], "lon": r["lon"], "versions": _versions()}
    if key.startswith("sunset"):
        d |= {"local_time_iso": r[key + "_iso"], "utc_offset_h": r[key + "_utc_offset_h"],
              "date": r["summer_day"] if "summer" in key else r["winter_day"]}
        if r.get(key + "_xcheck_h") is not None:
            d["xcheck_sunrise_equation_h"] = round(r[key + "_xcheck_h"], 4)
    else:
        d |= {"date": EQUINOX.isoformat(), "standard_utc_offset_h": r["std_utc_offset_h"]}
    return d


def main() -> None:
    v = _versions()
    keys = [f"pypi:{p}=={ver}" for p, ver in v.items()]
    for p, ver in v.items():
        record_dataset(f"pypi:{p}=={ver}", kind="python-package", note="installed from the uv lock; no network use at run time")
    it = Interim(source_id=SOURCE_ID, inputs=keys)
    it.notes += [
        f"Computed, not looked up. Year {YEAR}. Versions: {v}.",
        "Sunset = upper limb, zenith 90.833 deg, sea-level horizon (astral/NOAA); solar_noon_offset_h uses zone "
        "standard time (lower of the 15 Jan / 15 Jul offsets, i.e. DST removed) on 2025-03-20.",
        "Sunset after local midnight is reported as 24 + x hours.",
    ]
    for c in load_cities():
        r = compute(c)
        for k in ("sunset_summer_local", "sunset_winter_local", "solar_noon_offset_h"):
            if k in r["miss"]:
                it.miss(k, c.city_id, r["miss"][k])
            else:
                it.put(k, c.city_id, r[k], quality=QUALITY, year=YEAR, detail=_detail(r, k))
    path = it.write()
    print("wrote", path)

    rows, diffs = [], []
    for c in reference_centres():
        r = compute(c)
        rows.append({
            "city_id": c.city_id, "ucdb_id": c.ucdb_id, "name_en": c.name_en, "lat": c.lat, "lon": c.lon,
            "tz": r["tz"] or "",
            **{k: ("" if r.get(k) is None else f"{r[k]:.4f}")
               for k in ("sunset_summer_local", "sunset_winter_local", "solar_noon_offset_h", "std_utc_offset_h")},
        })
        for k in ("sunset_summer_local", "sunset_winter_local"):
            if r.get(k) is not None and r.get(k + "_xcheck_h") is not None:
                diffs.append(abs(r[k] - r[k + "_xcheck_h"]) * 60)
    REFERENCE.mkdir(parents=True, exist_ok=True)
    out = REFERENCE / f"{SOURCE_ID}.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    diffs.sort()
    print(f"wrote {out} ({len(rows)} centres); astral vs sunrise-equation |diff| min: n={len(diffs)} "
          f"median={diffs[len(diffs) // 2]:.2f} p95={diffs[int(len(diffs) * .95)]:.2f} max={diffs[-1]:.2f}")


if __name__ == "__main__":
    main()
