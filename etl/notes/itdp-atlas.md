# ITDP Atlas of Sustainable City Transport (`itdp-atlas`)

Module: `etl/soulcity_etl/itdp.py` (`cd etl && UV_SYSTEM_CERTS=1 uv run python -m soulcity_etl.itdp [--reference]`).
Output: `data/interim/itdp-atlas.json` (86 targets), `data/reference/itdp-atlas.csv` (524 centres >= 1M, all present).
New dependency: `rdata` (pure-python R .rds parser), added with `uv add`.

## Data source (what we use and why it is legitimate)

atlas.itdp.org is an R Shiny app with no static download link. Its frontend repository
**github.com/ITDP/atlas** (MIT) publishes the full data tree that the app reads (`data/data_final/…`) as **GitHub
release assets**:

| release | asset date | contents |
|---|---|---|
| `final` (2024-05-14 tag) | — | data_final.z01–z07 + .zip (~7.8 GB), the May-2024 launch data (year 2023) |
| **`update_2024`** (tag commit 2024-06-02, asset Last-Modified **2025-01-10**) | latest release | data_final.z01–z04 + data_final.zip (4.21 GB, 310,956 members); **2024 data year** |

We use `update_2024`. Instead of downloading 4.2 GB we read the zip64 central directory (the last 25 MB of `z04` plus
`data_final.zip`, which is fetched with `common.fetch`) and pull only the members we need with HTTP Range requests,
inflate them, and verify size + CRC-32 from the central directory. Members used per city:
`data_final/ghsl_<ID>/indicators_<ID>.rds` (sf data.frame: one row per analysis area, polygons + all indicators) and
`data_final/ghsl_<ID>/overlays/temp/{mrt,lrt,brt}_stations_ll_<ID>_2024.geojson` (for the station screen). All members'
sha256 + CRC are recorded under `https://github.com/ITDP/atlas/releases/tag/update_2024#data_final` in
`data/provenance/downloads.json` (2,116 members after `--reference`). Archive quirk handled in code: recorded
local-header offsets drift by −47 bytes in the second half of segment z01; the reader locates the local header whose file
name matches nearest to the recorded offset and still CRC-checks the payload.

Column semantics come from ITDP's data dictionary linked from the app's download panel
(Google Sheet `1tSE4U_yu6wKSkFnwbJjcXT2IlSSCcFeijoERVua_UMM`), the methodology page
https://atlas.itdp.org/about/about_methodology.html, and the backend code github.com/ITDP/pedestriansfirst (MIT).
Shares are stored as fractions 0–1; we multiply by 100.

### Other routes tried
- `https://atlas.itdp.org/` HTML: Shiny UI only; `robots.txt`, `sitemap.xml`, `terms.html` → 404. No terms-of-use page
  found. `about/about_data.html`, `about_atlas.html`, `about_faq.html`, `about_methodology.html` → 200 (quoted below).
- Shiny download handlers (`downloadData_cities_csv`, `downloadData2_gpkg` …) via the SockJS xhr transport
  (`/__sockjs__/<n>/<id>/xhr`, multiplex `0|o|/s=1`, Shiny `init`). It works technically, but the app expects a full
  browser input set; one probe that set only `indicator` ended with the server message *"The application unexpectedly
  exited"* (code 4503). **Abandoned**: not documented, fragile, and risk of disrupting the public service. (Disclosure:
  our probes may have triggered that restart once or a few times on 2026-10-28 ~20:40 UTC.) The GitHub release is the
  documented, bulk, machine-readable route and is what the module uses.
- Web search for Zenodo / figshare / HDX copies: none found. ITDP's data page says "For larger data extracts, contact
  data@itdp.org."

## Geography and boundary match

Methodology (General Topic 1a): *"The urban agglomerations included in the Atlas are taken from the Global Human
Settlement Layer's GHS Urban Centre Database - Stats in the City (R2024A). We include all urban agglomerations with a
population above 500,000 people."* (The older "Data & Algorithms" page still says "GHS-UCDB, we use the 2019 release";
the data itself confirms R2024A.) The Atlas id `hdc` is the zero-padded R2024A `ID_UC_G0`; member paths use it.

Crosswalk = ID (`hdc == ucdb_id`, checked per file) **plus geometric verification**: the Atlas `admin_level == "0"`
("Agglomeration") polygon vs our UCDB polygon, both in Mollweide (ESRI:54009), IoU and area ratio; acceptance IoU >= 0.5.

