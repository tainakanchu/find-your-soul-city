# GHS-UCDB R2024A (`ghsl-ucdb`) + GHS-POP R2023A (`ghsl-pop`)

Module: `etl/soulcity_etl/ghsl.py` (`cd etl && UV_SYSTEM_CERTS=1 uv run python -m soulcity_etl.ghsl`; runtime ~35 s
once inputs are cached). The run writes the files below and then prints the validation numbers quoted in §5.

| Output                                                        | Content                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data/interim/ghsl-ucdb.json`                                 | 9 metrics for the 86 target cities, read from UCDB theme layers (or simple arithmetic on them)                                                                                                                                                                                                              |
| `data/interim/ghsl-pop.json`                                  | `density_weighted`, which we compute from the GHS-POP E2025 1 km raster                                                                                                                                                                                                                                     |
| `data/interim/city-attributes.json`                           | non-numeric attributes: `iso2`, `country_name` (UN/WPP), `country_name_gadm`, `region` (UN SDG region), `income` (World Bank group), `ucdb_id`, `name_en`, `lat`/`lon` (point on surface), `area_km2`, `capital`, `plausibility`, `koppen_code`/`koppen_class`, `ucdb_names` (GC_UCN_LIS_2025 split on `;`) |
| `data/reference/ghsl-ucdb.csv`, `data/reference/ghsl-pop.csv` | the same metrics for all 524 centres with pop ≥ 1M (`reference_centres()`)                                                                                                                                                                                                                                  |

Missing rate: **0 / 86** for every metric, and 0 / 524 for the reference set (no blank cells in either CSV). ISO2 was resolved for 86/86 targets
and 524/524 reference centres.

## 1. Inputs, versions, licenses

| Input                                                                                   | URL                                                                                                                                                                                                                                  | Version / DOI                                                                       |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| GHS-UCDB R2024A gpkg                                                                    | `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_UCDB_GLOBE_R2024A/GHS_UCDB_GLOBE_R2024A/V1-2/GHS_UCDB_GLOBE_R2024A_V1_2.zip`                                                                                              | V1.2, data last update 15/05/2026, doi:10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd |
| UCDB documentation                                                                      | `GHSL_UCDB_R2024_V1_2.pdf` (in the zip; "Stats in the City – the GHSL Urban Centre Database 2025")                                                                                                                                   | doi:10.2760/3046391, JRC139768                                                      |
| GHS-POP R2023A, epoch 2025, 1 km, Mollweide                                             | `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2025_GLOBE_R2023A_54009_1000/V1-0/GHS_POP_E2025_GLOBE_R2023A_54009_1000_V1_0.zip` (308 MB global file; tif extracted to `.cache/raw/ghsl-pop/`) | V1-0, doi:10.2905/2FF68A52-5B5B-4A22-8F40-C41DA8332CFE                              |
| GHSL Data Package 2023 report                                                           | `GHSL_Data_Package_2023.pdf`, shipped inside the GHS-POP zip                                                                                                                                                                         | doi:10.2760/098587, JRC133256                                                       |
| Beck et al. 2018 Köppen-Geiger V1 (used only for `legend.txt`, the code-to-class table) | `https://ndownloader.figshare.com/files/12407516` (figshare article 6396959)                                                                                                                                                         | doi:10.1038/sdata.2018.214                                                          |
| GHSL copyright notice                                                                   | `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/copyright.txt`                                                                                                                                                                | —                                                                                   |

All of these are recorded in `data/provenance/downloads.json` through `common.fetch()`.

