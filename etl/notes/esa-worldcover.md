# ESA WorldCover 10 m 2021 v200 (`esa-worldcover`)

Module: `etl/soulcity_etl/worldcover.py` (`cd etl && uv run python -m soulcity_etl.worldcover`).
Output: `data/interim/esa-worldcover.json`. Validation dump (all 86 rows): `.cache/raw/esa-worldcover/validation.json`.

## Source
- ESA WorldCover 10 m 2021 v200 (algorithm V2.0.0), Zanaga et al. 2022, DOI 10.5281/zenodo.7254221. Sentinel-1/2, observation period 2021-01-01 to 2021-12-31 (tile metadata `time_start/time_end`).
- Cloud-optimised GeoTIFF tiles, 3 deg x 3 deg, EPSG:4326, 36000 x 36000 px (pixel = 1/12000 deg), uint8, nodata 0.
  URL: `https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_<TILE>_Map.tif`.
  `<TILE>` = lower-left corner, `N|S` + 2-digit lat + `E|W` + 3-digit lon (e.g. N33E138 covers 33-36N, 138-141E). Tile list: `.../v200/2021/esa_worldcover_grid.geojson` (property `ll_tile`). Tiles with no land are absent from the product.
- Tiles are read windowed over HTTPS (`/vsicurl`), nothing is downloaded whole. Every tile used (and the grid, PVR, PUM) is in `data/provenance/downloads.json`. 104 distinct tiles used (max 2 per city).
- Docs (cached under `.cache/raw/esa-worldcover/docs/`): Product User Manual V2.0, Product Validation Report V2.0.

## License and attribution
- ESA page https://esa-worldcover.org/en/data-access: "The ESA WorldCover product is provided free of charge, without restriction of use. For the full license information see the Creative Commons Attribution 4.0 International License." Tile metadata also says `license: CC-BY 4.0`.
- Required attribution (verbatim from the same page, year 2021): **"© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium"**. Citation: Zanaga, D. et al., 2022. ESA WorldCover 10 m 2021 v200. https://doi.org/10.5281/zenodo.7254221. Our values are modified (aggregated) derivatives: state that in the app credits.

## Method
1. City = GHS-UCDB R2024A polygon (`load_cities()`), split along the 3-degree tile grid (polygons crossing a tile boundary use both tiles; max 2 tiles).
2. Per tile, the polygon part is rasterised on the tile's exact pixel grid (`rasterio.features.geometry_mask`, pixel centre inside polygon, not all_touched), in strips of 3000 rows, so memory stays bounded (whole run for 86 cities about 3 min from an empty cache).
3. Each pixel's area is the spherical zone area `R^2 * dlon * (sin lat_top - sin lat_bottom)`, R = 6371.0088 km, i.e. proportional to cos(latitude). Class areas are summed per raw value (value 0 = no data; tiles absent from the product count as no data).
4. Check of the rasterisation: sum of pixel areas / UCDB `GC_UCA_KM2_2025` = 0.9974 to 0.9981 for all 86 cities (median 0.9977; UCDB area is a different ellipsoid/rounded). Valid-pixel coverage of the polygon = 1.000 for all 86 (no nodata pixels, no absent tiles).
5. Shares: `land = valid - class80`. tree/green/built are % of `land`; `water_share` is % of all valid polygon area. All 11 class shares (% of land, water excluded) are in `detail.land_share_pct`.

## Metrics (all `quality: observed`, year 2021, unit %)
Observed = satellite classification aggregated by us; it is a classified map with ~77% overall accuracy, not a survey, so treat small differences between cities as noise.

| key | definition | summary over 86 cities (min / median / max) |
|---|---|---|
| `tree_share` | class 10 area / land area | 1.5 / 24.4 / 55.4 |
| `green_share` | classes 10, 20, 30, 90, 95 / land area | 5.1 / 38.7 / 64.1 |
| `water_share` | class 80 area / valid polygon area | 0.0 / 4.1 / 26.5 |
| `built_share` | class 50 / land area (reference/validation) | 7.4 / 54.1 / 78.8 |

`detail` per value: coverage, land_km2, water_km2, polygon_area_pixels_km2, ucdb_area_km2, tiles, tiles_absent, nodata_km2, land_share_pct (all classes), water_pct_of_valid_area, green_incl_crop_share.

