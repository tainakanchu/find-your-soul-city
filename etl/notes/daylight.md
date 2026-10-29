# Daylight timing (`daylight`)

Module: `etl/soulcity_etl/daylight.py` (`cd etl && UV_SYSTEM_CERTS=1 uv run python -m soulcity_etl.daylight`).
Outputs: `data/interim/daylight.json` (130 target cities, none missing), `data/reference/daylight.csv` (524 centres).
Tests: `etl/tests/test_daylight.py`. Run time about 5 s. **No remote service is contacted**: every input is a pinned
Python package (`uv.lock`), so the external-access policy is not engaged.

## Metrics (`year: 2025`, `quality: estimated`)

Point: `City.lat/lon` (representative point inside the GHS-UCDB polygon, rounded to 1e-4 deg). A sub-degree choice of
point inside a city moves sunset by well under 1 min; the polygon is not otherwise used.

| key                   | definition                                                                            | unit                                |
| --------------------- | ------------------------------------------------------------------------------------- | ----------------------------------- |
| `sunset_summer_local` | local clock time of sunset on the local summer solstice date, DST as in force in 2025 | decimal hours since 00:00 (can >24) |
| `sunset_winter_local` | same on the local winter solstice date                                                | decimal hours since 00:00           |
| `solar_noon_offset_h` | clock time of solar noon on 2025-03-20 in zone **standard** time, minus 12:00         | hours (+ = clock ahead of the sun)  |

- Summer date = 21 June for lat >= 0, 21 December for lat < 0 (winter = the other). Dates are fixed calendar dates,
  not the exact astronomical solstice instant (21 June 2025 is the solstice date in UTC; the sunset changes by less
  than 1 s/day around solstices).
- Sunset = upper limb on a sea-level horizon with standard refraction (solar zenith 90.833 deg). No elevation/terrain.
- Sunset is "the first sunset after 12:00 local clock time of that date". If it falls after midnight it is reported as
  24 + x: Reykjavik 24.03 = 00:02 on 22 June. (Reykjavik is the only city above 24.)
- `solar_noon_offset_h`: UTC solar noon of 2025-03-20 (March equinox, 09:01 UTC) + the zone's **standard** UTC offset,
  minus 12. Equation of time on that date is about -7.5 min (included, via astral). Standard offset = the **lower of the
  zone offsets on 15 Jan and 15 Jul 2025**, i.e. DST removed in both hemispheres. This is deliberately not
  `utcoffset - dst()`: the tzdata package encodes Ireland (winter) and Morocco (Ramadan) as negative DST on a +1 base,
  which would make Dublin "standard" UTC+1 (the only target where the two rules differ; it would give +1.55 h
  instead of +0.55 h). Morocco is treated as UTC+1 (its clock outside Ramadan), so Casablanca/Marrakesh are +1.6 h.
  For the summer clock add the DST hour where it applies; the value is "how far a year-round winter clock is from
  the sun at the equinox", not what the wall clock said on that day.
- Sunset detail records the ISO local time, UTC offset used, tz name, `xcheck_sunrise_equation_h`, package versions.

## Method and inputs

| step               | tool (version)                                                                                        | licence                                     |
| ------------------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| point -> IANA zone | `timezonefinder` 9.0.0 + `timezonefinder-data` 3.2026.4 (boundaries from timezone-boundary-builder)   | code MIT; boundary data ODbL v1.0           |
| zone offsets / DST | `tzdata` 2026.5 (IANA tz database 2026e), loaded explicitly via `ZoneInfo.from_file`, not the OS copy | Apache-2.0 wrapper; IANA data public domain |
| sun position       | `astral` 3.2 (`astral.sun.sunset`, `astral.sun.noon`; NOAA-style equations, Spencer/NOAA series)      | Apache-2.0                                  |