**GHSL license.** `copyright.txt` on the FTP (also in each product folder) says: _"Any copyright and/or sui generis
right on the dataset is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence [2].
Reuse is allowed provided appropriate credit is given and any changes are indicated."_
(https://creativecommons.org/licenses/by/4.0). The UCDB `readme_V1_2.txt` cites the EC reuse notice: "Reuse is
authorised, provided the source is acknowledged" (Decision 2011/833/EU).

**Required citations.**

- Dataset (from the readme): Mari Rivero, I.; Melchiorri, M.; Florio, P.; Schiavina, M.; Goch, K.; Politis, P.; Uhl,
  J. H.; Pesaresi, M.; Maffenini, L.; Sulis, P.; Crippa, M.; Guizzardi, D.; Pisoni, E.; Belis, C.; Jacome Felix Oom, D.;
  Branco, A.; Mwaniki, D.; Kochulem, E.; Githira, D.; Carioli, A.; Ehrlich, D.; Tommasi, P.; Kemper, T.; Dijkstra, L.
  (2024): GHS-UCDB R2024A - GHS Urban Centre Database 2025. European Commission, Joint Research Centre (JRC)
  [Dataset] doi:10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd.
- Report: Melchiorri, M. et al., _Stats in the City – the GHSL Urban Centre Database 2025_, Publications Office of the
  EU, 2024, doi:10.2760/3046391, JRC139768.
- GHS-POP: Schiavina, M.; Freire, S.; Carioli, A.; MacManus, K. (2023): GHS-POP R2023A - GHS population grid
  multitemporal (1975-2030). European Commission, JRC. doi:10.2905/2FF68A52-5B5B-4A22-8F40-C41DA8332CFE.
- "Changes made": we derive population/area ratios, population-weighted density, land-cover shares and an ISO2 code.

**Upstream third-party data inside the UCDB columns we use.**

| Column(s)  | Upstream                                                                                         | License as read                                                                                                                                                                                                                                                                                                                               |
| ---------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EM_PM2_CON | WUSTL ACAG SatPM2.5 V6.GL.02.02 (Shen et al. 2024, doi:10.1021/acsestair.3c00054)                | https://sites.wustl.edu/acag/datasets/surface-pm2-5/ says "SatPM 2.5 data V6.GL.02.04 are licensed under CC BY 4.0" (same for V5.GL.05.02). The page no longer lists V6.GL.02.02, the exact version UCDB used, so its license is assumed to be the same but was **not** verified.                                                             |
| LU_HEC     | Copernicus Global Land Service LC100 Collection 3 (Buchhorn et al. 2020, doi:10.3390/rs12061044) | https://land.copernicus.eu/en/data-policy: "made available on a principle of full, open and free access … users shall inform the public of the source … Where the … products … have been adapted or modified by the user, the user shall clearly state this." Attribution: "European Union's Copernicus Land Monitoring Service information". |
| GE_ELV     | Copernicus DEM GLO-90 (doi:10.5270/ESA-c5d3d65)                                                  | registry.opendata.aws/copernicus-dem: "GLO-30 Public and GLO-90 are available on a free basis for the general public under the terms and conditions of the Licence".                                                                                                                                                                          |
| GR_AVG_GRN | Landsat 8 Collection 2 NDVI (USGS EROS) + GHS-BUILT-S                                            | USGS Landsat data are US-Government public domain. The usgs.gov copyright page returned 403 to our fetch, so this was not re-read.                                                                                                                                                                                                            |
| GH_BUH     | GHS-BUILT-H R2023A (JRC)                                                                         | CC BY 4.0 (GHSL copyright.txt)                                                                                                                                                                                                                                                                                                                |
| CL_KOP_CUR | Beck et al. 2018                                                                                 | figshare record license: CC BY 4.0 (figshare API `license.name`)                                                                                                                                                                                                                                                                              |

## 2. Column dictionary (from the UCDB fact sheets)

Page numbers are the printed numbers in `GHSL_UCDB_R2024_V1_2.pdf`, with the PDF page index in brackets. Every
meaning below is taken from the fact sheet, not from the column name. Where a column has no fact sheet, the
`Index` sheet of `GHS_UCDB_GLOBE_R2024A.xlsx` is cited instead.

| Column                                 | Meaning (fact sheet)                                                                                                                                                                                                                                                                                                 | Unit                      | Epoch                             | Upstream                                                                           | Method                                                                                              | Doc                  |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | --------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | -------------------- |
| GC_UCN_MAI_2025                        | Name of the main city inside the UC                                                                                                                                                                                                                                                                                  | –                         | 2025                              | OSM, GISCO, WUP2018                                                                | geocoding                                                                                           | p.23 [27]            |
| GC_UCN_LIS_2025                        | "List of names of the all cities inside the urban center"                                                                                                                                                                                                                                                            | –                         | 2025                              | same                                                                               | geocoding                                                                                           | p.23 [27]            |
| GC_CNT_GAD_2025                        | Country name from GADM 4.1 (mojibake in file, re-decoded latin-1→utf-8)                                                                                                                                                                                                                                              | –                         | 2025                              | GADM 4.1                                                                           | spatial join                                                                                        | p.24 [28]            |
| GC_CNT_UNN_2025                        | Country **name** based on WPP2022 (GADM countries merged per WPP notes). It is a name, not an M49 code.                                                                                                                                                                                                              | –                         | 2025                              | UN WPP2022                                                                         | spatial join                                                                                        | p.25 [29]            |
| GC_UCA_KM2_2025                        | Urban Centre area                                                                                                                                                                                                                                                                                                    | km²                       | 2025                              | GHS-SMOD R2023A                                                                    | geometry area                                                                                       | p.26 [30]            |
| GC_POP_TOT_2025                        | "Total population allocated inside of the UC"; "Zonal sum of the GHS-POP R2023A layer pixel values inside the urban centre"                                                                                                                                                                                          | inhabitants               | 2025                              | GHS-POP R2023A                                                                     | zonal sum                                                                                           | p.27 [31]            |
| GC_DEV_WIG_2025                        | World Bank income group (classification updated to 2022)                                                                                                                                                                                                                                                             | cat.                      | 2025                              | World Bank                                                                         | join by country                                                                                     | p.28 [32]            |
| GC_DEV_USR_2025                        | UN SDG region                                                                                                                                                                                                                                                                                                        | cat.                      | 2025                              | UNSD                                                                               | join by country                                                                                     | p.29 [33]            |
| GC_PLS_SCR_2025                        | Plausibility score of the modelled UC                                                                                                                                                                                                                                                                                | cat.                      | 2025                              | JRC                                                                                | ensemble model                                                                                      | p.30 [34]            |
| GC_UCM_CAP                             | Capital city flag (0/1)                                                                                                                                                                                                                                                                                              | bool                      | 2025                              | Wikipedia, Google Maps                                                             | geocoding                                                                                           | p.35 [39]            |
| GH_POP_TOT_XXXX                        | Same as GC_POP_TOT for 1975–2030                                                                                                                                                                                                                                                                                     | inhabitants               | 5-yearly                          | GHS-POP                                                                            | zonal sum                                                                                           | p.36 [40]            |
| GH_BUH_AVG_2020                        | "Average of the values inside the urban centre of the average height of the built surfaces in a 100 m pixel"                                                                                                                                                                                                         | m                         | 2020 (label)                      | GHS-BUILT-H R2023A ("derived from AW3D30, SRTM30, and Sentinel2 composite (2018)") | zonal mean                                                                                          | p.48 [52]            |
| GR_AVG_GRN_2020                        | "Mean greenness (NDVI) in the built-up area (within a 300 m buffer of the built-up cells)"                                                                                                                                                                                                                           | NDVI                      | 1985–2025                         | Landsat 8 C2 NDVI, GHS-BUILT-S, UN-Habitat thresholds                              | mask + zonal mean                                                                                   | p.581 [585]          |
| GR_SQM_{HGR,LGR,GRN}, GR_SHB_{HGR,GRN} | built-up m² in high/low/any greenness; share of built-up in high/any greenness                                                                                                                                                                                                                                       | m², %                     | 1985–2025                         | same                                                                               | mask/ratio                                                                                          | pp.583–589 [587–593] |
| GR_CTH_AVG_2020                        | Mean canopy top height in a 300 m buffer of built-up                                                                                                                                                                                                                                                                 | m                         | 2020                              | Lang et al. 2023                                                                   | zonal mean                                                                                          | p.579 [583]          |
| SD_POP_HGR_XXXX                        | "Share of the Urban Centre population living in area of high greenness" (SDG 11.7.1 proxy)                                                                                                                                                                                                                           | %                         | 1985–2025                         | Landsat NDVI, UN-Habitat, GHS-POP                                                  | mask + ratio                                                                                        | p.354 [358]          |
| LU_HEC_{020…126}_2019                  | Area of each Copernicus Global Land Cover class inside the UC: 20 shrubs, 30 herbaceous, 40 cropland, 50 built-up, 60 bare/sparse, 70 snow/ice, 80 permanent water, 90 herbaceous wetland, 100 moss/lichen, 111–116 closed forest (evergreen/deciduous needle/broad, mixed, other), 121–126 open forest (same split) | ha                        | 2015, 2019                        | CGLS-LC100 Collection 2/3 (Buchhorn et al. 2020)                                   | pixel-area sum per class                                                                            | pp.143–163 [147–167] |
| CL_KOP_CUR_2025                        | "Köppen-Geiger classification of the majority of UC surface - current conditions"; integer code of the Beck map                                                                                                                                                                                                      | cat. (1–30)               | label 2025; Beck V1 "present" map | Beck et al. 2018                                                                   | majority by area                                                                                    | p.368 [372]          |
| CL_UTC_T32_XXXX                        | "Annual mean number of days in the decade that UTCI has exceeded 32 degrees based on daily maxima"                                                                                                                                                                                                                   | days                      | decades 1970…2020                 | ERA5-HEAT (C3S)                                                                    | "Zonal average (count) of the number of pixels exceeding the threshold … touching the urban center" | p.404 [408]          |
| EM_PM2_CON_XXXX                        | "PM2.5 population weighted average concentrations": ACAG V6.GL.02.02 1 km annual PM2.5 overlaid with GHS-POP 1 km, population-weighted within the UC                                                                                                                                                                 | µg/m³ (stored as integer) | 2000, 2005, 2010, 2015, 2020      | ACAG SatPM2.5 + GHS-POP                                                            | modelled                                                                                            | pp.490–491 [494–495] |
| EM_PM2_MOR_XXXX                        | Premature deaths due to PM2.5 (GBD IER curves, JRC FASST)                                                                                                                                                                                                                                                            | deaths                    | 2000–2020                         | WHO, GBD 2019                                                                      | modelled                                                                                            | p.492 [496]          |
| NS_ESB_P25_2025                        | Count of PM2.5 Earth-system-boundary transgressions                                                                                                                                                                                                                                                                  | count                     | 2025                              | Rockström et al. 2023                                                              | zonal sum                                                                                           | p.504 [508]          |
| GE_ELV_AVG_2025                        | Average elevation in the UC                                                                                                                                                                                                                                                                                          | m                         | label 2025                        | Copernicus GLO-90                                                                  | zonal mean                                                                                          | p.576 [580]          |
| GE_ECO_CLA_2025, GE_MRB_*, GE_BIO_*    | ecoregion, major river basin, biome shares                                                                                                                                                                                                                                                                           | cat./%                    | 2025                              | Olson 2001, WB, Higgins 2016                                                       | overlap                                                                                             | pp.549–574           |
| GE_SCL_MPC_2023, GE_SCL_LST_2023       | **No fact sheet in the PDF.** The xlsx Index sheet lists them as "Most probable soil group" / "List of soil groups" from SoilGrids250m 2.0, and also reuses the same IDs for the river-basin rows (a documentation error)                                                                                            | cat.                      | 2023                              | SoilGrids                                                                          | –                                                                                                   | xlsx Index           |
| GH_L30_2025, GH_W30_2025               | **Not documented** in the PDF or the xlsx Index                                                                                                                                                                                                                                                                      | –                         | –                                 | –                                                                                  | –                                                                                                   | –                    |
| WA_MAR_SST_XXXX                        | Sea surface temperature, zonal mean "using a 10 km buffer around the coastal urban centers"                                                                                                                                                                                                                          | °C                        | 2021–2024                         | CMEMS Global Ocean Physics Reanalysis                                              | zonal mean                                                                                          | p.526 [530]          |
| WA_MAR_SHT / STT / W01–W12             | sea-level trend, SST trend, monthly wave height (coastal UCs only)                                                                                                                                                                                                                                                   | mm/yr, °C/yr, m           | 2018–2023                         | CMEMS                                                                              | zonal mean (10 km buffer)                                                                           | pp.524–527           |
| IN_ROA_LEN_2024 / IN_ROA_DEN_2024      | road length; road length / UC area                                                                                                                                                                                                                                                                                   | m; m/m²                   | 2024                              | Overture Maps (accessed 24/07/2024)                                                | length sum / division                                                                               | pp.539–540 [543–544] |
| HL_{FCL,FDE,FPC,POP,SHP}_{HOS,PHA}     | hospitals/pharmacies: count, per km², per 10⁶ inhabitants, population and share within 1 km                                                                                                                                                                                                                          | various                   | 2024/2025                         | healthsites.io (OSM), GHS-POP                                                      | ratio / zonal sum                                                                                   | pp.512–518 [516–522] |
| SC_CON_*                               | Ookla fixed/mobile speed, latency                                                                                                                                                                                                                                                                                    | Mbps, ms                  | –                                 | Speedtest by Ookla                                                                 | weighted mean                                                                                       | xlsx Index           |

**Coast / sea proximity.** The UCDB has **no** coastline length, distance-to-sea or coastal flag. The only coastal
signal is the set of WA_MAR_* columns, which are non-null for "coastal urban centers". The PDF never defines
"coastal" (p.524–527 only say "a 10 km buffer around the coastal urban centers"). Among the targets, 47 have a
non-null WA_MAR_SST_2024 and 39 do not. A coast metric should come from a coastline dataset, not from this null
pattern.

## 3. Metrics produced

| Key                      | File      | Definition                                                                                         | Unit                     | Year                                                                          | Quality   |
| ------------------------ | --------- | -------------------------------------------------------------------------------------------------- | ------------------------ | ----------------------------------------------------------------------------- | --------- |
| `urban_pop`              | ghsl-ucdb | GC_POP_TOT_2025                                                                                    | persons (not millions)   | 2025                                                                          | estimated |
| `urban_area_km2`         | ghsl-ucdb | GC_UCA_KM2_2025                                                                                    | km²                      | 2025                                                                          | estimated |
| `density_mean`           | ghsl-ucdb | GC_POP_TOT_2025 / GC_UCA_KM2_2025                                                                  | persons/km²              | 2025                                                                          | estimated |
| `density_weighted`       | ghsl-pop  | Σ p_i·d_i / Σ p_i, d_i = p_i / cell_area (1 km²), over GHS-POP E2025 1 km cells inside the polygon | persons/km²              | 2025                                                                          | estimated |
| `building_height_mean_m` | ghsl-ucdb | GH_BUH_AVG_2020                                                                                    | m                        | 2018 (UCDB labels it 2020; GHS-BUILT-H is derived from the 2018 S2 composite) | estimated |
| `pm25_popweighted_ugm3`  | ghsl-ucdb | EM_PM2_CON_2020                                                                                    | µg/m³ (integer upstream) | 2020                                                                          | estimated |
| `ndvi_builtup_mean`      | ghsl-ucdb | GR_AVG_GRN_2020                                                                                    | NDVI (−1…1)              | 2020                                                                          | observed  |
| `tree_cover_share_pct`   | ghsl-ucdb | 100 · Σ LU_HEC_{111…126}_2019 / Σ LU_HEC_{all 21 classes}_2019                                     | %                        | 2019                                                                          | observed  |
| `elevation_mean_m`       | ghsl-ucdb | GE_ELV_AVG_2025                                                                                    | m a.s.l. (DSM)           | 2025 (UCDB label)                                                             | observed  |

Quality rationale:

- **Population is model output.** GHS-POP E2025 starts from GPWv4.11 census units, applies growth rates that
  converge to WPP2022 national trends, rescales to the UN WUP2018 city time series (both projections for 2025), and
  allocates population to 100 m cells by residential built-up volume. The 2025 built-up itself is "solved by
  spatial-temporal interpolation or extrapolation" for "the future epochs 2025 and 2030" (Data Package 2023
  pp.46–47 [51–52]; p.6 [11]). E2025 is therefore a projection/nowcast, not an observation, so it is labelled
  `estimated`. Inside the targets, GH_POP_TOT 2025/2020 has median 1.036 (min 0.951 Osaka, max 1.251 Addis Ababa).
