# OSM opening hours: city "chronotype" (`osm-hours`)

Module: `etl/soulcity_etl/opening_hours.py` (`cd etl && UV_SYSTEM_CERTS=1 uv run python -m soulcity_etl.opening_hours`)
Output: `data/interim/osm-hours.json` (130 targets), `data/reference/osm-hours.csv` (530 centres = 524 reference
centres with pop >= 1M plus the smaller targets). Validation summary: `.cache/raw/osm/hours_validation_summary.json`
(regenerated per run, includes a per-target table).

Diagnosis questions this can serve: "Until what time do you want shops / restaurants to be open?", "Do you need to
shop on Sundays?", "Do you eat breakfast out early?"

## Recommendation (summary)

| metric                                            | recommendation                                                           | why                                                                                                                                                                                                                                         |
| ------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grocery_late_open_share` (Wed 23:00)             | **adopt, `estimated`, ideal-type question** ("shops open until ...")     | Strongest signal. Konbini cities are at 71-80%, Europe has a median of 11.6%, and the regional pattern matches expectations. Brand reweighting changes it by a median of less than 3 points                                                 |
| `grocery_24h_share`                               | adopt as an alternative to late (r high); pick one, not both             | Almost the same construct (Tokyo 73%, Vienna 2.3%)                                                                                                                                                                                          |
| `grocery_sunday_open_share` (Sun 12:00)           | **adopt with care, only as a "need Sunday shopping" filter/penalty**     | Clear signal only for DE/AT/CH/NO/GR: Munich 6.5%, Vienna 7.8%, Berlin 16%, Zurich 25%, Oslo 36%, Athens 33%. Elsewhere it sits at 80-100%, so it does not separate cities. "Sunday" is the wrong rest day in MENA and Israel (see caveats) |
| `supermarket_sunday_open_share`                   | better variant of the Sunday metric where available (80/130)             | Removes late-night kiosks and Spätis, which are mostly open on Sundays: Berlin groceries 16%, but supermarkets 2.2%                                                                                                                         |
| `eating_late_open_share` (Wed 23:00)              | **adopt, `estimated`, ideal-type** ("dinner at 22:00+ should be normal") | Spanish, Greek and Italian late dinners are visible: Madrid 57%, Athens 66%, Barcelona 44%, Rome 42%. Compare London 12%, Sydney 8% and US cities 7-25%. MENA/Central Asia are high too (Cairo 75%, Riyadh 87%, Tashkent 41%)               |
| `eating_early_open_share` (Wed 07:00)             | secondary / optional                                                     | Plausible: early-breakfast cultures are high (US 28%, AU 35%), Southern Europe is low (Madrid 9%). The chain effect is the largest of all metrics here (chains +12 to +33 points)                                                           |
| `eating_24h_share`, `supermarket_late_open_share` | diagnostic only                                                          | Small numbers (Europe median 0.5%) or many missing values                                                                                                                                                                                   |

How the metrics should be used:

- They are **preference-ideal / directional** inputs, not quality-of-life "higher is better" scores. A night owl
  wants a high `late_open_share`. Someone who values quiet streets or labour-protective Sunday closing does not care,
  or prefers low values.
- Suggested phrasing: an ideal-type question ("Until what time should shops near you be open?" with the options
  21:00 / 23:00 / 24 h). Map it to `grocery_late_open_share` and `grocery_24h_share` as "the higher the better if the
  user chose late". Ask the Sunday question as a yes/no need ("I need to do groceries on Sundays"), which penalises
  low `supermarket_sunday_open_share`.
- Use coarse bins (for example terciles over the non-missing targets). The values are tagged-POI shares and carry
  sampling and selection noise of a few percentage points. Treat `detail.coverage_flag = "low"` (coverage below
  15%) as low confidence.

All values are `quality: "estimated"`: the tagged POIs are a non-random sample (see Bias), and the value is
post-stratified.

## Metric definitions

- **POI groups**
  - groceries = `shop=supermarket` + `shop=convenience`
  - supermarket = `shop=supermarket`
  - eating = `amenity=restaurant` + `amenity=cafe` + `amenity=fast_food`
  - bars and pubs are excluded
  - Each group is a set of OSM features (node, way or relation) whose centroid (`geof:centroid` of the full
    geometry) lies inside the GHS-UCDB R2024A polygon (`shapely` point-in-polygon on the exact polygon, so there is
    no boundary mismatch).
- **Evaluated set**: POIs whose `opening_hours` tag parses (see Parser). POIs without the tag are **never** given
  hours. They enter only the denominator of the coverage figure and the chain-share weight.
- **Checks**, all in local time on a fixed **reference week Mon 2026-10-05 .. Sun 2026-10-11** (ISO week 41):
  - `late` = open at Wed 23:00, so a shop closing at 23:00 counts as not open
  - `early` = open at Wed 07:00
  - `sunday` = open at Sun 12:00
  - `24h` = open every minute of the 7 days
  - Diagnostics in `detail` and the CSV:
    - `late22_share` (Wed 22:00)
    - `fri12_share`, `sat12_share`
    - `sun_any`: any opening Sun 06:00-22:00, excluding spill-over from Saturday night
- **Holidays**: public/school holiday rules (`PH`, `SH`, `PH -1 day`, ...) are ignored. A normal week is evaluated.
  Rules that apply only to Easter, Christmas or other dates outside the reference week do not apply.
  Nth-weekday rules (`Su[1]`) are skipped, because they apply to some weeks only.
- **Sunday at 12:00 rather than "any time on Sunday"**:
  - Noon is the time a weekly shop would happen.
  - It is robust to spill-over (a shop open "Sa 08:00-01:00" is not a Sunday shop).
  - It is robust to short morning-only windows (French supermarkets open until 13:00 are counted; a bakery-style
    07:00-09:00 window is not).
  - The difference is small anyway. The median target has `sun_any - sun12` < 1 point. Shanghai is the largest gap
    (81% vs 98%).
- **Unit**: % (0-100) of evaluated POIs.
- **Value published** (post-stratified by chain status):
  `chain_share_all * rate_chain + (1 - chain_share_all) * rate_nonchain`
  - chain = the POI has a `brand` or `brand:wikidata` tag
  - `chain_share_all` = chain share among **all** POIs of the group in the polygon, tagged or not
  - Requires at least 10 parsed POIs in each stratum. When chains make up less than 5% of POIs (or more than 95%),
    the rate of the dominant stratum is used. Otherwise the value is missing.
  - Raw (unweighted) and per-stratum rates are in `detail` (`raw_share`, `chain_share_value`,
    `nonchain_share_value`).
- **Observation date**: OSM planet `planet-260921.osm.pbf` (2026-09-21), so `year: 2026`. Tags record the hours
  mappers entered at various times; no `check_date` filtering is applied.

### Minimum data (value is missing otherwise, with the reason in `missing`)

1. At least **50 POIs with a parseable tag** per group and city.
2. Tag coverage (tagged / all POIs of the group) of at least **5%**.
3. Chain/non-chain strata large enough (see above).

Why 5% and not 10%: within each region, city-level coverage shows **no consistent relation** to the metric.
These are Spearman correlations across reference centres with at least 50 parsed tags; the sign flips between
regions:

- groceries late: Europe −0.11, E/SE Asia +0.40, LatAm −0.47, N. America +0.02
- eating late: Europe −0.34, E/SE Asia −0.18, LatAm +0.02, N. America −0.49

Raising the floor would therefore not buy a demonstrable bias reduction. It would drop well-populated cities with
plausible values: Seoul groceries 7.7% coverage but 815 parsed tags; Beijing; Bogotá. The 5% floor removes only the
extreme cases, where fewer than 1 in 20 POIs is tagged (for example Seoul eating at 2.8%, Karachi). Values with
coverage below 15% carry `detail.coverage_flag = "low"`. That applies to 23 grocery values and 37 eating values.

## Parser

### Options considered

- **opening-hours-py 2.1.4** (PyPI, Rust core `opening-hours-rs`): licence "MIT OR Apache-2.0" (PyPI metadata),
  released 2026-07-07, so it satisfies `exclude-newer`. It implements the full spec and was used as the
  **cross-check** (run in a throw-away environment with `uv run --no-project --with opening-hours-py==2.1.4`).
  It is not a project dependency, because adding it would touch `pyproject.toml`/`uv.lock`, which other agents were
  editing.
  - **The orchestrator may `uv add opening-hours-py==2.1.4`** if a library is preferred. Results agree to within
    0.5% of POIs (see below).
- **osm-humanized-opening-hours** 0.6.2: AGPL-3.0 (PyPI classifier), last release 2018. Rejected for the licence and
  because it is unmaintained.
- **osm-opening-hours** / **opening-hours** (0.1.x): no licence given, abandoned. Rejected.

### Own parser

`parse_oh()` is about 300 lines and supports this subset of the
[specification](https://wiki.openstreetmap.org/wiki/Key:opening_hours/specification):

- `24/7`
- rule separators `;` (normal, overrides the days it names), `,` (additional rule) and `||` (fallback: applies only
  to days no earlier rule named; a comment-only fallback is ignored)
- weekday ranges and lists, including wrap-around (`Su-Th`, `Fr-Mo`) and an optional `:` after selectors
- month, month-day, year and `week` selectors, including wrap-around (`Nov-Mar`)
- `easter` (± n days), which never falls inside the reference week
- time ranges, including past midnight (`18:00-03:00`, `18:00-26:00`), `24:00`, and `00:00-00:00` as 24 h
- `off`/`closed` (an `off` rule with times subtracts them)
- comments
- en-dashes as `-`, case-insensitive weekdays, a missing comma between time ranges
- Hours past midnight spill into the next day.

It reports these as **unparseable**, counted separately by reason:

- `open_end` (`18:00+`, ambiguous for a 23:00 check)
- `event_time` (`sunrise-sunset`)
- `unknown_state` (comment-only values such as `"by appointment"`, or the `unknown` modifier)
- `unknown_word` (free text, `Mon-Fri` and similar)
- `point_in_time`, `periodic_time`
- `syntax`, `bad_char`
- `no_normal_week_rule` (only `PH off` and similar)

### Parse rates and cross-check

- **Parse rates** (targets, POIs with a tag):
  - groceries: 60,974 parsed of 61,572 tagged (99.0%); per-region medians 97.0-99.7%, minimum 79% (one city)
  - eating: 164,851 of 167,643 (98.3%); regional medians 96.1-99.6%
  - Across all 530 polygons: 98,556 distinct values, of which 3,669 are unparseable. The commonest reasons are
    `open_end` 1,388, `unknown_word` 887, `unknown_state` 400, `bad_char` 390 and `syntax` 386.
- **Cross-check against opening-hours-py**: every tag value in the 130 target polygons, weighted by POI count.

| group     | both parse   | only library | only own | neither | disagree late23 | early07     | sun12       | 24h        |
| --------- | ------------ | ------------ | -------- | ------- | --------------- | ----------- | ----------- | ---------- |
| groceries | 60,897 POIs  | 335          | 77       | 263     | 90 (0.15%)      | 80 (0.13%)  | 18 (0.03%)  | 4 (0.01%)  |
| eating    | 164,271 POIs | 1,769        | 580      | 1,023   | 720 (0.44%)     | 846 (0.52%) | 191 (0.12%) | 32 (0.02%) |

- Almost all disagreements come from one construct: `Mo, We, Fr-Su 09:00-21:00` or `Su, PH off`, a weekday list
  written with a space after the comma.
  - The library reads ", " as an additional-rule separator. It normalises the example to
    `Mo,We; Fr-Su 09:00-21:00`, which means Mo and We are open 24 h.
  - The own parser reads it as one weekday list, which is clearly what the mapper meant.
- "Only library" cases are mostly:
  - `open_end` (`11:00+`), which the library evaluates as open-ended
  - `sunrise-sunset`
  - comment-only values (the library returns "open" with a comment; I treat them as unknown and exclude them)
- "Only own" cases are tolerated typos (`Mo-Fr16:00-20:00`, `Mo - Su 11:00 - 22:00`, en-dashes).

## Sources, versions, access

- **QLever osm-planet SPARQL**: `https://qlever.cs.uni-freiburg.de/api/osm-planet`, which now 308-redirects to
  `https://qlever.dev/api/osm-planet`. Index "OpenStreetMap, PBF from
  https://planet.openstreetmap.org/pbf/planet-260921.osm.pbf, converted to RDF TTL ... using osm2rdf". Server
  `latest-master-147-g3d3ff47a9`. This is the same route and snapshot as `osm.md`, and it reuses `osm.py`'s helpers
  (`_count`, `_sparql_tsv_once`, `osm_stats`).
