# GHS-UCDB R2024A natural-hazard exposure (`ghsl-hazard`)

Module: `etl/soulcity_etl/hazard.py` (`cd etl && UV_SYSTEM_CERTS=1 uv run python -m soulcity_etl.hazard`; about 10 s
once the UCDB gpkg is cached). The run writes the files below and then prints the validation numbers quoted in §5.

| Output                           | Content                                                      |
| -------------------------------- | ------------------------------------------------------------ |
| `data/interim/ghsl-hazard.json`  | 6 metrics for the 130 target cities                          |
| `data/reference/ghsl-hazard.csv` | the same metrics for the 524 centres with pop ≥ 1M           |

Why a new source_id: the hazard metrics read different UCDB themes, and they have their own upstream licences
(one of them non-commercial, §1). A separate module avoids changing `ghsl.py` output. It reads the same gpkg
through `cities.ucdb_gpkg()`, so `inputs` lists the same UCDB URL plus the licence documents fetched in §1.

Quiz question: 「地震・洪水・台風などの自然災害が少ない街がいい？」. For every metric, **lower = fewer hazards**.

## 1. Inputs and licences

Only documented routes were used: the UCDB zip that was already cached, plus licence and metadata files from the
JRC FTP (directory listings and `.txt` files) and the Zenodo REST API (`/api/records/<id>`, which is documented).
Every file was fetched with `common.fetch()` and is recorded in `data/provenance/downloads.json`.

| Hazard (UCDB columns)                        | Upstream dataset (as cited in the fact sheets)                                                                                                                                                                                  | Licence as read (quoted)                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| all (UCDB itself, GHS-POP R2023A)            | GHS-UCDB R2024A V1.2, doi:10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd                                                                                                                                                         | GHSL `copyright.txt`: _"Any copyright and/or sui generis right on the dataset is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence"_ (see `ghsl-ucdb.md`)                                                                                                                                                                                                                                                                                                 |
| Earthquake (EX_E01..E10_POP, EX_SHA_POP)     | GEM Global Seismic Hazard Map v2023.1 (Johnson et al. 2023), doi:10.5281/zenodo.8409647                                                                                                                                         | Zenodo record 8409647 API: `"license": {"id": "cc-by-nc-sa-4.0"}`, i.e. **CC BY-NC-SA 4.0 (non-commercial, share-alike)**                                                                                                                                                                                                                                                                                                                                                                   |
| River flood (EX_010/100_POP/SHP)             | Baugh et al. 2024, "Modelled flood inundation for different return period scenarios at the global scale", https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard/                                            | `flood_hazard/copyright.txt`: _"Any copyright and/or sui generis right on the dataset is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence … Reuse is allowed provided appropriate credit is given and any changes are indicated."_ The same folder's `README.txt` (A02) says instead: _"License information, restrictions on use: Open Data Commons Open Database License v1.0"_. **The two statements conflict.** Both allow reuse with attribution. |
| Coastal flood (EX_CF1/CF2_POP/SHP)           | Vousdoukas et al. 2018 (Nat. Commun. 9, 2360) and Dottori et al. 2016; JRC LISFLOOD-FP coastal extent                                                                                                                           | The fact sheets give no download URL. JRC publishes its coastal datasets under `jrc-opendata/LISCOAST/`, and that folder's `copyright.txt` is the same CC BY 4.0 text. **We did not identify the exact sub-folder UCDB used.**                                                                                                                                                                                                                                                               |
| Tropical cyclone occurrence (HZ_CEV_TCY)     | MYRIAD-HES (Claassen et al. 2023, Sci Rep 13, 13808), doi:10.5281/zenodo.8269680                                                                                                                                                | Zenodo record 8269680 API: `"license": {"id": "cc-by-4.0"}`. `METADATA.pdf`: _"License Creative Commons Attribution 4.0 International"_                                                                                                                                                                                                                                                                                                                                                   |
| (rejected) Cyclone wind (EX_*_S1P/S3P)       | STORM wind-speed return periods v4, doi:10.4121/12705164.v4                                                                                                                                                                     | Not read. The DOI resolves to `data.4tu.nl/datasets/0ea98bdd-…/4`, and one curl to the data.4tu.nl API ended in a connection reset at the agent proxy (`ws_closed_mid_exchange`, 2026-10-29 03:24 UTC). Following the access policy we stopped and did not retry.                                                                                                                                                                                                                             |