- PM2.5 (satellite AOD + chemical transport model + CNN calibration) and BUILT-H (DEM/S2 regression) are modelled
  surfaces, so they are `estimated`.
- NDVI, land-cover classification and the DEM are direct remote-sensing measurements aggregated by JRC, so they
  are `observed`. They are still classifier or sensor products with their own error.

**density_weighted method.** UCDB geometries are read in their native ESRI:54009 Mollweide (no reprojection). The
GHS-POP 1 km tif is also ESRI:54009, with origin (−18 041 000, 9 000 000) and 1000 m cells, and every polygon vertex
lies on that grid, so the polygon is an exact union of raster cells. Cells are selected by centre-in-polygon
(`rasterio.features.geometry_mask`, `all_touched=False`), and the cell area is 1.000 km² because Mollweide is equal
area. **Check:** Σp_i inside the polygon / GC_POP_TOT_2025 = **1.000000 for all 86 targets and all 524 reference
centres** (rounded to 6 d.p.). The cell selection therefore reproduces JRC's own zonal sum, and the epochs match.
`detail` holds n_cells, grid_pop_sum, the ratio, and the p90 and maximum cell density.

**tree_cover_share_pct denominator.** The 21 LU_HEC classes do not include CGLS class 200 (open sea). Σ classes /
UC area is 0.9985–1.000 for the 39 targets without WA_MAR data (median 1.000), but as low as 0.470 (Hong Kong) for
coastal ones (median 0.891 over 47). We conclude that the missing area is sea inside the 1 km cells. This is our
inference; the docs do not say it. The share is therefore relative to classified land + inland water, and
`detail.lc_total_over_uc_area` records the ratio.