- **Query**: one paged query per tag (`ORDER BY ?x LIMIT 50000 OFFSET n`). Columns: id, centroid, and optional
  `opening_hours`, `brand`, `brand:wikidata` and `name`.
- **Planet feature counts**:

  | tag                | features  | with `opening_hours` |
  | ------------------ | --------- | -------------------- |
  | shop=supermarket   | 494,820   | 202,667              |
  | shop=convenience   | 840,193   | 172,616              |
  | amenity=restaurant | 1,618,999 | 377,580              |
  | amenity=cafe       | 650,252   | 164,744              |
  | amenity=fast_food  | 664,103   | 221,353              |

  86 pages, about 300 MB of TSV, in `.cache/raw/osm/qlever/planet-260921/hours/`. Query hashes are in
  `data/provenance/downloads.json` (key `...osm-planet#260921#opening_hours`).

- **Access behaviour** (external-access policy):
  - Strictly sequential, with a 3 s pause after each request.
  - **No retry on HTTP errors**: `retries=0`, so any 429/5xx/timeout raises and stops the run.
  - A row-count mismatch against the COUNT query discards the page and re-fetches it once, then stops.
  - The full pull took about 4 minutes of server time. No 429, 5xx or timeouts occurred.
- **Incident fixed in this module**: the first run stopped on `amenity=cafe` page 0 with 50,001 rows against 50,000
  expected.
  - Cause: an OSM value containing a raw carriage return. `Path.read_text()` uses universal-newline mode and split
    that row in two.
  - It was not a server problem. The module now parses cached TSVs with `newline=""` (`_tsv_rows`).
  - `osm.py` has the same latent issue. Its runs were unaffected, because the COUNT check would have failed loudly.