**Licence verdict.** River flood, coastal flood and tropical-cyclone metrics: CC BY 4.0 (the GloFAS README names
ODbL instead; both allow reuse with attribution). **The earthquake metrics derive from a CC BY-NC-SA 4.0 map.**
JRC redistributes UCDB under CC BY 4.0. Even so, the UCDB earthquake columns are adapted material of GEM's map, and
the conservative reading is that NC and SA carry through. The derived numbers are then fine for a non-commercial
quiz that gives attribution, and they should be shared under the same terms. Commercial use needs GEM's permission.
**The orchestrator or the user must decide on this.**

Attribution text to show: "Hazard exposure: European Commission JRC, GHS-UCDB R2024A (CC BY 4.0), using GEM Global
Seismic Hazard Map v2023.1 (© GEM Foundation, CC BY-NC-SA 4.0), CEMS GloFAS flood hazard maps, JRC coastal flood
maps (Vousdoukas et al. 2018) and MYRIAD-HES (Claassen et al. 2023, CC BY 4.0). Derived by soul-city: shares,
pop-weighted MMI excess and per-year cyclone counts."

## 2. Column dictionary (EXPOSURE and HAZARD_RISK themes)

Page numbers are the printed page in `GHSL_UCDB_R2024_V1_2.pdf`, with the PDF page index in brackets.
"Epochs" means the population/built-up epoch. Every hazard map is static: a single snapshot, reused for all epochs.
`ID` is the code inside `EX_<ID>_<metric>_<epoch>`.

### 2.1 Exposure (section 2.9.5, pp.164–301 [168–305]): hazard map × GHS-POP / GHS-BUILT-S zonal sums

| Columns                                     | Hazard and threshold (from the fact sheet)                                                                                                                                                       | Metric                                                                   | Epochs         | Upstream             | Doc                       |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ | -------------- | -------------------- | ------------------------- |
| EX_010_POP, EX_100_POP                      | River flood, 10-yr / 100-yr return period. Method: _"masked by the 10 yrp flood hazard map (1 - flood, 0 - no flood)"_, i.e. any depth counts                                                    | inhabitants                                                              | 1975–2030 (5y) | Baugh et al. 2024    | p.164–165 [168–169]       |
| EX_010_SHP, EX_100_SHP                      | same                                                                                                                                                                                             | % of UC population                                                       | same           | same                 | p.166–167 [170–171]       |
| EX_010/100_BUS, _SHB, _NRE, _SNR            | same                                                                                                                                                                                             | built-up m², % built-up, non-residential m², %                           | same           | + GHS-BUILT-S R2023A | p.168–175 [172–179]       |
| EX_E01, E02, E04 … E10 _POP                 | Earthquake: population in GEM hazard class MMI 1, 2–3, 4, 5, 6, 7, 8, 9, 10 (classes are exclusive)                                                                                              | inhabitants                                                              | same           | GEM GSHM 2023.1      | p.176–184 [180–188]       |
| EX_SHA_POP                                  | Earthquake, class ≥ 6 MMI                                                                                                                                                                        | % of UC population                                                       | same           | same                 | p.185 [189]               |
| EX_E*_BUS, EX_E*_NRE, EX_SHA_BUS, EX_SHA_RES | same, for built-up / non-residential. The p.205 sheet is titled "EX_SHA_RES" but the column in the file is EX_SHA_NRE                                                                            | m², %                                                                    | same           | same                 | p.186–205 [190–209]       |
| EX_L05/L10_POP, _SHP; EX_LEC_SHP …          | Low Elevation Coastal Zone: < 5 m, 5–10 m, < 10 m. Elevation only, not a flood model                                                                                                             | inhabitants, %                                                           | same           | CIESIN LECZ v3       | p.206–225 [210–229]       |
| EX_L05/L10_P11…P23, _B11…B23                | LECZ × GHS-BUILT-C building type                                                                                                                                                                 | inhabitants, m²                                                          | 2020 only      | same                 | p.226–273 [230–277]       |
| EX_020_S1P, EX_100_S1P, EX_400_S1P          | Tropical-cyclone wind, 20/100/400-yr, Saffir-Simpson categories 1–2                                                                                                                              | inhabitants                                                              | 1975–2030      | STORM v4             | p.274–278 [278–282]       |
| EX_400_S3P                                  | 400-yr, categories 3–5 (the sheet text says "1-2", a copy error). Sheet note: _"There is population exposed only to classes 3-5 for 400 yrp"_                                                    | inhabitants                                                              | same           | same                 | p.280–281 [284–285]       |
| EX_*_S1B/S3B/S1N/S3N                        | same, built-up / non-residential                                                                                                                                                                 | m²                                                                       | same           | same                 | p.282–297 [286–301]       |
| EX_CF2_*, EX_CF1_*                          | Coastal flood, **CF2 = 20-yr, CF1 = 100-yr**. Uncertainty note: LISFLOOD-FP extent from the total water level (mean sea level + tide + surge + waves)                                            | POP inhabitants; BUS/NRE m²; SHP/SHB/SNR %                               | same           | Vousdoukas 2018      | p.298–321 [302–325]       |