### Decisions and justification
- **Cropland excluded from `green_share`.** Inside UCDB polygons cropland is farmland on the fringe (Cairo 21.5% of land, Tokyo 8.3%), not accessible urban green or amenity; including it would reward cities for sprawling over fields. The variant including class 40 is kept in `detail.green_incl_crop_share` for sensitivity.
- **Shrubland, grassland, herbaceous wetland, mangrove included** (all vegetated, non-farmed). Caveat: in arid cities classes 20/30 are partly natural desert scrub, not urban greenery (Dubai: 1.7% shrub + 1.1% grass). Bare ground (Dubai 25%, Lima 30%) stays in the land denominator and not in the numerator, which is intended.
- **Moss/lichen (100) and snow/ice (70) excluded** (not urban green; ~0 here).
- **Land denominator excludes permanent water** so a city with a big bay/lake is not penalised as less green. `water_share` is given separately over total area.
- **`water_share` limitations**: the UCDB polygon follows the built-up/land mask, so open sea is mostly outside it; the water inside is harbours, bays, lakes, reservoirs, wide rivers and ponds, with no distinction between sea, lake and river. A high value (Hong Kong 26.5, Reykjavik 23.0, Manila/Auckland 17.1, Helsinki 16.0) indicates waterfront/inland water inside the city boundary, but a low value does not mean "not on the sea" (e.g. a city whose polygon stops at the shore). It also does not measure access or visibility of water. Class 80 omits small rivers under 10 m width and tidal flats (mapped as bare/wetland). Use it as a coarse "water in the city" proxy, not as a sea-view metric.
- **`built_share`** is class 50 (buildings, roads, railways; parks are not built-up per the PUM). It is for reference and validation; the dense-core/greenspace trade-off in a city is better read from `tree_share`.

## Accuracy and known confusions (Product Validation Report V2.0, verified in the cached PDF)
- Global overall accuracy of v200: **76.7 +- 0.5%** (2.16 M sample units at 21,624 locations; confusion matrix in Table 2 of the PVR). Per class (user's / producer's accuracy, global): tree 80.0 / 91.9; shrubland 49.1 / 46.9; grassland 71.9 / 66.7; cropland 80.6 / 79.3; built-up 65.9 / 73.2; bare 92.1 / 82.5; water 89.4 / 86.4; herbaceous wetland 30.5 / 44.6; mangrove 74.1 / 46.2.
- The PVR says there is a slight global over-estimation of tree cover. Shrubland, grassland and wetland are the weakest classes, so `green_share` carries more uncertainty than `tree_share`.
- These are global figures, not urban-specific. Within cities the main confusions are tree cover vs built-up (a street tree canopy over a road, 10 m mixed pixels), built-up vs bare (PUM: "spectral mixing leading to confusion between bare areas and urban") and grass vs cropland. All continents have overall accuracy above 72%, highest for Asia at 82.1% (PVR Table 3); the PVR attributes lower Oceania/Eurasia accuracy to shrub/grass/tree confusions in open woodland and tundra. No uncertainty interval per city is available.
- A pixel is 10 m: private gardens and street trees under 10 m wide are mixed into the dominant class, so garden-heavy low-density cities and tree-lined dense cities are both only roughly resolved.

## Validation (86 target cities, same polygons)
### Sanity ranking of `green_share` (rank 1 = lowest of 86)
- Lowest: Lima 5.1, Dubai 6.0, Cairo 11.1, Tehran 14.6, Dakar 17.5, Accra 19.4, Los Angeles 20.2, Osaka 20.3, Fukuoka 20.8, Sapporo 21.4. Expected low-green cities (Dubai, Cairo, Lima) are ranks 2, 3, 1.
- Highest: Stockholm 64.1, Seattle 61.0, Berlin 58.7, Oslo 57.9, Helsinki 57.2, Reykjavik 56.6, Zurich 54.0, Hong Kong 53.4, Warsaw 53.4, Vancouver 53.0. Helsinki (rank 82) and Vancouver (rank 77) are high as expected.
- Singapore is 37.9 (tree 30.2), rank 42/86, just under the median (38.7). The "garden city" reputation is not visible at the 10 m class level within the UCDB polygon (59.6% built-up); this is a data result, do not adjust it by hand.
- Osaka/Fukuoka/Sapporo are low because 70-73% of their land is built-up (trees 17-18%), with 5-7% cropland excluded from green.

### Against GHS-UCDB LULC theme (`GHSL_UCDB_THEME_LULC_GLOBE_R2024A`)
`LU_HEC_<class>_2019` are hectares from **Copernicus Global Land Service land cover CGLS-LC100 Collection 2** (Buchhorn et al. 2020, doi:10.3390/rs12061044), 100 m, reference years 2015/2019 (UCDB PDF indicator sheets). Classes: 20 shrubs, 30 herbaceous, 40 cultivated, 50 urban, 60 bare, 70 snow, 80 water, 90 wetland, 100 moss, 111-126 forests (tree analogue). I rebuilt the same shares from it (land = sum minus 80; tree = sum of forest classes 111-126; green = tree + 20 + 30 + 90):