- Overture places carry no opening hours, so there is no independent hours benchmark. Validation therefore relies
  on internal consistency, chain stratification and the expectation checks below.

## License

OpenStreetMap: ODbL 1.0, exactly as in `osm.md`. From https://www.openstreetmap.org/copyright: "You are free to
copy, distribute, transmit and adapt our data, as long as you credit OpenStreetMap and its contributors." The ODbL
1.0 text (https://opendatacommons.org/licenses/odbl/1-0/) defines a "Produced Work" as "a work ... resulting from
using the whole or a Substantial part of the Contents (via a search or other query) from this Database". The per-city
shares are a Produced Work, and §4.3 requires a notice that "Content was obtained from the Database ... and that it is
available under this License".

**App attribution:** "© OpenStreetMap contributors", linked to https://www.openstreetmap.org/copyright (ODbL). The
cached POI tables are a Derivative Database and are not published. This module is the method (§4.6).

## Validation

### 1. Tagging coverage (tagged / all POIs), 130 targets, median [min-max] by UN SDG region

| region                  | groceries        | supermarket only | eating           | groceries parsed n (median) | eating parsed n |
| ----------------------- | ---------------- | ---------------- | ---------------- | --------------------------- | --------------- |
| Europe (23)             | 0.67 [0.21-0.93] | 0.82             | 0.53 [0.13-0.83] | 583                         | 1,887           |
| Northern America (16)   | 0.31 [0.19-0.53] | 0.56             | 0.43 [0.21-0.56] | 403                         | 2,303           |
| Australia & NZ (5)      | 0.28 [0.22-0.33] | 0.45             | 0.26 [0.22-0.28] | 198                         | 1,098           |
| E & SE Asia (22)        | 0.19 [0.02-0.78] | 0.19             | 0.16 [0.03-0.40] | 302                         | 752             |
| Latin America (16)      | 0.11 [0.05-0.28] | 0.20             | 0.10 [0.06-0.30] | 142                         | 385             |
| N Africa & W Asia (16)  | 0.11 [0.04-0.37] | 0.14             | 0.11 [0.05-0.28] | 54                          | 133             |
| Central & S Asia (16)   | 0.10 [0.03-0.30] | 0.16             | 0.13 [0.02-0.33] | 66                          | 318             |
| Sub-Saharan Africa (16) | 0.08 [0.02-0.37] | 0.14             | 0.11 [0.03-0.28] | 31                          | 79              |

- The reference set (530 centres) shows the same ordering: Europe 0.57 / 0.50, the other regions 0.06-0.41.
- **Comparison with the `osm.json` coverage flags** (median eating-tag coverage of the targets, by nightlife flag):
  - `ok`: 0.24 (83 cities)
  - `osm_low_vs_overture`: 0.16 (30)
  - `overture_low_vs_osm` (China, Iran, Cuba, East Africa): 0.09 (17)

  Cities where OSM POIs themselves are thin also have thin hours tagging. Both flags are copied into each value's
  `detail` (`osm_nightlife_coverage_flag`, `osm_culture_coverage_flag`).

### 2. Bias: chains tag more, and chains keep different hours

**Chain share of all POIs** (median): groceries Europe 0.52, E/SE Asia 0.57, N America 0.40, LatAm 0.10,
Sub-Saharan Africa 0.04. Eating 0.03-0.15 everywhere except N America 0.32.

**Tag coverage, chain vs non-chain** (target medians):

| region          | groceries chain | groceries non-chain | eating chain | eating non-chain |
| --------------- | --------------- | ------------------- | ------------ | ---------------- |
| Europe          | 0.86            | 0.41                | 0.74         | 0.52             |
| N America       | 0.46            | 0.22                | 0.54         | 0.39             |
| E/SE Asia       | 0.22            | 0.14                | 0.20         | 0.16             |
| LatAm           | 0.20            | 0.10                | 0.10         | 0.10             |
| N Africa/W Asia | 0.40            | 0.08                | 0.09         | 0.11             |
| Sub-Saharan     | 0.29            | 0.07                | 0.19         | 0.10             |

Chains are tagged about 1.5-5 times as often as non-chains. Two reasons: brand-wide edits (NSI, All-The-Places
imports) and corporate mappers.

**Chain minus non-chain rate** (percentage points, median, cities with at least 10 parsed POIs in each stratum):

- groceries late23:
  - E/SE Asia **+36** (konbini vs local shops)
  - N America +17, Sub-Saharan Africa +18, LatAm +11
  - Europe −5 (discounters close early, independent kiosks and Spätis stay open)
  - N Africa/W Asia −19
- groceries early07: +25 to +37 in Europe, Asia, N America and Australia
- groceries sun12: +4 to +17
- eating early07: N America +33, E/SE Asia +28 (breakfast chains)
- eating late23: N America +15, Australia/NZ +16, elsewhere −2 to +7

So the share of tagged POIs **is** related to the metric. The raw share over-represents chains, and in most regions
this pushes late, early and 24 h upwards.

**Correction**: post-stratify to the chain share of all POIs (definition above). Effect on the published values
(post minus raw, median [min-max] by region):

- groceries late23:
  - E/SE Asia −2.6 [−15.2, +3.3]
  - N America −1.8 [−6.5, +14.3]
  - N Africa/W Asia +1.6 [−1.5, +10.1]
  - Europe +0.5 [−1.4, +6.0]
- groceries 24h: E/SE Asia −2.7 [−16.0, +3.9]
- groceries early07: Australia/NZ and N America −3.9, Europe −2.1
- groceries sun12: −0.2 to −1.6
- eating late23: within ±0.8 in every region (chains are a small share of eateries)

Rank agreement between raw and post-stratified values, across reference centres with at least 50 parsed POIs
(Spearman):

- groceries: 0.97-0.99 (late 0.985, sun12 0.969, 24h 0.988)
- eating: 0.98-1.00

So brand selection shifts levels by a few points, mostly in chain-heavy Asian and US cities, but it does not drive
the ranking.

**Sensitivity, wider chain definition** (brand tag OR the same normalised name at least 5 times in the city): this
catches unbranded 7-Eleven, Oxxo, "Żabka" and similar. Spearman with the main post-stratified values is 0.991-1.000
for all checks.

**Choice and justification**:

- Post-stratification removes the one selection mechanism we can measure: chains are tagged more often and keep
  different hours. Its correction is small, transparent, and recorded per city (raw values are in `detail`).
- Reporting chain and non-chain metrics separately would double the number of metrics. The non-chain stratum would
  then be missing in many cities.
- Residual bias that cannot be corrected: within each stratum, the tagged POIs may still differ from the untagged
  ones, for example an active mapper community around a nightlife district.
- Within-region coverage–metric correlations have inconsistent signs (see Minimum data), so there is no evidence
  of a strong residual coverage-driven gradient. They cannot prove its absence either.

### 3. Expectation checks (published, post-stratified values)

| expectation                                                 | result                                                                                                                                                                                                                                                                                                                                                                           | holds?                                                   |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Tokyo / Osaka / Taipei / Seoul high late and 24 h groceries | Grocery late / 24h: Tokyo 79 / 73, Osaka 80 / 76, Taipei 78 / 72, Seoul 71 / 66. Also Sapporo 75 / 62, Fukuoka 79 / 71, Bangkok 78 / 77, Kaohsiung 76 / 72. E/SE Asia median 62 / 59 against Europe 12 / 4                                                                                                                                                                       | **yes**                                                  |
| DE/AT/CH very low Sunday grocery opening                    | Supermarkets, Sun 12:00: Munich 1.0%, Vienna 2.3%, Berlin 2.2%, Zurich 6.3%. All groceries: Munich 6.5%, Vienna 7.8%, Berlin 16% (Spätis), Zurich 25% (station shops). Oslo 36% and Athens 33% are also low. Most other European cities are 70-97% (Sunday trading is legal in UK, NL, Nordics, PL, CZ, HU, and in FR/IT/ES partly)                                              | **yes**                                                  |
| Spanish late dinner (eating late high, early low)           | Madrid late 57% / early 9%, Barcelona 44% / 12%. Southern Europe is similar: Athens 66 / 23, Rome 42 / 18, Milan 35 / 16, Lisbon 28 / 15. Compare London 12 / 20, Stockholm 10 / 8, Sydney 8 / 39, US median 15 / 28. Late22 shows the same contrast more strongly (Madrid 73%, Paris 61%, Minneapolis 15%)                                                                      | **yes**                                                  |
| US high 24 h groceries                                      | Only partly. Houston 55%, New York 30%, Phoenix 35%, Denver 28%, but Boston 6%, Minneapolis 4%, Chicago 11%; US/Canada median 18%. Late23 median 29% (Houston 59%, NYC 42%). Probably real: 24 h supermarkets became rarer after 2020 and many now close at 23:00/24:00. US OSM convenience shops are also under-mapped relative to chain supermarkets (groceries coverage 0.31) | **partly**                                               |
| (additional) MENA late eating                               | Riyadh 87%, Cairo 75%, Dubai 70%, Doha 81%, Baku 58%                                                                                                                                                                                                                                                                                                                             | plausible (late dining culture, hot climate)             |
| (additional) rest day                                       | Tel Aviv: Sun 12:00 98% but Sat 12:00 69% (Shabbat). Gulf cities: Fri 12:00 95%, so Friday-prayer closures are not visible at noon                                                                                                                                                                                                                                               | "Sunday" is a Christian-majority construct (see caveats) |

Anomalies to note:

- Lisbon and Milan have very low early grocery opening (Lisbon early07 2.9%). Southern-European supermarkets
  typically open at 08:00-08:30, so this is plausible.
- Durban groceries are missing: 88 chain and 3 non-chain parsed POIs, but non-chains make up 29% of POIs, so the
  value cannot be reweighted.
- Dar es Salaam groceries (1,837 parsed, chain share 0.03%) look like a mapping project or import of small shops
  ("duka"). The value is published (Sunday 58%) with coverage 18%.

## Missing values (130 targets)

| metric                              | values | missing | low-coverage flag |
| ----------------------------------- | ------ | ------- | ----------------- |
| grocery_late / early / sunday / 24h | 100    | 30      | 23                |
| supermarket_late / sunday           | 80     | 50      | 7                 |
| eating_late / early / 24h           | 112    | 18      | 37                |

- **Groceries missing** (mostly fewer than 50 parsed tags; the exact reason is in `missing` for each value):
  abidjan, addis-ababa, amman, beirut, casablanca, chennai, dakar, doha, durban, hyderabad, islamabad, karachi,
  kathmandu, kigali, kinshasa, kolkata, lagos, lahore, luanda, lusaka, maputo, marrakesh, mumbai, nairobi,
  panama-city, phnom-penh, riyadh, santiago, tunis, ulaanbaatar.
- **Eating missing**: abidjan, amman, beirut, casablanca, dar-es-salaam, islamabad, karachi, kigali, kinshasa, lagos,
  lahore, lusaka, maputo, medellin, nairobi, santo-domingo, seoul (2.8% coverage of 55,874 POIs), tunis.
- **Supermarket**: the 50 missing values additionally include most of South Asia, Africa, China, Vietnam, Cebu,
  Denpasar, Edinburgh, Reykjavik, Honolulu, Phoenix, Tbilisi and Yangon.

Coverage is concentrated in Sub-Saharan Africa, South Asia and MENA. A diagnosis using these metrics must treat
missing as "unknown", not as low.

## Known biases and caveats

- **Selection**: tagged POIs are not a random sample. The chain effect is corrected; the within-stratum selection is
  not. Errors are likely in either direction. One example: Seoul's grocery value rests on 7.7% coverage.
- **Stale tags**: OSM hours are not re-verified. Post-2020 reductions in hours (24 h chains cutting back) may lag.
  No `check_date:opening_hours` filtering is applied.
- **Threshold effects**: closing times cluster at 22:00, 23:00 and 24:00, so the 23:00 instant is sensitive.
  Example: many Indian restaurants close at 23:00, giving Bengaluru eating late23 18% but late22 66%. `late22_share`
  is in `detail`, and the choice of instant should match the quiz wording.
- **Count, not capacity**: a 24 h konbini and a 24 h hypermarket each count as 1. Urban form is not weighted.
- **Sunday** is the wrong rest day for Israel (Saturday) and partly for MENA (Friday). `sat12_share`/`fri12_share`
  are in `detail`. For a quiz the Sunday metric should be presented as "Sunday", or replaced by the
  minimum over Fri/Sat/Sun.
- **Holidays ignored**: PH/SH rules are dropped. A city with frequent holiday closures is not penalised.
- **POI definitions vary**: `shop=convenience` covers konbini, Spätis, bodegas and kiosks. Kiosk-type `shop=kiosk`
  is not included.
- **Duplicates**: no node/building de-duplication. `osm.py` found that de-duplication removes about 1% of features,
  which is negligible for shares.

## Alternatives considered

- **Overture places**: no opening hours in the schema, so it is not usable.
- **Google / Foursquare hours**: proprietary, terms forbid this use.
- **opening-hours-py as the parser**: equally valid (agreement above 99.5%). Adopt it via `uv add` if the
  orchestrator prefers a maintained full-spec implementation over the own subset parser.
- **Separate chain and non-chain metrics**: rejected in favour of one post-stratified value (see Bias). The strata
  are in `detail`.