### 2.2 Hazard and Risk theme (pp.322–350 [326–354])

| Columns                                                                   | Meaning                                                                                                                                                                                                                                                                                   | Unit         | Epochs           | Upstream                                    |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ---------------- | ------------------------------------------- |
| HZ_CON_* (VAC, BAT, SDV, RIO, PRO, ERV; TOT, SBC, NSC, OSV, FAT)          | Conflict event counts over 3 years (ACLED; UCDP GED). Not a natural hazard                                                                                                                                                                                                               | events       | 1990/2000–2020   | ACLED, UCDP                                 |
| HZ_WLF_NUM, HZ_WLF_BHA                                                    | Accumulated wildfire count and burnt area                                                                                                                                                                                                                                                 | count, ha    | 2015, 2020, 2024 | EFFIS/GWIS, MODIS MCD64                     |
| HZ_CEV_TEV, THZ, MHZ                                                      | MYRIAD-HES multi-hazard events / hazards / maximum hazards per event that overlay the UC. _"The total number corresponds to the previous year, the precedent year and the next year"_ (p.337 [341])                                                                                       | count        | 2005, 2010, 2015 | MYRIAD-HES                                  |
| HZ_CEV_{EAR, EWI, TSU, HEW, DRO, FLO, TCY, VOL, LAN, COW, WLF}            | Count of hazards of type earthquake, extreme wind, tsunami, heatwave, drought, flood, tropical cyclone, volcano, landslide, cold wave, wildfire. Same 3-year windows                                                                                                                      | count        | 2005, 2010, 2015 | same                                        |

There is **no landslide or volcano exposure** layer, only the sparse MYRIAD counts. There is also **no composite
hazard or risk index** in UCDB, so any combination is our own choice (§4).

### 2.3 Documentation errors we found, and how the data resolve them

- **EX_010_SHP / EX_100_SHP.** The PDF names and the xlsx Index both have the two labels swapped. The PDF
  _descriptions_ match the data: EX_010_SHP equals 100·EX_010_POP/GC_POP_TOT within ±0.005 for all 524 reference
  centres, and EX_100_SHP equals 100·EX_100_POP/GC_POP_TOT. So **010 = 10-yr and 100 = 100-yr**.