**Attributes.** ISO2 comes from `pycountry` on the UN name (GC_CNT_UNN_2025), with the GADM name (mojibake-fixed) as
fallback. A small name→name alias table covers WPP spellings ("Republic of Korea", "China, Taiwan Province of
China", "Turkey", "Democratic Republic of the Congo"…). All 127 country names among the 524 reference centres were
listed and checked against the pycountry name; 12 differed only in spelling ("Bolivia (Plurinational State of)" →
BO, "Iran (Islamic Republic of)" → IR, …), and none was wrong. Köppen letters come from Beck V1 `legend.txt` (30
classes). Target distribution: Cfb 15, Cfa 11, Aw 9, Csa 8, Dfb 8, BSk 7, Csb 5, others ≤ 3. Regions among the
targets: Europe 23, E/SE Asia 17, N America 11, LatAm 10, C/S Asia 7, N Africa/W Asia 7, SSA 7, Aus/NZ 4. Income:
High 49, Upper-middle 19, Lower-middle 17, Low 1. Use these for fairness checks: the set is skewed to high income.

## 4. Rejected candidates

| Candidate                                  | Reason                                                                                                                                                                                                                                                          |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SD_POP_HGR_* (pop share in high greenness) | Implausible values: Ulaanbaatar 99.98 % (2020) while its NDVI is 0.17; Tokyo 0.67 %→1.46 % and Munich 3.8 %→7.8 % between 2020 and 2025. The UN-Habitat thresholds per agro-ecological zone are not published in the doc.                                       |
| GR_SHB_HGR / GR_SHB_GRN                    | Unit says %, but values are ~0.001–0.04 (e.g. Tokyo 0.0026), so they are neither % nor a plausible fraction. Not usable without clarification.                                                                                                                  |
| GR_AVG_GRN_2025                            | 2025 needs a 3-year Landsat average that includes the future relative to the 2024 build. The 2020 epoch is used instead.                                                                                                                                        |
| CL_UTC_T32 (heat-stress days)              | The "decade" for the 2020 epoch is undefined (ERA5-HEAT was accessed Jan 2025, so at most 2020–2024), and the method text ("zonal average (count) of the number of pixels … touching") is ambiguous. Heat is computed directly from ERA5 by the climate module. |
| WA_MAR_SST / coastal flag                  | "Coastal urban centre" is undefined, and values are doubtful (Osaka 12.9 °C vs Tokyo 15.4 °C annual SST in 2024).                                                                                                                                               |
| GE_SCL_*, GH_L30/W30                       | No fact sheet (soil classes are not lifestyle-relevant anyway).                                                                                                                                                                                                 |
| LU_HEC water (class 80)                    | Median 0 % across targets (rivers < 100 m vanish at 100 m resolution, and sea is excluded), so it does not discriminate.                                                                                                                                        |
| IN_ROA_DEN (road density)                  | Weak construct for walkability (it counts motorways too), and the upstream Overture transportation data derive from OSM under ODbL (share-alike).                                                                                                               |
| HL_SHP_HOS / HL_FPC_* (hospital access)    | The doc warns "OSM limitations, completeness and accuracy are inherited". Completeness differs strongly by country, which would bias cross-country comparison.                                                                                                  |
| SC_CON_* (internet speed)                  | Upstream Ookla Open Data is CC BY-NC-SA 4.0 (teamookla/ookla-open-data README), which is non-commercial and share-alike.                                                                                                                                        |
| EM_PM2_MOR, NS_ESB_P25                     | Counts that scale with population or are boundary-transgression counts. The concentration (EM_PM2_CON) is the right user-facing quantity.                                                                                                                       |
| GH_BPC_* (built-up per capita)             | Duplicates density information; values outside 1–600 m²/person are excluded upstream.                                                                                                                                                                           |
| CL_LCZ_*, SC_SEC_* (HDI etc.), hazards     | Out of scope for this pass. HDI is a subnational GDL estimate (Smits 2019), not a city measurement. Could be revisited.                                                                                                                                         |
| GHS-POP 100 m for density_weighted         | Not used. The 1 km grid exactly matches the UCDB polygons and GC_POP_TOT, and it is the standard unit for the Degree of Urbanisation. 100 m cells would raise all values (finer cells show more concentration).                                                 |

## 5. Validation (numbers printed by `validate()`)

Distributions over the 86 targets (min / median / max):

| Metric                 | Min                 | Median | Max               |
| ---------------------- | ------------------- | ------ | ----------------- |
| urban_pop              | 206 900 (Reykjavik) | 4.57 M | 40.55 M (Jakarta) |
| urban_area_km2         | 97 (Reykjavik)      | 761    | 6 611 (Dhaka)     |
| density_mean           | 1 731 (Perth)       | 6 260  | 27 714 (Mumbai)   |
| density_weighted       | 2 534 (Perth)       | 10 900 | 58 855 (Mumbai)   |
| building_height_mean_m | 3.39 (Dhaka)        | 8.76   | 18.54 (Hong Kong) |
| pm25_popweighted_ugm3  | 3 (Honolulu)        | 15     | 94 (New Delhi)    |
| ndvi_builtup_mean      | 0.102 (Dubai)       | 0.372  | 0.575 (Dhaka)     |
| tree_cover_share_pct   | 0 (Accra)           | 5.7    | 35.9 (Vancouver)  |
| elevation_mean_m       | 0.6 (Amsterdam)     | 57     | 2 801 (Quito)     |

**Known-city sanity.** By weighted density, the five densest are Mumbai 58 855, Hong Kong 56 895, Cairo 49 637,
Dhaka 46 752 and Bengaluru 46 588. The least dense are Perth 2 534, Denver 2 822, Seattle 3 015, Miami 3 306 and
Reykjavik 3 355. PM2.5 is highest in New Delhi 94, Dhaka 84 and Cairo 74, and lowest in Honolulu 3, Reykjavik 4, and
Vancouver/Toronto/Stockholm/Seattle 6. Hong Kong has the tallest mean building height (18.5 m). NDVI is lowest in the desert/arid cities: Dubai 0.10, Lima 0.12, Dakar 0.15, Tehran 0.17. Köppen classes match the expected climates
(Tokyo Cfa, Cape Town Csb, Lima BWh, Addis Ababa Cwb). One exception: Barcelona is BSk because UCDB takes the
majority class over the polygon at the Beck 1 km border.

**Mean vs weighted density.** Spearman ρ = 0.934 over the 86 targets and 0.871 over the 524 reference centres.
Weighted/mean ratio: min 1.36, median 1.78, max 8.28 (Dhaka). Largest rank moves (0 = densest, mean→weighted):
Dhaka 45→3, New York 59→31, Hanoi 47→26, Johannesburg 56→36, Marrakesh 21→6, Havana 54→40; Sapporo 46→61, Tehran
9→23, Quito 35→47, Almaty 33→44.

**Why weighted is preferred for "how crowded does it feel".** The mean divides by the whole polygon, including
sparsely populated 1 km cells at the edge and large voids such as airports, parks and water. Its value therefore
depends on how far the delineation reaches. Population weighting gives the density around the average resident.
Dhaka shows the problem: the polygon is 6 611 km² and swallows towns up to ~100 km away (Cumilla, Noakhali,
Lakshmipur), so the mean is only 5 643/km², while residents of the core live at ~47 000/km². New York (Manhattan
within a large suburban polygon) moves the same way. Weighted density is much less sensitive to polygon merging,
which matters given the merges listed below. Reference p10/p50/p90 of density_weighted over the 524 centres:
5 630 / 13 788 / 31 556.

**Epoch alignment.** Population, area, density_mean and density_weighted are all 2025 (grid sum = UCDB sum exactly).
The other metrics come from other years: PM2.5 2020, NDVI 2020, land cover 2019, building height 2018 (labelled
2020), Köppen present-day V1 map, and DEM (static, labelled 2025). The orchestrator should treat them as
"circa 2018–2020 environment" combined with "2025 population".

**Polygons that merge distinct cities** (GC_UCN_LIS_2025, first names; count = number of listed places):

- **tokyo** 119 names, 33.16 M, 5 165 km²: Tokyo, Yokohama, Kawasaki, Saitama, Chiba, Funabashi, Kawaguchi… (the whole Kantō plain core)
- **osaka** 44 names, 12.65 M, 2 212 km²: Osaka, **Kobe, Kyoto**, Sakai, Higashiosaka, Nishinomiya, Amagasaki… (this is why Kyoto is not a target)
- **seoul** 18 names, 22.26 M, 2 282 km²: Seoul, **Incheon**, Suwon, Goyang, Seongnam, Bucheon, Anyang…
- **san-francisco** 18 names, 4.72 M, 1 614 km²: the list starts with **San Jose**, then San Francisco, Oakland, Fremont, Berkeley… (the whole Bay Area)
- **los-angeles** 27 names, 13.47 M, 4 498 km²: LA, Long Beach, Anaheim, Santa Ana, Irvine, San Bernardino…
- **new-york** 12 names, 14.20 M, 3 031 km²: New York, **Newark, Jersey City**, Yonkers, Paterson, New Brunswick…
- **miami** 16 names, 5.73 M, 2 784 km²: Miami, Fort Lauderdale, **West Palm Beach**…
- **new-delhi** 7 names, 31.42 M, 2 139 km²: Ghaziabad, Gurugram, Noida, New Delhi, Faridabad…
- **dhaka** 8 names, 37.31 M, 6 611 km²: Dhaka, Narayanganj, Gazipur, plus **Cumilla, Noakhali, Lakshmipur** (separate cities ~100 km away)
- **jakarta** 9 names, 40.55 M, 4 614 km²: Jakarta, Bekasi, Tangerang, Depok, **Bogor, Serang, Sukabumi, Cianjur**
- **manila** 33 names, 25.92 M; **buenos-aires** 35, 14.18 M; **sao-paulo** 22, 19.49 M; **mexico-city** 19, 17.64 M; **shanghai** 16 (mostly districts), 30.68 M; **beijing** 10 (districts); **fukuoka** 10; **vancouver** 10 (Surrey, Burnaby…); **tel-aviv** 7; **toronto** 7 (Mississauga, Brampton…); **ho-chi-minh** 6 (Biên Hòa, Thủ Dầu Một); **bangkok** 7; **cairo** 7 (Giza…); **kuala-lumpur** 8; **lisbon** 9; **madrid** 8; **paris** 5; **barcelona** 5.
- In the reference set (not a target), **Guangzhou** is a single 42.99 M centre. Hong Kong is a separate 4.81 M centre (names: Hong Kong, Kowloon).

Place counts depend on how finely OSM/GISCO names places (districts vs municipalities), so they are not
comparable across countries. Area and population are the meaningful size indicators.

## 6. Caveats and known biases

- **Hong Kong iso2 = CN.** Both GC_CNT_UNN_2025 and GC_CNT_GAD_2025 say "China" for the Hong Kong centre. We keep
  the UCDB assignment (no manual override). Any join of country-level data on iso2 will give Hong Kong China's
  national values. Override deliberately in the consumer if HK-specific statistics are wanted.
- GHS-POP allocates census population by residential built-up _volume_, so tall residential districts get
  concentrated population. The weighted density inherits this modelling assumption, and E2025 is an
  extrapolation.
- `urban_pop` is in persons; the knowledge metric card says 百万人 (millions), so the consumer must scale.
- PM2.5 is stored as an integer by UCDB, which limits resolution for clean-air cities (3–9 µg/m³).
- `ndvi_builtup_mean`: the fact sheet's methodology text mentions masking at "greater or equal than threshold",
  while the description says mean NDVI in the 300 m built-up buffer. Values (desert cities 0.10–0.15, Munich 0.49)
  fit an unmasked mean, but this is not certain. Use as a relative greenness indicator. The WorldCover module's
  `green_share` is the primary green metric; `tree_cover_share_pct` (CGLS 2019) is a cross-check.
- `building_height_mean_m` likely averages over all 100 m pixels of the UC, including empty ones. Dhaka's 3.4 m
  minimum fits this, since its polygon includes rural cells. It mixes "how tall" with "how built-up".
- `elevation_mean_m`: Copernicus GLO-90 is a surface model (includes buildings and trees), and the mean over large
  polygons hides relief (e.g. Quito's valley).
- UCDB region labels follow the UN SDG grouping (e.g. Turkey/Israel/Egypt/Morocco all "Northern Africa and Western
  Asia"); income labels use mixed spellings ("High income", "Upper Middle").

## 7. Alternatives considered

- WorldPop or LandScan for population-weighted density: rejected because they use different grids and
  population-model assumptions. Only GHS-POP gives Σp exactly equal to the UCDB population (ratio 1.000000), which
  keeps `urban_pop`, `density_mean` and `density_weighted` mutually consistent.
- GHS-POP E2020 instead of E2025: the population is less extrapolated, but the UC polygons are the 2025
  delineation. Changing epoch would break the exact match. The 2020→2025 change inside the targets is small
  (median +3.6 %).
- Recomputing NDVI/PM2.5 ourselves from Landsat/ACAG rasters: possible later. UCDB values are used now because
  they are already computed on the exact polygon (PM2.5 already population-weighted with the same GHS-POP grid).
