# OpenStreetMap culture / nightlife venues (`osm`)

Module: `etl/soulcity_etl/osm.py` (`cd etl && UV_SYSTEM_CERTS=1 uv run python -m soulcity_etl.osm`)
Output: `data/interim/osm.json` (86 targets), `data/reference/osm.csv` (530 centres = 524 reference centres with
pop >= 1M plus the 6 smaller targets). Validation summary: `.cache/raw/osm/validation_summary.json` (regenerated per run).

Diagnosis question: "Do you want lots of museums, theatres, live venues (and maybe clubs/bars) around you?"

## Recommendation (summary)

| metric                      | recommendation                                                                               | why (numbers below)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `culture_venues_per_km2`    | **adopt as `estimated`** (primary culture metric). Treat Jakarta and Lagos as low confidence | Rank agreement with two independent sources: Spearman 0.86 with Overture museum+cinema density, 0.88 with Wikidata notable culture-venue density. The OSM/Overture ratio has no regional gradient (regional medians 0.37 to 0.67). Coverage noise (log10 SD 0.20) is about half the spread of the metric (log10 SD 0.39). Only 2 of 86 cities have OSM at least 2x below the typical ratio                                                                                                                                                                                                                                       |
| `culture_venues_per_100k`   | secondary / diagnostic only                                                                  | Same counts. Per-capita does not match "around you" (see Normalisation)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `nightlife_venues_per_km2`  | **reject for the diagnosis, or restrict to cities flagged `ok` and use only coarse bins**    | The OSM/Overture bar+club ratio has a systematic regional bias. Medians: Europe 0.61, Australia/NZ 0.57, Northern America 0.51, but Eastern & South-Eastern Asia 0.25, N. Africa & W. Asia 0.28, Latin America 0.32. 20 of 86 cities have OSM at least 2x below the typical ratio (Bangkok, Hanoi, Ho Chi Minh, Jakarta, Kuala Lumpur, Mexico City, São Paulo, Rio, Lima, Istanbul, Mumbai, New Delhi, Taipei, Hong Kong, Sapporo, Rome, Miami, Cairo, Johannesburg, Lagos). Using it as-is would push Asian and Latin American cities down in a "nightlife" ranking because of mapping effort, not because they have fewer bars |
| `nightlife_venues_per_100k` | reject (same reason)                                                                         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

All four metrics are written with `quality: "estimated"`, not `observed`. An OSM POI count is a lower bound of unknown
completeness. Here it is used as a proxy for "venue density", so the assumption is that completeness is
comparable across cities. That assumption holds roughly for culture and fails for nightlife. Each value carries
`detail.coverage_flag`:

- `ok`
- `osm_low_vs_overture`: OSM/Overture ratio < 1/2 of the 86-city median, so OSM probably undercounts by at least 2x relative to peers
- `overture_low_vs_osm`: ratio > 2x the median. Overture is sparse here, so OSM cannot be checked against it. This
  happens where Meta/Facebook data is weak or blocked: Beijing, Shanghai, Tehran, Havana, Addis Ababa, Nairobi, Dakar, Accra
- `unverified_overture_sparse`: fewer than 10 Overture venues. Did not occur.

The detail also carries the Overture density, so a downstream ensemble (for example the geometric mean of the
OSM and Overture densities) is possible without re-running anything. I did not build that ensemble. It would be
a separate, modelled metric.

## Metric definitions

- **culture venues**: OSM features (node, way or relation) tagged with any of
  `tourism=museum`, `tourism=gallery`, `amenity=theatre`, `amenity=arts_centre`, `amenity=cinema`,
  `amenity=music_venue`, `amenity=concert_hall`.
- **nightlife venues**: `amenity=nightclub`, `amenity=bar`, `amenity=pub`.
- `*_venues_per_km2` = de-duplicated count of features whose centroid falls inside the GHS-UCDB R2024A urban-centre
  polygon, divided by `GC_UCA_KM2_2025`. Unit: venues per km².
- `*_venues_per_100k` = the same count divided by `GC_POP_TOT_2025`, times 1e5. Unit: venues per 100,000 residents.
- Observation date: OSM planet `planet-260921.osm.pbf` (2026-09-21), so `year: 2026`.
- Geographic unit: exactly the UCDB polygon. Points are tested with `shapely.contains_xy` against the EPSG:4326
  polygon, so there is no boundary mismatch. Ways and relations are represented by the centroid of their full
  geometry (`geof:centroid`, the same thing as Overpass `out center`).