- **EX_SHA_POP** equals 100·Σ(E06..E10)/GC_POP_TOT within ±0.005 for all 524. The E classes sum to the UC population
  (ratio p1 = 0.9998, median 1.0000).
- **xlsx Index** lists the earthquake classes as `EX_01_POP` … `EX_09_POP`. The gpkg uses `EX_E01_POP` … .
- **"0" vs missing.** The EX flood, earthquake and coastal columns have no nulls in any of the 11,422 centres. A 0
  is therefore a modelled zero exposure, not a gap. The exception is the gap in §2.4. EX_LEC_* is null for 6,259
  centres (non-coastal). HZ_CEV_* columns never contain a 0: the minimum non-null value is 1. A null therefore means
  that the spatial join found no hazard of that type. We read it as 0 only when HZ_CEV_TEV for that epoch is
  non-null, which shows the centre took part in the join.

### 2.4 Defects that decide what we use

- **Cyclone-wind exposure (EX_*_S1P / S3P): rejected.** Only 36 of the 524 reference centres have any exposure.
  Tokyo, Osaka, Hong Kong, Shanghai, Miami and Houston (and every centre in China and the USA) are 0 at every
  return period. Marrakesh, Rabat, Caracas, Lisbon and Porto are exposed. EX_400_S1P exceeds 101 % of the population
  in 474 of the 495 centres that have any value (max 200.0 %; Taipei 152 %). The column is not usable. We could not
  rebuild it from STORM, because data.4tu.nl is not reachable from this environment (§1).
- **River flood, 100-yr layer gap in central/north China.** 27 reference centres have a 10-yr share > 0 but a
  100-yr share = 0, which is impossible for nested return periods. Examples: Kaifeng 64.5 % vs 0, Wuhan 23.8 % vs 0,
  Nanjing 38.5 % vs 0. All 27 lie at lon 110–124°E, lat 30–42°N. Outside China there are 0 such cases out of 441.
  Our rule: when the 10-yr share exceeds the 100-yr share + 0.01, `river_flood_pop_share_100y_pct` is **missing**.
  This affects no target city. Shiyan, Xuzhou, Anshan and Dalian (both shares 0, inside the same box) may be
  affected without being detectable. Beijing (1.8 % / 2.2 %) and Shanghai (58.1 % / 82.3 %) are consistent.
- CF2 ≤ CF1 holds for all 524 centres, and 20-yr ≤ 100-yr cyclone wind holds for all (that column is rejected
  anyway).

## 3. Metrics produced

All values use population epoch 2025 (GHS-POP R2023A E2025, itself a projection) on static hazard maps, so
`year = 2025`. The cyclone metric uses `year = "2004-2016"`. All have `quality = estimated`: the inputs are modelled
hazard maps or modelled event footprints on a modelled population grid.