Results (86 targets): 85 present; **all 85 accepted, IoU min 0.9999 / median 1.0000, area ratio 0.9999–1.0001**.
Population check: Atlas `city_popdensitytotal_2025` (GHS-POP R2023A summed by ITDP in its polygon) / UCDB
`GC_POP_TOT_2025`: min 0.9927, median 0.9973, max 1.0031. Reference set (524 centres >= 1M): all 524 in the Atlas,
IoU min 0.9993, area ratio 0.9993–1.0007. I.e. the Atlas polygon *is* our polygon; values need no boundary adjustment.

Per-city table (also in `.cache/raw/itdp-atlas/boundary_match.json` after a run):

| city_id | ID_UC_G0 | Atlas name | IoU | area ratio (Atlas/UCDB) | Atlas pop 2025 / UCDB pop 2025 | RT stations / line-km | accepted |
|---|---|---|---|---|---|---|---|
| tokyo | 5929 | The Tokyo / Yokohama / Kawasaki area | 0.9999 | 1.0000 | 0.9974 | 291 / 493 | yes |
| seoul | 348 | The Seoul / Incheon / Suwon area | 1.0000 | 1.0000 | 0.9983 | 371 / 695 | yes |
| taipei | 1142 | The New Taipei / Taipei / Taoyuan area | 0.9999 | 1.0000 | 0.9955 | 86 / 192 | yes |
| singapore | 178 | The Singapore area | 0.9999 | 1.0001 | 0.9929 | 105 / 225 | yes |
| bangkok | 2315 | The Bangkok / Nonthaburi / Pak Kret area | 1.0000 | 1.0000 | 0.994 | 72 / 154 | yes |
| hanoi | 1999 | The Hanoi / Từ Sơn area | 0.9999 | 1.0000 | 0.9944 | 4 / 13 | yes |
| mumbai | 7599 | The Mumbai / Thane / Navi Mumbai area | 0.9999 | 1.0000 | 0.9951 | 15 / 48 | yes |
| dubai | 1007 | The Dubai / Sharjah / Ajman area | 0.9999 | 1.0000 | 0.9956 | 42 / 97 | yes |
| istanbul | 2637 | The Istanbul area | 0.9999 | 1.0000 | 0.999 | 203 / 332 | yes |
| cairo | 4605 | The Cairo / Giza / Shubra al Khayma area | 1.0000 | 1.0000 | 0.9965 | 75 / 104 | yes |
| lagos | 1289 | The Lagos / Ikeja area | 0.9999 | 1.0000 | 0.9927 | 11 / 37 | yes |
| nairobi | 1717 | The Nairobi area | 1.0000 | 1.0000 | 0.9939 | 0 / 0 | yes |
| cape-town | 431 | The Cape Town area | 1.0000 | 1.0000 | 0.9979 | 0 / 0 | yes |
| london | 5816 | The London / Westminster / City of London area | 1.0000 | 1.0000 | 1.0017 | 3 / 536 | yes |
| paris | 2878 | The Paris / Argenteuil / Saint-Denis area | 1.0000 | 1.0000 | 1.0001 | 510 / 820 | yes |
| berlin | 5483 | The Berlin area | 1.0000 | 1.0000 | 1.0012 | 152 / 152 | yes |
| amsterdam | 1590 | The Amsterdam area | 0.9999 | 1.0000 | 1.0013 | 19 / 43 | yes |
| copenhagen | 698 | The Copenhagen area | 1.0000 | 1.0000 | 1.0022 | 93 / 139 | yes |
| vienna | 1081 | The Vienna area | 1.0000 | 1.0000 | 1.0002 | 91 / 86 | yes |
| helsinki | 572 | The Helsinki / Vantaa area | 1.0000 | 1.0000 | 1.0029 | 37 / 67 | yes |
| reykjavik | 48 | — | — | — | — | — | no: not in Atlas release update_2024 (no data_final/ghsl_00048/indicators_00048.rds); UCDB 2025 population 206,895 is below the Atlas inclusion threshold of 500,000 (methodology, General Topic 1a) |
| lisbon | 231 | The Lisbon / Amadora / Agualva-Cacém area | 1.0000 | 1.0000 | 0.9978 | 65 / 59 | yes |
| barcelona | 5071 | The Barcelona / l'Hospitalet de Llobregat area | 0.9999 | 1.0000 | 0.9985 | 185 / 165 | yes |
| new-york | 8099 | The New York / Newark / Jersey City area | 0.9999 | 1.0000 | 0.9984 | 427 / 451 | yes |
| vancouver | 358 | The Vancouver / Surrey / Burnaby area | 0.9999 | 1.0000 | 1.0002 | 50 / 74 | yes |
| mexico-city | 5402 | The Mexico City / Ecatepec / Nezahualcóyotl area | 1.0000 | 1.0000 | 0.994 | 387 / 460 | yes |
| bogota | 3881 | The Bogota / Soacha area | 1.0000 | 1.0000 | 0.9928 | 62 / 116 | yes |
| sao-paulo | 7277 | The São Paulo / Guarulhos area | 0.9999 | 1.0000 | 0.9953 | 58 / 158 | yes |
| buenos-aires | 4443 | The Buenos Aires / Lanús / Avellaneda area | 0.9999 | 1.0000 | 0.9973 | 136 / 136 | yes |
| sydney | 2324 | The Sydney area | 1.0000 | 1.0000 | 0.9974 | 136 / 295 | yes |
| osaka | 4399 | The Osaka / Kobe / Kyoto area | 0.9999 | 1.0000 | 0.9969 | 183 / 284 | yes |
| fukuoka | 907 | The Fukuoka / Kasuga / Chikushino area | 0.9999 | 1.0000 | 0.997 | 33 / 33 | yes |
| sapporo | 351 | The Sapporo / Ebetsu area | 0.9999 | 1.0000 | 0.9988 | 35 / 49 | yes |
| shanghai | 11345 | The Shanghai / Pudong / Taicang area | 1.0000 | 1.0000 | 0.9967 | 439 / 825 | yes |
| beijing | 8745 | The Beijing / Shunyi / Mentougou area | 0.9999 | 1.0000 | 0.9981 | 395 / 809 | yes |
| hong-kong | 11185 | The Hong Kong / Kowloon area | 1.0000 | 1.0000 | 0.9965 | 77 / 137 | yes |
| ulaanbaatar | 337 | The Ulaanbaatar area | 1.0000 | 1.0000 | 1.0003 | 0 / 0 | yes |
| ho-chi-minh | 5239 | The Ho Chi Minh City / Thủ Đức / Thủ Dầu Một area | 0.9999 | 1.0000 | 0.9938 | 0 / 0 | yes |
| kuala-lumpur | 1648 | The Kuala Lumpur / Kajang / Klang area | 1.0000 | 1.0000 | 0.9946 | 14 / 191 | yes |
| jakarta | 5472 | The Jakarta / Bekasi / Tangerang area | 0.9999 | 1.0000 | 0.9937 | 120 / 383 | yes |
| manila | 2323 | The Quezon City / Manila / Caloocan area | 0.9999 | 1.0000 | 0.9945 | 0 / 0 | yes |
| new-delhi | 7963 | The Ghaziabad / Gurugram / Noida area | 1.0000 | 1.0000 | 0.9967 | 183 / 370 | yes |
| bengaluru | 9558 | The Bengaluru area | 1.0000 | 1.0000 | 0.9951 | 10 / 71 | yes |
| dhaka | 6090 | The Dhaka / Cumilla / Narayanganj area | 0.9999 | 1.0000 | 0.9958 | 16 / 19 | yes |
| kathmandu | 1822 | The Kathmandu / Bhaktapur area | 1.0000 | 1.0000 | 0.996 | 0 / 0 | yes |
| almaty | 2847 | The Almaty area | 1.0000 | 1.0000 | 0.9993 | 7 / 14 | yes |
| tehran | 5174 | The Tehran / Eslamshahr / Qods area | 1.0000 | 1.0000 | 0.9971 | 105 / 175 | yes |
| tbilisi | 467 | The Tbilisi area | 0.9999 | 1.0000 | 0.9984 | 16 / 28 | yes |
| tel-aviv | 457 | The Tel Aviv / Rishon LeZion / Petah Tikva area | 1.0000 | 1.0000 | 0.997 | 13 / 24 | yes |
| athens | 854 | The Athens / Piraeus / Peristeri area | 1.0000 | 1.0000 | 0.999 | 47 / 76 | yes |
| rome | 3938 | The Rome area | 1.0000 | 1.0000 | 0.9995 | 81 / 65 | yes |
| milan | 1498 | The Milan / Monza area | 1.0000 | 1.0000 | 0.9993 | 116 / 100 | yes |
| madrid | 3338 | The Madrid / Móstoles / Leganés area | 1.0000 | 1.0000 | 0.9982 | 251 / 287 | yes |
| zurich | 1689 | The Zurich area | 0.9999 | 1.0000 | 0.9998 | 130 / 99 | yes |
| munich | 5249 | The Munich area | 1.0000 | 1.0000 | 1.0008 | 85 / 88 | yes |
| prague | 560 | The Prague area | 1.0000 | 1.0000 | 1.0004 | 53 / 66 | yes |
| budapest | 964 | The Budapest area | 1.0000 | 1.0000 | 1.0003 | 37 / 39 | yes |
| warsaw | 3712 | The Warsaw area | 1.0000 | 1.0000 | 1.0009 | 38 / 41 | yes |
| stockholm | 1693 | The Stockholm area | 1.0000 | 1.0000 | 1.0031 | 81 / 95 | yes |
| oslo | 828 | The Oslo area | 1.0000 | 1.0000 | 1.0028 | 74 / 78 | yes |
| dublin | 394 | The Dublin area | 1.0000 | 1.0000 | 1.002 | 16 / 41 | yes |
| edinburgh | 2186 | The Edinburgh area | 1.0000 | 1.0000 | 1.0017 | 8 / 14 | yes |
| casablanca | 2102 | The Casablanca / Mohammedia area | 1.0000 | 1.0000 | 0.997 | 67 / 46 | yes |
| marrakesh | 1853 | The Marrakesh area | 1.0000 | 1.0000 | 0.9964 | 0 / 0 | yes |
| dakar | 39 | The Dakar / Guédiawaye / Pikine area | 1.0000 | 1.0000 | 0.995 | 0 / 0 | yes |
| accra | 3175 | The Accra / Tema area | 1.0000 | 1.0000 | 0.995 | 0 / 0 | yes |
| addis-ababa | 5862 | The Addis Ababa area | 1.0000 | 1.0000 | 0.9929 | 36 / 31 | yes |
| johannesburg | 3512 | The Johannesburg / Soweto / Randburg area | 1.0000 | 1.0000 | 0.9954 | 0 / 0 | yes |
| toronto | 2869 | The Toronto / Mississauga / Brampton area | 1.0000 | 1.0000 | 0.9992 | 137 / 139 | yes |
| montreal | 3700 | The Montreal / Laval / Longueuil area | 1.0000 | 1.0000 | 0.9996 | 65 / 93 | yes |
| seattle | 5098 | The Seattle / Bellevue area | 0.9999 | 1.0000 | 0.9999 | 21 / 40 | yes |
| san-francisco | 1461 | The San Jose / San Francisco / Oakland area | 0.9999 | 1.0000 | 0.9976 | 134 / 264 | yes |
| los-angeles | 2007 | The Los Angeles / Long Beach / Anaheim area | 1.0000 | 1.0000 | 0.9969 | 119 / 229 | yes |
| denver | 5932 | The Denver / Aurora / Lakewood area | 1.0000 | 1.0000 | 0.998 | 53 / 87 | yes |
| chicago | 7532 | The Chicago / Evanston / Elmhurst area | 1.0000 | 1.0000 | 0.9986 | 101 / 162 | yes |
| miami | 7168 | The Miami / Hialeah / Fort Lauderdale area | 0.9999 | 1.0000 | 0.9952 | 31 / 65 | yes |
| honolulu | 193 | The Honolulu / Waipahu / Pearl City area | 1.0000 | 1.0000 | 0.9946 | 5 / 13 | yes |
| havana | 367 | The Havana area | 1.0000 | 1.0000 | 0.995 | 0 / 0 | yes |
| lima | 2171 | The Lima / Callao area | 1.0000 | 1.0000 | 0.9943 | 32 / 66 | yes |
| quito | 2544 | The Quito / Sangolqui area | 1.0000 | 1.0000 | 0.9944 | 40 / 101 | yes |
| santiago | 2334 | The Santiago area | 1.0000 | 1.0000 | 0.9971 | 95 / 234 | yes |
| rio-de-janeiro | 7799 | The Rio de Janeiro / Duque de Caxias area | 1.0000 | 1.0000 | 0.9952 | 108 / 143 | yes |
| montevideo | 804 | The Montevideo area | 0.9999 | 0.9999 | 0.997 | 0 / 0 | yes |
| melbourne | 1747 | The Melbourne area | 0.9999 | 1.0000 | 0.9983 | 4 / 559 | yes |
| perth | 498 | The Perth / Joondalup area | 1.0000 | 1.0000 | 0.9965 | 55 / 105 | yes |
| auckland | 1147 | The Auckland area | 0.9999 | 1.0001 | 0.9983 | 0 / 0 | yes |