| metric | Spearman | Pearson | mean WorldCover | mean CGLS |
|---|---|---|---|---|
| tree_share | 0.60 | 0.58 | 25.7 | 8.3 |
| green_share | 0.28 | 0.29 | 37.4 | 13.7 |
| built_share | 0.26 | 0.42 | 54.6 | 76.6 |
| water_share | 0.21 | 0.14 | 5.8 | 1.3 |

Agreement is only moderate for tree and weak for the others. Explanation: CGLS-LC100 is 100 m, and a 100 m pixel containing mostly buildings is classed "urban" whatever tree cover sits in it, so it treats cities as 77% built-up and trees are systematically hidden (e.g. Berlin tree 5.9% vs 52.5%, Copenhagen 0.6% vs 29.0%, Edinburgh and Dublin 0% vs 31.8% / 25.3%). In addition CGLS "forest" needs closed canopy >15% at 100 m, and CGLS has virtually no water inside polygons (Tokyo 0, Copenhagen 0, Singapore 0 vs WorldCover 5.6 / 10.6 / 11.6), because the UCDB LULC stats cover land cells and the permanent-water class at 100 m misses channels and bays. The largest rank disagreements on green_share are Dakar (WC 17.5 vs CGLS 32.0), Fukuoka (20.8 vs 30.8), Lagos, Ulaanbaatar, Bogota (CGLS higher, probably grass/shrub classes in dry or hilly surroundings) and Berlin, Copenhagen, Prague, Amsterdam, Zurich (WC much higher, CGLS puts them in "urban"). The 10 m WorldCover is the finer product for tree cover inside urban areas; I did not use CGLS as the primary source for that reason. The CGLS comparison therefore validates ordering of trees only loosely and is not an independent accuracy test.
- Median ratio of CGLS class total to UCDB polygon area is 0.977, i.e. the LULC theme covers nearly the full polygon.

### Against GHS-UCDB GREENNESS theme (`GHSL_UCDB_THEME_GREENNESS_GLOBE_R2024A`, 2020; Landsat 8 NDVI within GHS-BUILT-S built-up pixels)
Spearman correlation across 86 cities with WorldCover:

| UCDB field | tree_share | green_share | built_share |
|---|---|---|---|
| GR_SHB_GRN_2020 (share of built-up in green area) | 0.85 | 0.83 | -0.69 |
| GR_SHB_HGR_2020 (share of built-up in high-green area) | 0.65 | 0.65 | -0.58 |
| GR_AVG_GRN_2020 (mean greenness in built-up area) | 0.70 | 0.51 | -0.25 |
| GR_CTH_AVG_2020 (mean canopy height) | 0.55 | 0.62 | -0.85 |

Strong agreement (0.83-0.85) with the independent NDVI-based measure of how green the built-up area is. `GR_AVG_GRN` is weaker for `green_share` because mean NDVI also reflects climate/phenology (arid vs humid) and sensor date and not the share of vegetated pixels; the built_share relation with canopy height (-0.85) is plausibly driven by the dense tall-canopy vs paved contrast. These are correlations of different constructs, not an accuracy estimate.

## Missing
None: 86/86 cities have all four metrics (coverage 1.000, no absent tiles, no nodata pixels). Rule if it occurs: a city with valid-pixel coverage < 0.5 gets all four metrics as missing with the reason.

## Caveats for downstream use
- Share of the UCDB urban-centre polygon, not the municipality: polygons differ in how much peri-urban land they include, so `built_share` and `green_share` are partly a function of polygon definition and city size. Normalise or compare cautiously across sizes (the reference set of 524 centres was not computed here; `--reference` flag exists but was not run).
- Date mismatch with CGLS 2019 / NDVI 2020 is minor for the purposes of the validation.
- Class shares are classification outputs with ~77% accuracy; city-level estimates average out random pixel errors but not the systematic ones (tree over-estimation, mixed pixels in dense cores).

## Alternatives considered
- GHS-UCDB LULC theme (CGLS-LC100, 100 m): already in the project but it hides urban trees (above) and lacks inland water; kept for validation only.
- GHS-UCDB GREENNESS theme (Landsat NDVI in built-up pixels): good as a cross-check but measures greenness only inside built-up pixels and is a non-physical index; kept for validation only.
- Dynamic World 10 m (Google Earth Engine; needs account and a per-image time series) and ESRI 10 m land cover (annual, licence CC BY 4.0 but derived by a proprietary model): not used because WorldCover is open-access and static, and one version avoids mixing; not tested here.
- Direct tree-canopy products (e.g. Hansen/Meta canopy height) were not evaluated in this module.