| Metric key                          | Definition                                                                                                                                                                                                  | Unit            | Notes                                                                                                                                                                                                                                                      |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `quake_pop_share_mmi6plus_pct`      | EX_SHA_POP_2025                                                                                                                                                                                             | % of population | GEM: PGA with _"a 10% probability of being exceeded in 50 years, computed for reference rock conditions"_ (Zenodo description), i.e. a 475-yr return period, expressed as MMI classes by JRC. The PGA→MMI conversion is **not documented** in the fact sheets. Almost binary: 0 or 100 in 119/130 targets (69 at 0, 50 at 100) |
| `quake_mmi_excess_popweighted`      | Σ max(0, MMI_class − 5) · pop_class / Σ pop_class over EX_E01..E10_POP_2025. **Our definition**: the mean number of MMI steps above V. MMI VI is the first class with light damage; classes ≤ V score 0      | MMI steps (0–5) | Separates Tokyo 3.05 / Lima, Santiago, Kathmandu 3.0 / Istanbul 2.46 / Osaka 2.12 / Seoul 1.0 / Kolkata 0.78. The floor at V removes artefacts in the low classes from the regional-model mosaic: Berlin is all MMI 1 while London is all MMI 4. Spearman with the share = 0.97 |
| `river_flood_pop_share_100y_pct`    | EX_100_SHP_2025                                                                                                                                                                                             | %               | Any modelled inundation depth counts. Missing when inconsistent (§2.4)                                                                                                                                                                                     |
| `coastal_flood_pop_share_100y_pct`  | EX_CF1_SHP_2025                                                                                                                                                                                             | %               | 72 % of reference centres are 0. Inland centres are 0 by construction                                                                                                                                                                                      |
| `flood_pop_share_100y_pct`          | max(river, coastal). This is the lower bound of the union of the two extents. UCDB does not publish their overlap, so a sum would double-count; `detail.upper_bound_pct` = min(100, sum)                     | %               | Missing where the river share is missing                                                                                                                                                                                                                   |
| `tropical_cyclone_hazards_per_year` | (HZ_CEV_TCY_2005 + _2010 + _2015) / 9, with null read as 0 per §2.3. Covers the windows 2004–06, 2009–11 and 2014–16                                                                                       | hazards / year  | Historical footprints overlapping the UC. Intensity is not taken into account. 9 sampled years only                                                                                                                                                       |

Rejected or not used: cyclone-wind exposure (defective, §2.4). Built-up shares (they duplicate the population
shares; residents are what the quiz is about). 10-yr and 20-yr variants (kept in `detail`). LECZ (elevation, not
hazard, and it overlaps coastal flood). HZ_CEV_EAR/TSU/VOL/LAN (too sparse: EAR is non-null for only 18–22 of the
524 per epoch). HZ_CEV_EWI (extreme wind includes mid-latitude storms: Madrid 11 vs Tokyo 22, so it barely
discriminates). Wildfire (not in the question). Conflict (not natural).

### Coverage (130 targets)

All metrics are 130/130, except `tropical_cyclone_hazards_per_year`, which is 129/130.

- **nairobi**: HZ_CEV_TEV is null for an epoch, so the centre was not in the MYRIAD join and we cannot tell 0 from
  missing.

Reference set (524): river and combined flood have 27 missing (the China gap, §2.4). The cyclone metric has 3
missing (Nairobi, Malanje, Maceió). All other metrics are 0 missing.

## 4. How the quiz question should map

The question names earthquakes, floods and typhoons. The three hazard families are almost uncorrelated across the
524 reference centres: Spearman quake–flood −0.05, quake–cyclone 0.04, flood–cyclone 0.24. No single column
represents "natural disasters", and UCDB publishes no documented composite. Recommendation:

- Map the question to **three metrics, each lower_better**: `quake_mmi_excess_popweighted`,
  `flood_pop_share_100y_pct` and `tropical_cyclone_hazards_per_year`.
- Combine them in the scoring layer as an **equal-weight mean of reference-set percentiles**. This is a transparent
  choice of ours, to be documented as such; it is not a published index.
- Use `quake_mmi_excess_popweighted` rather than the MMI ≥ 6 share. The share is effectively binary: 119 of the 130
  targets sit at exactly 0 or 100.
- If only one metric can be used, the flood metric has the widest spread, but it misses the earthquake signal
  entirely (Istanbul flood 0.1 %). Do not use one metric alone.

Illustrative composite (printed by `validate()`, complete rows only):

- Lowest hazard: Lusaka 0.23, Doha 0.26, Kampala 0.26, Addis Ababa 0.27, Singapore 0.27, Luanda, Cape Town,
  Salvador, Fortaleza, Stockholm, Minneapolis, Madrid 0.30.
- Highest: Kaohsiung 0.94, Taipei 0.92, Tokyo 0.92, Manila 0.91, Osaka 0.90, Dhaka 0.85, Mexico City 0.83, Cebu 0.82,
  Yangon 0.80, Sapporo 0.78, Fukuoka 0.77, Kolkata 0.77.