- De-duplication: within a group, features with the same normalised name (NFKD, lowercase, punctuation stripped)
  within 150 m count once. This catches a museum mapped both as a node and as its building. Unnamed features always
  count. Effect: the median city keeps 98.7% (culture) and 99.7% (nightlife) of raw features; the minimum is 94%.
  Raw per-tag counts are in `detail.raw_counts`.

### Tag set: wiki status checked on wiki.openstreetmap.org (raw `Tag:` pages)

| tag                  | wiki status | wiki description / note                                                                         | planet count |
| -------------------- | ----------- | ----------------------------------------------------------------------------------------------- | ------------ |
| tourism=museum       | approved    | "an institution with exhibitions on scientific, historical, cultural topics"                    | 111,214      |
| tourism=gallery      | approved    | "displays a variety of visual art exhibitions" (commercial sale galleries should be `shop=art`) | 22,425       |
| amenity=theatre      | approved    | "live performances occur, such as plays, musicals and formal concerts"                          | 53,338       |
| amenity=arts_centre  | de facto    | "a venue where a variety of arts are performed or conducted"                                    | 28,540       |
| amenity=cinema       | approved    | "a movie theater"                                                                               | 31,599       |
| amenity=music_venue  | in use      | "an indoor place to hear live music which is not a theatre"                                     | 861          |
| amenity=concert_hall | in use      | rare. Most concert halls are `amenity=theatre` + `theatre:type=concert_hall`, already counted   | 233          |
| amenity=nightclub    | approved    | "a place to dance and drink at night"                                                           | 24,324       |
| amenity=bar          | de facto    |                                                                                                 | 244,140      |
| amenity=pub          | de facto    |                                                                                                 | 199,719      |

Considered and excluded:

- `amenity=library`: not what the question asks.
- `amenity=events_venue` (36k): mostly wedding and banquet halls.
- `tourism=attraction`: too generic.
- Lifecycle-prefixed tags (`disused:amenity=...`): closed venues. They use a different key, so they are excluded
  automatically.

### Normalisation: per km² vs per 100k

The question is about opportunities _around you_. That is a spatial density: how many venues are within walking or
transit distance. The UCDB urban centre is itself defined by a density threshold (contiguous 1 km² cells of at least
1,500 inhabitants per km²), so its area is close to the built-up area and venues/km² is a fair "how dense is the
offer near me" measure. Per 100k residents measures supply per person, which rewards small, rich cities with a
regional catchment (top per 100k: Zurich 37.7, Reykjavik 35.8, Prague 32.8). It says little about what is near you
in a 30-million-person agglomeration. The two rank cities similarly (Spearman 0.83 for culture, 0.91 for
nightlife), but per km² is the one that matches the question. Ranges across the 86 cities:

- culture: 0.017/km² (Dhaka) to 1.65/km² (Vienna)
- nightlife: 0.006/km² (Dhaka) to 5.26/km² (Barcelona)

## Sources, versions, access

- **OSM via QLever osm-planet**: `https://qlever.cs.uni-freiburg.de/api/osm-planet` (University of Freiburg).
  Index name, as reported by `?cmd=stats`: "OpenStreetMap, PBF from
  https://planet.openstreetmap.org/pbf/planet-260921.osm.pbf, converted to RDF TTL ... using osm2rdf". Server
  `latest-master-147-g3d3ff47a9`.
  - One SPARQL query per tag, paged at 50,000 rows with `ORDER BY ?x`.
  - Before paging, a `COUNT` query fixes the expected number of rows. Any page whose row count does not match is
    discarded and fetched again. QLever and proxy responses were seen to be silently truncated at about 1 MB.
  - Queries run one at a time with a 3 s pause, and back off exponentially on 429 or 5xx.
  - Raw TSVs: `.cache/raw/osm/qlever/planet-260921/`. The query sha256 prefixes are recorded in
    `data/provenance/downloads.json` (key `...osm-planet#260921`).
- **Why not Overpass**: when this was built (2026-10-28):
  - `overpass-api.de` was unreachable.
  - `maps.mail.ru/osm/tools/overpass` answered `/status` but every query returned 504 or
    "Dispatcher_Client::request_read_and_idx::timeout. The server is probably too busy".
  - `overpass.kumi.systems` and `overpass.private.coffee` timed out.
  - `overpass.openstreetmap.fr` returned 403, `overpass.osm.jp` has an expired TLS certificate, and
    `overpass.openstreetmap.ru` reset the connection.

  QLever serves the same planet data with a stated snapshot date.