## Metrics (all `year: 2024`, `quality: observed`)

"observed" here means *a computed indicator taken verbatim as published by ITDP* — not a survey or official statistic.
Method common to all "People Near X": points of interest from OSM (or GTFS / Transit Explorer) are snapped to the
nearest node of an OSM walkable network (osmnx; all `highway=*` except link/motor/proposed/construction/abandoned/
platform/raceway, `service=parking_aisle|driveway|private`, `foot=no`), buffered along the network by the stated
distance, then by an absolute buffer (usually 100 m), unioned, small holes filled, and population counted from
GHS-POP (R2023A, Mollweide) inside the polygon; value = share of the agglomeration's population (methodology Appendix A).

| key | Atlas column | unit | definition (methodology / data dictionary) |
|---|---|---|---|
| `walk_services` | `walk_pns_2024` | % | People Near Services: share living within a **1 km walk of both** some healthcare (`amenity=hospital,doctors,clinic,pharmacy` or `healthcare=*` listed values) **and** some education (`amenity=school,kindergarten` or any `school=*`); 1 km network + 100 m buffer, intersection of the two isochrone sets |
| `walk_healthcare` | `walk_pnspnh_2024` | % | within 1 km walk of healthcare |
| `walk_education` | `walk_pnspne_2024` | % | within 1 km walk of education |
| `bike_protected` | `bike_pnpb_2024` | % | People Near Protected Bikeways: within 300 m walk (250 m network + 100 m) of `highway=cycleway`, `highway=path`+`bicycle=designated`, or `cycleway[:left/right/both]=track/opposite_track` |
| `bike_any` | `bike_pnpbpnab_2024` | % | as above plus `cycleway*=lane` (painted lanes) |
| `rapid_transit` | `transit_pnrt_2024` | % | People Near Rapid Transport: within 1 km walk of a BRT (Transit Explorer `brt_rating` not empty/"NOT BRT"), LRT/tram, or metro (incl. selected regional rail with <=20 min headways) station open by 2024; source Transit Explorer |
| `rapid_transit_km_per_mpop` | `transit_pnrtrtrall_2024` | km / million people | Rapid Transit to Resident Ratio (all modes) |
| `frequent_transit` | `transit_pnft_2024` | % | People Near Frequent Transport: within 500 m walk of a GTFS stop with mean headway <= 10 min between 07:00–21:00 (per-feed, feeds from MobilityData catalog whose bbox overlaps the agglomeration) |
| `sustainable_transport` | `transit_pnst_2024` | % | People Near Sustainable Transport: near protected bikeway AND (frequent OR rapid transport) |
| `car_free_places` | `walk_pncf_2024` | % | within 100 m (straight buffer) of a park/playground/pitch/forest/recreation ground or pedestrian/path/footway/cycleway (not `access=private`, not sidewalk/crossing) |
| `safe_from_highways` | `walk_pnnhighways_2024` | % | living >= 500 m from a grade-separated highway (>= 2 lanes/direction, no 4-way at-grade junctions over >= 1 km) |
| `block_density` | `city_blockdensity_2024` | blocks/km² | walkable blocks per km² (1,000 m² / mean "true" block area, polygonized walkable network) |
| `weighted_density` | `city_popdensity_2024` | people/km² | population-weighted density, Σpop²/Σpop over 1 km GHS-POP cells |