## 5. Validation (numbers from `validate()`)

**Distributions over the 130 targets:**

| Metric                     | Min             | Median | Max             | Zeros |
| -------------------------- | --------------- | ------ | --------------- | ----- |
| quake share MMI ≥ 6        | 0               | 0      | 100             | 69    |
| quake MMI excess           | 0               | 0      | 3.05 (Tokyo)    | 69    |
| river flood, 100-yr        | 0               | 1.98   | 82.3 (Shanghai) | 19    |
| coastal flood, 100-yr      | 0               | 0      | 69.6 (Amsterdam)| 66    |
| combined flood             | 0               | 2.5    | 82.3            | 7     |
| cyclone hazards per year   | 0               | 0      | 3.78 (Manila)   | 97    |

Reference p50/p75/p90: river 2.22/13.0/41.6, coastal 0/0.02/1.21, cyclone 0/0.11/0.89, MMI excess 0/1/2.

**Sanity checks against expected hazards:**

- **Earthquake (high, as expected).** MMI excess: Tokyo 3.05, Istanbul 2.46, Los Angeles 2.44, Osaka 2.12, Taipei
  2.10, Manila 2.02. Share MMI ≥ 6 is 100 % in all six.
- **Earthquake (low).** Madrid, Paris, London, Berlin, Riyadh, Denver, Miami, Shanghai and Hong Kong are all 0.
  Hong Kong is 71 % MMI 5 and 29 % MMI 4.
- **Flood.** Dhaka river 56.8 % and Kolkata 28.9 % are high. Shanghai 82.3 %, Bangkok 74.5 % and Phnom Penh 57.5 %
  are the highest. Madrid 0.30 % and Denver 0.98 % are low.
- **Typhoon.** Manila 3.78/yr, Taipei 3.44, Kaohsiung 3.33, Osaka 2.78, Miami 2.67, Fukuoka 2.44, Tokyo 2.33 and
  Havana 1.67 are high. Madrid, Denver and every European centre are 0.
- **Anomalies.**
  - Mexico City gets 1.44/yr from inland remnant footprints. The counts carry no intensity.
  - Hong Kong gets only 0.78/yr against Tokyo's 2.33. This is a footprint artefact we cannot check without MYRIAD
    (6.4 GB).
- **Flood defences are not modelled.** Amsterdam shows 69.6 % of its population in the 100-yr coastal flood extent
  despite the Dutch dyke system. Tokyo shows 19.3 % river and 20.8 % coastal. Neither the fact sheets nor the
  GloFAS README mention protection, and the Amsterdam figure is only possible without it. These metrics measure
  **undefended hazard exposure, not risk**. They penalise low-lying, well-protected cities: Amsterdam, Tokyo, Osaka,
  Shanghai, New York (7.3 % coastal).
- **Cross-check with observations.** Spearman between the modelled river-flood share and the MYRIAD observed
  flood-hazard counts for 2004–16 = 0.27 (524 centres). The agreement is weak but positive, as expected from a
  100-yr extent compared with 9 years of events.

**Regional pattern** (reference means: quake share % / MMI excess / river % / coastal % / combined % / cyclone per
yr):

| Region                           | Quake % | MMI excess | River % | Coastal % | Combined % | Cyclone /yr |
| -------------------------------- | ------- | ---------- | ------- | --------- | ---------- | ----------- |
| Europe                           | 15.4    | 0.22       | 6.1     | 3.1       | 8.1        | 0.00        |
| Sub-Saharan Africa               | 6.7     | 0.08       | 6.6     | 0.04      | 6.6        | 0.03        |
| Eastern & South-Eastern Asia     | 41.6    | 0.70       | 20.8    | 7.1       | 22.6       | 0.74        |
| Central & Southern Asia          | 57.6    | 0.90       | 15.2    | 0.6       | 15.5       | 0.18        |
| Latin America & Caribbean        | 45.2    | 1.00       | 3.8     | 0.1       | 3.8        | 0.31        |
| Northern America                 | 28.8    | 0.46       | 4.4     | 0.5       | 4.5        | 0.29        |
| N. Africa & W. Asia              | 53.4    | 0.77       | 12.8    | 0.5       | 12.9        | 0.00        |
| Australia/NZ (n=5)               | 20.0    | 0.20       | 4.1     | 0.07      | 4.1        | 0.00        |