- **Snapshot consistency check against the live OSM API** (`api.openstreetmap.org/api/0.6/map`, three small boxes,
  nodes and ways with a centroid in the box): Reykjavik centre 92 live vs 92 in the snapshot, Nairobi CBD 18 vs 17,
  Bangkok Silom 96 vs 96. The extraction is faithful and the 5-week-old snapshot is current.
- **Wikidata via QLever** (`https://qlever.cs.uni-freiburg.de/api/wikidata`): "Complete Wikidata, TTL ...
  latest-all.ttl.bz2 from 10.08.2026 ..., updated LIVE". Because the index is updated live, a re-run with an empty
  cache can differ slightly. The cache directory is keyed by a hash of the index name.
- **Overture Maps places**: release `2026-10-21.0`,
  `s3://overturemaps-us-west-2/release/2026-10-21.0/theme=places/type=place/*.parquet`. Read anonymously with duckdb
  httpfs, using a bbox filter per target polygon, then point-in-polygon. Cached CSVs:
  `.cache/raw/osm/overture/2026-10-21.0/`. The `sources.dataset` values seen are Meta, Microsoft/"Overture",
  BrightQuery, Foursquare, AllThePlaces, PinMeTo, Uberall, DAC and OpenTravel. There is **no OSM** among them, so the
  comparison is independent.

## Licenses