Value ranges over the 85 cities: walk_services 7.7–77.1 % (median 52.5), bike_protected 0–82.2 (9.9),
rapid_transit 0–53.9 (15.2), frequent_transit 0.7–72.7 after screen, car_free_places 5.5–81.8, weighted_density
2,498–58,222 people/km². Spot checks against common knowledge: Copenhagen 82.2 % / Helsinki 78.5 % / Stockholm 73.7 %
protected-bike access; Barcelona 53.9 % / Madrid 50.4 % / Zurich 49.3 % rapid transit; Lagos 7.7 % services.

**Data vintage.** "2024" is ITDP's data year. OSM: Geofabrik country extracts (`*-latest.osm.pbf`, script
`1.1-download_osm.R`); the exact snapshot date is not published — the script history (pedestriansfirst commit 4d2fdb2,
2024-12-20, and later versions writing `<country>_202412.osm.pbf`) indicates **~December 2024**, consistent with the
release date 2025-01-10, but treat it as "2024". Population: GHS-POP R2023A (1 km Mollweide). Transit: Transit Explorer
(lines open by 2024) and MobilityData GTFS feeds current at processing time. The live app now also shows a "2025" year
that is not in any GitHub release (repo code reads `indicator_values_2025`); we only use released data.

## Plausibility screen (values withheld as missing)