East/South-East Asia is penalised on all three families. This is physically expected (Pacific Ring of Fire,
monsoon deltas, the typhoon belt), not an artefact. Sub-Saharan Africa and Europe score lowest. By World Bank income
group the means barely move:

| Income group  | Quake share % | Combined flood % | Cyclone /yr |
| ------------- | ------------- | ---------------- | ----------- |
| High          | 36.0          | 7.4              | 0.47        |
| Upper middle  | 36.8          | 14.4             | 0.33        |
| Lower middle  | 45.1          | 15.0             | 0.20        |
| Low           | 25.7          | 7.0              | 0.06        |

The metric is not a proxy for wealth. Because hazard is not vulnerability, a poor and a rich city with the same
exposure score the same. That is intended for "fewer hazards", but the quiz text should not imply "safer".

**Correlation with existing reference metrics.** Spearman over the 524 centres, every pair with |ρ| ≥ 0.25:

| Hazard metric       | Correlates with                                                                                                                                                 |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flood metrics       | elevation (ucdb_elev_m −0.45 river, −0.57 coastal, −0.51 combined); WorldCover water_share (+0.35 / +0.61 / +0.42); dewpoint_warmest (+0.25 / +0.37 / +0.28)    |
| Cyclone             | dewpoint_warmest +0.42, precip_annual +0.35, dewpoint_max_month +0.37, ITDP frequent_transit / sustainable_transport −0.28                                       |
| Earthquake          | nothing above 0.29 (orography +0.28, lapse adjustment +0.26)                                                                                                   |

No hazard metric duplicates an existing metric: the maximum |ρ| is 0.61, for coastal flood vs water share, which is
a physical link. The earthquake metric is essentially independent of everything else.

## 6. Known biases and caveats

1. **Undefended hazard.** Flood maps ignore dykes and levees. The earthquake map is rock-site PGA: no site
   amplification and no building vulnerability.
2. **Modelled, static maps on 2025 population.** Exposure changes over time only through population; the hazard
   footprints do not change.
3. **The earthquake metric's licence is NC-SA** (§1).
4. **The cyclone metric is a 9-year count of historical footprints.**
   - It carries no intensity, so weak remnants count as much as a category-5 landfall.
   - Rare-but-severe locations are undercounted, for example Houston at 0.78/yr.
   - We could not use the STORM 100-yr wind exposure, which would be the better metric (defective in UCDB,
     unreachable upstream).
5. **Earthquake classes.** The MMI classes are JRC's conversion of GEM PGA, and the method is undocumented.
   Mosaic borders between regional models create steps (Berlin MMI 1 vs London MMI 4). Flooring at MMI V removes
   this artefact from the scored metric.
6. **Gap in central/north China** in the 100-yr river layer (§2.4).

## 7. Alternatives considered

- **STORM v4 return-period wind maps × GHS-POP** (our own zonal stats). This is the best typhoon metric, but
  data.4tu.nl is unreachable (connection reset at the proxy). We did not retry, per the access policy.
- **GEM GSHM raster × GHS-POP ourselves** (a 35 MB zip on Zenodo, reachable). It would give continuous PGA
  instead of classes. The licence is the same CC BY-NC-SA, so the licence question stays the same. It could be added
  later if the class granularity matters.
- **INFORM Risk / WorldRiskIndex.** These are national indices, and the comparability rule requires the city
  polygon.
- **EM-DAT disaster counts.** Country-level, and the registration terms are non-commercial.