- **OpenStreetMap: ODbL 1.0.** From https://www.openstreetmap.org/copyright: "OpenStreetMap is open data, licensed
  under the Open Data Commons Open Database License (ODbL) by the OpenStreetMap Foundation (OSMF). ... You are free to
  copy, distribute, transmit and adapt our data, as long as you credit OpenStreetMap and its contributors." and
  "Where you use OpenStreetMap data, you are required to ... Provide credit to OpenStreetMap by displaying our
  attribution notice. Make clear that the data is available under the Open Database License."

  The ODbL 1.0 legal text (https://opendatacommons.org/licenses/odbl/1-0/) defines a "Produced Work" as "a work
  (such as an image, audiovisual material, text, or sounds) resulting from using the whole or a Substantial part of
  the Contents (via a search or other query) from this Database". Per-city counts and densities are a Produced Work.
  §4.3: "if you Publicly Use a Produced Work, You must include a notice associated with the Produced Work reasonably
  calculated to make any Person that uses, views, accesses, interacts with, or is otherwise exposed to the Produced
  Work aware that Content was obtained from the Database ... and that it is available under this License."

  The intermediate files (the extracted POI tables under `.cache/`) would be a Derivative Database (§4.6: if
  publicly used, the database or the method of making it must be offered). They are not published. This module
  is the method.

  **Required attribution in the app:** "© OpenStreetMap contributors", linked to https://www.openstreetmap.org/copyright,
  with a statement that the data is available under the ODbL.

- **Wikidata: CC0.** From https://www.wikidata.org/wiki/Wikidata:Licensing: "All structured data from the main, Property,
  Lexeme, and EntitySchema namespaces is available under the Creative Commons CC0 License". Used for validation only.
- **Overture places**, from https://docs.overturemaps.org/attribution/:
  - "Data from Meta. Available under CDLA Permissive 2.0", and the same for Microsoft, PinMeTo, Krick, RenderSEO, DAC,
    BrightQuery, Birdeye, Uberall and OpenTravel Alliance.
  - "Data from Foursquare ... Available under Apache 2.0".
  - "Data from AllThePlaces. Available under CC0 1.0".

  Used for validation only. Nothing from Overture is part of the metric value. Only its counts appear in
  `detail.coverage`, so it does not need display attribution unless those diagnostics are shown.

## Validation

### 1. Wikidata recall (notable venues)

- **Benchmark**: Wikidata items that are an instance of a subclass of museum (Q33506), theatre building (Q24354) or
  concert hall (Q1060829), and that meet all of these conditions:
  - have coordinates (P625)
  - have no dissolution date (P576) or closing date (P3999)
  - have at least one Wikimedia sitelink
  - are not `part of` (P361) another item of the same class. This drops, for example, the individual buildings of
    Skansen and the rooms of Versailles, which made the unfiltered Stockholm benchmark meaningless (243 of 334
    items unmatched, most of them Skansen sub-buildings).
- **Benchmark size**: 17,388 items lie inside the 530 polygons, and 8,311 of the 10,448 inside the 86 targets are
  "notable".
- **Match**: an item counts as found when an OSM culture feature (any of the 7 culture tags, anywhere on the planet)
  meets either condition:
  - (a) its `wikidata=` tag equals the QID, or it is the OSM object named in the item's P11693/P10689/P402
  - (b) it lies within 250 m and its `name` or `name:en` matches any label or alias of the item: exact match,
    containment, or difflib ratio >= 0.75 after normalisation
- **Target-city totals**: 4,992 items matched by link and 1,502 by name. A further 851 unmatched items are linked
  from _some_ OSM object that lacks a culture tag, typically `historic=*`, `building=*` or `tourism=attraction`.
  Those venues are mapped but invisible to this metric.

| region (UN SDG)              | recall, 524+6 centres (median [min–max], n with >= 5 notable items) | recall, 86 targets     |
| ---------------------------- | ------------------------------------------------------------------- | ---------------------- |
| Europe                       | 0.71 [0.36–0.89], n=50                                              | 0.71 [0.36–0.84], n=23 |
| Northern America             | 0.66 [0.48–0.80], n=31                                              | 0.67 [0.57–0.80], n=11 |
| Eastern & South-Eastern Asia | 0.68 [0.20–1.00], n=66                                              | 0.72 [0.47–0.92], n=17 |
| Latin America & Caribbean    | 0.67 [0.20–1.00], n=51                                              | 0.70 [0.48–0.88], n=10 |
| Sub-Saharan Africa           | 0.66 [0.20–0.89], n=12                                              | 0.71 [0.57–0.89], n=6  |
| N. Africa & W. Asia          | 0.60 [0.25–1.00], n=31                                              | 0.64 [0.40–0.79], n=7  |
| Central & Southern Asia      | 0.60 [0.22–1.00], n=31                                              | 0.67 [0.50–0.70], n=7  |
| Australia & NZ               | 0.58 [0.42–0.66], n=5                                               | 0.58 [0.42–0.66], n=4  |

Reading:

- Notable culture institutions are found in OSM's culture tag set about 60–70% of the time in every region. There is
  no Europe-versus-Global-South gradient.
- Part of the remaining 30–40% is matcher limitation: cross-script names, Wikidata coordinates off by more than
  250 m, and venues tagged differently in OSM. So these recall values are lower bounds.
- Only 12 Sub-Saharan centres have at least 5 notable Wikidata items. Wikidata itself is thin there, so this test
  says little about the long tail. Test 2 covers that.

### 2. Overture places: OSM/Overture count ratio (86 targets)

Overture uses `confidence >= 0.5` and excludes `operating_status = permanently_closed`. Categories are paired as
follows:

| pair            | Overture `basic_category`                          | OSM tags                                                |
| --------------- | -------------------------------------------------- | ------------------------------------------------------- |
| museum          | museum                                             | tourism=museum                                          |
| cinema          | movie_theater                                      | amenity=cinema                                          |
| performing_arts | theatre_venue, performing_arts_venue, music_venue  | amenity=theatre, arts_centre, music_venue, concert_hall |
| gallery         | art_gallery (includes commercial galleries)        | tourism=gallery                                         |
| bar_pub         | bar (includes pub, wine, cocktail and hookah bars) | amenity=bar, pub                                        |
| nightclub       | dance_club                                         | amenity=nightclub                                       |

**Culture comparison basis**: the culture comparison uses **museum + cinema**, the two categories defined the same
way in both sources. Overture's performing-arts and gallery categories come largely from self-categorised Facebook
pages and are inflated. For example, Ho Chi Minh City has 1,469 Overture "performing arts" venues against 27 in
OSM, and Tokyo has 5,733 against 408, because cafés with live music, karaoke and event companies get those
categories. The Overture gallery category also includes sale galleries. Ratios for those pairs are reported in the
detail but not used for flags.

| region                      | museum+cinema OSM/Overture (median [min–max]) | museum only | bar+pub+club OSM/Overture |
| --------------------------- | --------------------------------------------- | ----------- | ------------------------- |
| Europe (23)                 | 0.51 [0.29–0.65]                              | 0.53        | **0.61** [0.20–0.79]      |
| Australia & NZ (4)          | 0.41 [0.30–0.60]                              | 0.42        | 0.57 [0.51–0.66]          |
| Northern America (11)       | 0.37 [0.27–0.49]                              | 0.41        | 0.51 [0.14–0.75]          |
| Eastern & SE Asia (17)      | 0.48 [0.20–1.17]                              | 0.54        | **0.25** [0.12–1.78]      |
| Latin America (10)          | 0.53 [0.27–2.33]                              | 0.61        | **0.32** [0.08–1.83]      |
| N. Africa & W. Asia (7)     | 0.42 [0.30–0.64]                              | 0.51        | **0.28** [0.16–0.64]      |
| Central & Southern Asia (7) | 0.55 [0.23–1.85]                              | 0.71        | 0.44 [0.14–0.55]          |
| Sub-Saharan Africa (7)      | 0.67 [0.17–2.05]                              | 0.50        | 1.13 [0.11–3.04]          |

Values above 1 are cities where Overture is sparse: China (no Meta data), Iran, Cuba, Ethiopia, Kenya, Senegal and
Ghana.

Signal versus coverage noise across the 86 cities, using log10 standard deviations:

|                                                           | culture (museum+cinema) | nightlife          |
| --------------------------------------------------------- | ----------------------- | ------------------ |
| Spearman, OSM density vs Overture density                 | 0.864                   | 0.810              |
| SD of log10 OSM density                                   | 0.387                   | 0.569              |
| SD of log10(OSM/Overture)                                 | 0.20                    | 0.31               |
| OSM/Overture p10 / p50 / p90                              | 0.29 / 0.44 / 0.67      | 0.15 / 0.48 / 0.77 |
| OSM density p90/p10                                       | 8.1x                    | 18.5x              |
| Spearman, OSM culture density vs Wikidata notable density | 0.883                   | –                  |

- **Culture**: the ratio's variance is at most (0.20/0.387)² ≈ 27% of the metric's variance. That is an upper bound,
  because the ratio also contains Overture's own errors. The noise is **not regionally structured**.
- **Nightlife**: the noise share is (0.31/0.569)² ≈ 30%, so similar in size, but it **is** regionally structured. That
  is the reason for rejecting nightlife.
- Example: Mexico City has 489 OSM bars against 5,774 in Overture (ratio 0.08), and São Paulo 1,238 against 10,842
  (0.11). Barcelona's ratio is 0.59 and Berlin's 0.79.
- Near-zero nightlife in Tehran (0.007/km²) and Dhaka (0.006/km²) is real, not a coverage artefact: alcohol is
  restricted there, and Overture is also near zero.

### 3. Per-city flags

| flag                  | culture                                                 | nightlife                                                                                                                                                                                          |
| --------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `osm_low_vs_overture` | Jakarta (OSM/Overture 0.20), Lagos (0.17)               | bangkok, cairo, hanoi, ho-chi-minh, hong-kong, istanbul, jakarta, johannesburg, kuala-lumpur, lagos, lima, mexico-city, miami, mumbai, new-delhi, rio-de-janeiro, rome, sao-paulo, sapporo, taipei |
| `overture_low_vs_osm` | addis-ababa, beijing, havana, nairobi, shanghai, tehran | accra, addis-ababa, beijing, dakar, havana, nairobi, shanghai                                                                                                                                      |
| `ok`                  | the other 78 cities                                     | the other 59 cities                                                                                                                                                                                |

## Missing values

None. All 86 targets have all four metrics (0% missing). Low-confidence cities are flagged in `detail.coverage_flag`;
their values are not removed.

## Known biases and caveats

- OSM records presence, not size or quality. The Louvre and a two-room local museum each count as 1. A "lots of
  culture" reading is a count of venues, not of cultural weight.
- `tourism=museum` includes small heritage rooms and local history collections, and tagging practice varies by
  country.
- Cinemas are chain multiplexes in some countries and many single screens in others.
- Completeness differs by tag. Museums are mapped best: the OSM/Overture museum ratio has a regional median of
  0.41–0.71. Bars are the most uneven category.
- Wikidata recall measures notable institutions. The long tail (small bars, galleries) is only checked through
  Overture, and Overture has its own biases: strong where Facebook pages are common, weak or absent in
  China, Iran and Cuba.
- Both sources were captured within the same 5-week window (OSM 2026-09-21, Overture 2026-10-21, Wikidata dump of
  2026-08-10 updated live).
- Culture densities in very large, low-density-edge polygons (Tokyo 5,165 km², Jakarta, Dhaka) are diluted by
  peripheral area. That is inherent to the "per km² of urban centre" definition.

## Alternatives considered

- **Overpass API**: preferred, but unavailable (see Sources). The QLever result was verified against the live API.
- **Geofabrik extracts**: `download.geofabrik.de` is not reachable. Planet PBF from planet.openstreetmap.org (over
  80 GB) is too big for the shared 30 GB disk.
- **Overture places as the primary metric**: CDLA-Permissive. Coverage is denser everywhere except China, Iran and
  Cuba, but categories are self-assigned and noisy (performing arts and galleries above). It could serve as a second
  estimator in an ensemble and would need its own module and notes.
- **Wikidata counts as the metric**: notable-only. OSM culture count / Wikidata items has a median of 3.3 and a
  range of 0.7–29 across targets. Wikidata's regional completeness is also unknown, so it is kept as a validation
  benchmark only.