Coded in `itdp.screen()`; applied identically to the reference CSV.
1. **frequent_transit == 0 with 0 frequent stops** (`transit_pnftpoints_2024 == 0`, i.e. a feed was processed but no
   stop qualified): treated as GTFS ingestion/coverage failure → missing. Hits: amsterdam, bangkok, edinburgh, fukuoka,
   manila, melbourne, mexico-city, santiago, taipei, tokyo, zurich (Tokyo/Zurich at 0 % is not a measurement).
2. **Rapid-transit station data incomplete**: line-km > 0 but < 0.2 stations per line-km (targets' median ≈ 0.6/km;
   real systems 0.5–1.4/km). People Near Rapid Transport is computed from stations, so it collapses. Hits:
   london (3 stations / 536 km → 0.5 %), melbourne (4 / 559 → 1.0 %), kuala-lumpur (14 / 191 → 1.5 %),
   bengaluru (10 / 71 → 4.4 %). `rapid_transit_km_per_mpop` (line-based) is kept for these.
3. **sustainable_transport** is withheld whenever frequent or rapid transport is NA or screened (it would be an
   underestimate).
Cities just above the threshold with likely-incomplete stations (kept, flagged here): hanoi 0.31/km, mumbai 0.31,
jakarta 0.31, lagos 0.30, sao-paulo 0.37 (`detail.rt_stations`, `detail.rt_line_km` are in every rapid_transit value).
Low but non-zero frequent-transit values are kept but look partial: osaka 0.7 %, rio-de-janeiro 1.6 %, jakarta 1.8 %,
istanbul 2.2 %, miami 2.5 %, nairobi 1.3 % (per-feed headway calculation; ITDP notes it cannot merge stops across feeds).