Licence quotes (installed `*.dist-info/licenses/LICENSE`): timezonefinder "The MIT License (MIT) Copyright (c) 2016
Jannik Michelfeit ... Permission is hereby granted, free of charge, to any person obtaining a copy of this software
..."; timezonefinder-data ships the "Open Database License (ODbL) v1.0" text (https://opendatacommons.org/licenses/odbl/1-0/).
Operative ODbL clauses: s.4.3 "if you Publicly Use a Produced Work, You must include a notice ... that Content was
obtained from the Database ... and that it is available under this License", example: "Contains information from
DATABASE NAME, which is made available here under the Open Database License (ODbL)."; s.4.4 share-alike for publicly
used Derivative Databases (our ODbL data is compatible). Our output holds only computed times, not boundary geometry.
Attribution to include in the public methodology: "Time zones from timezone-boundary-builder
(https://github.com/evansiroky/timezone-boundary-builder) via timezonefinder, ODbL 1.0; IANA tz database; solar
position with astral (Apache-2.0)." Requirements of astral's Apache-2.0 (notice retention) apply to redistribution of
the code, not to the numbers.

## Quality label: `estimated`, not `observed`

`observed` is defined in BRIEF.md as a direct measurement/official statistic. These values are model outputs
(analytic solar ephemeris, accuracy about 1 min at mid-latitudes, point not polygon, sea-level horizon, no
terrain/atmospheric variation, a zone assignment taken from a boundary dataset and the 2025 tz rules). They are
deterministic and reproducible but derived with documented assumptions, hence `estimated`. Nothing is `imputed`.

## Ranges (130 cities)

| metric                | min                                                       | median | max                  |
| --------------------- | --------------------------------------------------------- | ------ | -------------------- |
| `sunset_summer_local` | 17.71 (Fortaleza)                                         | 19.56  | 24.03 (Reykjavik)    |
| `sunset_winter_local` | 14.80 (Stockholm)                                         | 17.31  | 19.17 (Kuala Lumpur) |
| `solar_noon_offset_h` | -0.31 (Salvador; Doha, Fortaleza, Sapporo all about -0.3) | 0.34   | 1.66 (Marrakesh)     |

Sample (summer sunset / winter sunset / noon offset): Stockholm 22.13 / 14.80 / -0.08; Helsinki 22.84 / 15.19 / 0.46;
Reykjavik 24.03 / 15.48 / 1.58; Madrid 21.80 / 17.85 / 1.37; Lisbon 21.08 / 17.30 / 0.74; Paris 21.95 / 16.93 / 0.97;
London 21.36 / 15.88 / 0.13; Singapore 19.21 / 19.07 / 1.20; Kuala Lumpur 19.17 winter; Tokyo 19.00 / 16.52 / -0.19;
Sydney (21 Dec) 20.10 / 16.90 (21 Jun) / 0.05; Quito 18.27 / 18.32.

## Polar / edge cases

- Midnight sun or polar night: `sunset_local` raises `ValueError` when no sunset lies within 24 h after 12:00
  local; the metric is then written via `Interim.miss` with a reason. **Does not occur in the 130 targets** (highest
  latitude Reykjavik 64.1 N sets at 00:02) so `missing` is empty. In the 524 reference centres no value is empty either
  (checked: every row has tz and both sunsets).
- Time zones with `Etc/` ocean names were checked: none among the reference centres.
- Western China is not represented by a target; all Chinese cities use Asia/Shanghai (UTC+8) as per the tz
  database, which is the legal clock. If a far-west city (Urumqi/Kashgar) were added, the solar noon offset would
  be about +3 h by this definition (unofficial Xinjiang time is not modelled).
- Zone-dependent oddities, by design: Istanbul/Izmir/Ankara UTC+3 permanent (noon offset +1.3 at Izmir), Iceland
  UTC+0 (+1.6), Kuala Lumpur/Singapore UTC+8 (+1.2 to +1.35), Spain UTC+1 (+1.4 Madrid).

## Validation

1. Second method, own implementation of the textbook sunrise equation (Julian transit, mean anomaly, equation of
   centre, hour angle with -0.833 deg), `independent_sunset_local_h`, computed for every sunset: 524 reference
   centres x 2 solstices = 1048 values: |astral - sunrise equation| median 0.04 min, p95 0.16 min, max 0.46 min;
   among the 130 targets the maximum is 1.07 min (Reykjavik, where the sun skims the horizon at a very shallow
   angle and small formula differences produce larger timing differences). All within the required +/-2 min.
   Caveat: both methods are low-order NOAA/Meeus-type series, so they share the same family of approximation; the
   comparison tests our implementation (date handling, longitude, DST, the after-midnight rule), not the accuracy
   of the model itself (about 1 min). No higher-precision ephemeris (JPL) was added.
2. Published almanac check (reading only, no scraping): not performed by lookup. Instead the sanity checks below were
   compared with commonly cited values: Stockholm sunset 22:08 (computed 22:08:05 CEST), Helsinki 22:50 (computed
   22:50:20 EEST), Reykjavik about 00:02-00:04 (computed 00:01:52 GMT, a sea-level result; published tables for
   a point at 0 m differ by a couple of minutes), Singapore 19:12 / 19:04, Madrid 21:48 (computed 21:48:10 CEST)
   against Lisbon 21:05 (1 h of clock difference, 5 deg lon), London 21:21. These are recollected, not fetched,
   so they are only plausibility checks.
3. Structure checks: Singapore summer 19.21 vs winter 19.07 (stable around 19:1x); Quito/Nairobi
   within 0.1 h of 18.3/18.6 year-round; Stockholm, Helsinki, Oslo and Reykjavik are the four latest summer sunsets, and
   the four earliest winter sunsets are Stockholm 14.80, Helsinki 15.19, Oslo 15.20, Warsaw 15.42; southern-hemisphere
   cities use 21 Dec as summer (Sydney 20.10, Cape Town 19.94, Sao Paulo 18.88); Madrid (21.80) later than Lisbon
   (21.08) at similar latitude; Dublin noon offset 0.55 h after the standard-offset fix.
4. Unit tests: `etl/tests/test_daylight.py` (Singapore stability, Reykjavik > 24 h, midnight sun at Longyearbyen
   raises, standard offsets of Dublin/Casablanca/Sydney, astral vs sunrise equation within 2 min).

## Known biases and caveats

- Representative point, not a population-weighted centre; large metros span about 0.1-0.5 deg lon = up to 2 min.
- Sea-level horizon and no terrain: mountain-ringed cities (Kathmandu, Medellin, Quito, Tehran) have real
  sunsets earlier by minutes to over an hour; coastal/elevated cities differ by a minute at most.
- Zone from point-in-boundary: a point close to a zone border could pick the neighbouring zone (tz boundary builder
  has ocean/land edges); none produced an `Etc/` result.
- 2025 tz rules from tzdata 2026e; later rule changes are not reflected.
- `solar_noon_offset_h` uses standard time (see definition); it does not describe the DST wall clock.

## Alternatives considered

- Looking sunsets up on timeanddate.com / almanac sites: scraping a web UI, forbidden by the access policy and not
  a documented data route; also not reproducible.
- NASA/USNO/NOAA web calculators: same reason (form posts); the NOAA equations are used offline instead.
- `pytz`/OS tz data: replaced by an explicit `tzdata` pin for reproducibility.
- `suntime`, `ephem`, `skyfield`: ephem/skyfield need compiled/ephemeris downloads; astral is pure Python and sufficient.
- `quality: observed`: rejected, see above.