## Missing (86 targets)

- **reykjavik — all metrics**: not in the Atlas (UCDB 2025 population 206,895 < 500,000 inclusion threshold).
- **frequent_transit (39 missing; 47 present)** — Atlas NA (no usable Mobility Database GTFS feed): almaty, beijing,
  bengaluru, cape-town, casablanca, dakar, dhaka, hanoi, havana, ho-chi-minh, johannesburg, kathmandu, kuala-lumpur,
  lagos, lima, marrakesh, montevideo, mumbai, new-delhi, oslo, quito, sapporo, seoul, shanghai, tbilisi, tehran,
  ulaanbaatar; screened: the 11 cities in rule 1; plus reykjavik.
- **rapid_transit (5 missing)**: bengaluru, kuala-lumpur, london, melbourne (rule 2); reykjavik.
- **sustainable_transport (40 missing)**: union of the above.
- All other metrics: only reykjavik missing (85/86).
Reference set (524): frequent_transit present for 95, rapid_transit withheld for 12, others complete.

## License

- Atlas data, https://atlas.itdp.org/about/about_data.html: *"The data in the Atlas is made available under the Open
  Database License: http://opendatacommons.org/licenses/odbl/1.0/ . Any rights in individual contents of the database
  are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/ ."* Code (atlas,
  pedestriansfirst): MIT.
- ODbL 1.0 (https://opendatacommons.org/licenses/odbl/1-0/) — commercial use allowed; obligations:
  - §4.3 Produced Work notice: *"if you Publicly Use a Produced Work, You must include a notice … aware that Content was
    obtained from the Database … and that it is available under this License."* Example text: *"Contains information
    from DATABASE NAME, which is made available here under the Open Database License (ODbL)."*
  - §4.4 Share-alike: *"Any Derivative Database that You Publicly Use must be only under the terms of: i. This License
    …"*; §4.4b: *"Extraction or Re-utilisation of the whole or a Substantial part of the Contents into a new database is
    a Derivative Database"*; §4.6: offer the derivative database or the method of alteration in machine-readable form.
- **Verdict**: redistribution of the derived values and commercial use are permitted. Our `data/interim/itdp-atlas.json`
  / reference CSV (an extract of 13 indicators × 524 centres) should be treated as an ODbL Derivative Database: if the
  repo or app publishes these values, that file must be offered under ODbL (not CC BY / proprietary) with this module
  as the alteration method (§4.6), and the quiz UI must carry a notice. Mixing it into a combined city table makes that
  table ODbL-share-alike only if it is a Derivative Database of the Atlas; keeping the Atlas columns in a separate
  ODbL-licensed file and the quiz output as a Produced Work (notice only) is the clean option.
- Required attribution text (UI + data file): *"Contains information from the Atlas of Sustainable City Transport
  (ITDP, atlas.itdp.org, release update_2024), which is made available under the Open Database License (ODbL). Based on
  OpenStreetMap data © OpenStreetMap contributors (ODbL), GHSL © European Union (CC BY 4.0), Transit Explorer and
  MobilityData GTFS."* Citation requested by ITDP: Reich, D. T. & Braga, K., ITDP (2024). Atlas of Sustainable City
  Transport. atlas.itdp.org. Accessed 2026-10-28.
- Upstream inputs: OSM is ODbL (the Atlas is a derived database of OSM, hence its ODbL); GHSL CC BY 4.0; GTFS feed
  licenses vary by operator; Transit Explorer is "viewed for free online or purchased for download" — ITDP publishes
  only derived shares/km, which we use.

## Known biases / caveats

- **OSM completeness**: services, bikeways and car-free places depend on OSM tagging. Under-mapping of clinics,
  pharmacies and schools in parts of Africa and South/Southeast Asia (e.g. Lagos 96 healthcare points for 12.5 M people)
  biases `walk_services` downward there; heavily mapped cities (Germany, Nordics) look better partly due to mapping
  effort. The inclusive "any school / any healthcare" rule ignores capacity and quality (a pharmacy counts as healthcare).
- **Protected-bike tagging** varies by community (separately mapped `highway=cycleway` vs `cycleway=track`); shared
  paths in parks count as protected bikeways.
- **Frequent transit** requires an open GTFS feed in the MobilityData catalog; informal transport (matatus, minibuses)
  is absent; per-feed headway calculation underestimates corridors served by several agencies.
- **Rapid transit** uses Transit Explorer coverage and ITDP's mode rules (most suburban/regional rail and non-certified
  BRT excluded) — Tokyo 13.5 % (291 stations on 493 km) likely reflects that most JR/private commuter rail is not counted.
- Walk distances use network snapping to nearest node (overstates access for points inside large blocks).
- The agglomeration is the GHSL urban centre (built-up core); suburbs outside it are not included — consistent with our
  city definition.

## Validation performed

- ID crosswalk + geometry: 85/85 IoU >= 0.9999; 524/524 reference IoU >= 0.9993 (above).
- Population consistency vs UCDB: ratio 0.993–1.003.
- Archive integrity: every member CRC-32 and size checked; sha256 recorded.
- Internal consistency screen (above) found 11 + 4 failing values; examples cross-checked by inspecting the raw columns
  (London `transit_pnrtkmmrt_2024` = 508 km with 3 stations in the overlay; Tokyo `transit_pnftpoints_2024` = 0).
- Not done: independent recomputation from OSM (see alternatives).

## Alternatives considered

- **Compute the indicators ourselves from OSM** (pedestriansfirst is MIT and runnable): needs per-city OSM extracts
  (Geofabrik is unreachable from this environment; Overpass mirror maps.mail.ru could serve ~86 bboxes but full walk
  networks for Tokyo/Jakarta-scale centres are hundreds of MB each), osmnx network isochrones and GHS-POP; days of
  compute for 86 cities and still OSM-biased. Not cheap → not implemented. A cheaper proxy (Euclidean 1 km buffers around
  OSM healthcare ∩ education points × GHS-POP 100 m) is feasible in a few hours if an independent check is wanted.
- **Shiny download buttons**: rejected (see above).
- **`final` release (2023 data)**: older; `update_2024` supersedes it.
- **People Near Transit (Verbavatz & Barthelemy 2020, figshare)**: OECD-only, different boundaries; not used.
