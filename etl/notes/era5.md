# ERA5 climate normals (`era5`)

Module: `etl/soulcity_etl/era5.py` (`cd etl && UV_SYSTEM_CERTS=1 uv run python -m soulcity_etl.era5`).
Outputs: `data/interim/era5.json` (86 target cities), `data/reference/era5.csv` (524 reference centres),
validation numbers also in `.cache/raw/era5/validation.json` and in the `notes` of the interim file.
A full run from an empty cache streams about 215 GB (about 35 min at the ~170 MB/s we measured). A rerun from the
cache (about 130 MB of per-cell arrays and station files) takes about 1 min.

## Metrics

All metrics cover the **1990–2019** climatology (`year: "1990-2019"`). The spatial unit is ERA5 0.25° grid cells
mapped to the GHS-UCDB R2024A polygon (see *Geographic mapping*).

| key | definition | unit | quality |
|---|---|---|---|
| `temp_warmest` | mean 2 m air temperature of the warmest calendar month, lapse-adjusted to the city's mean elevation | °C | `observed`. It is `estimated` when the lapse adjustment is larger than 0.5 K (23 cities). |
| `temp_coldest` | same, for the coldest calendar month | °C | same rule as `temp_warmest` |
| `seasonal_range` | `temp_warmest − temp_coldest`. The lapse shift cancels out. | K (°C difference) | observed |
| `precip_annual` | mean annual total precipitation | mm/yr | observed |
| `cloud_cover_annual` | mean total cloud cover (ERA5 `tcc`, fraction × 100). This is the proxy for "sunshine". | % | observed |
| `dewpoint_max_month` | highest monthly mean 2 m dewpoint, i.e. the "muggiest month". **This is the recommended humidity metric.** | °C | observed |
| `dewpoint_warmest` | mean 2 m dewpoint of the warmest month (by temperature). Kept because the brief asked for it. | °C | observed |

The `detail` of `temp_warmest` holds the 12 lapse-adjusted monthly mean temperatures (`monthly_temp_c`), the annual
mean, `unadjusted_c`, `lapse_adjustment_K`, `era5_orography_m`, `ucdb_elev_m`, `elev_diff_m`, `cell_rule`,
`n_cells`, `n_centres_in_polygon`, `nearest_km` (for the fallback rule), the 2010 diurnal-sampling bias, and the
GHCN-M station normal where one exists. `precip_annual.detail.monthly_precip_mm` holds the 12 monthly totals, plus
the GHCN-M station normal and `era5_to_station_ratio` where available. `dewpoint_warmest.detail.monthly_dewpoint_c`
holds the 12 monthly dewpoints.

The two dewpoint metrics differ by more than 1 K only for monsoon and tropical-highland cities, where the hottest
month comes before the wet season: New Delhi (Jun → Aug, +4.1 K), Bogotá (+4.2 K), Mexico City (+3.6 K), Addis Ababa
(+3.3 K), Bengaluru (+3.0 K), Quito (+2.9 K), Nairobi (+1.8 K) and Ho Chi Minh (+1.1 K). For "how muggy does it
get", `dewpoint_max_month` is the defensible measure.

Considered and dropped:
- **Sunshine hours / surface solar radiation.** The store has no sunshine-duration variable and no downward
  surface SW (`ssrd`). `mean_surface_net_short_wave_radiation_flux` and all other `mean_*_flux` arrays in the
  WB2 climatology are **entirely NaN**: every chunk is the same 150,877-byte fill block. Net SW is also mixed with
  surface albedo (snow), so it is not a cleaner sunshine proxy than cloud fraction.
- **Annual mean temperature.** It is only stored in `detail`, because the quiz uses the warmest and coldest months.

## Source and method

### Inputs (all recorded in `data/provenance/downloads.json`)
1. **WeatherBench 2 ERA5 hourly climatology 1990–2019**, `https://storage.googleapis.com/weatherbench2/datasets/era5-hourly-climatology/1990-2019_6h_1440x721.zarr`
   (zarr v2, consolidated `.zmetadata` whose sha256 is recorded).
   - Variables are `[hour=4 (0, 6, 12, 18 UTC), dayofyear=366 (1..366), latitude=721 (90 → −90, descending), longitude=1440 (0 … 359.75)]`,
     float32, blosc-lz4 chunks `[3, 3, 721, 1440]`.
   - WB2 computes each value as the mean over 1990–2019 of that UTC hour on that day of year. The value is
     smoothed with a 61-day **triangular** window (`weatherbench2/utils.py: create_window_weights`,
     `compute_rolling_stat`; `scripts/compute_climatology.py --window_size=61`). Day 366 is filled from day 365
     in non-leap years.
   - Used for: `total_precipitation_24hr` (units `m`), `total_cloud_cover` (0–1), and `2m_temperature` (only to
     measure the smoothing effect).
2. **WB2 copy of hourly ERA5**, `…/datasets/era5/1959-2023_01_10-full_37-1h-0p25deg-chunk-1.zarr`. It has one chunk
   per hour, 721 × 1440.
   - The climatology's `2m_dewpoint_temperature` is all NaN, so dewpoint had to come from here. We streamed
     **every 00/06/12/18 UTC field of 1990–2019** (43,830 time steps) for `2m_dewpoint_temperature` and
     `2m_temperature`, and formed plain (unsmoothed) monthly means. The time axis is checked to be contiguous
     hours since 1959-01-01.
   - Temperature comes from this store, not from the smoothed climatology, so that `temp_*` and the dewpoint
     metrics use the same standard definition (a monthly normal).
   - 48 days of 2010 (the 1st, 8th, 15th and 22nd of each month) × 24 h were also read to measure the 6-hourly
     sampling bias.
3. **WB2 ERA5 static fields**, `…/datasets/era5/1959-2022-6h-1440x721.zarr`: `land_sea_mask` (0–1) and
   `geopotential_at_surface` (m² s⁻²). Model orography = z / 9.80665.
4. Validation only:
   - GHS-UCDB CLIMATE (`CL_B01_CUR_*`, `CL_B12_CUR_*`) and GEOGRAPHY (`GE_ELV_AVG_2025`) theme layers.
   - GHCN-M v4 TAVG QCF, `https://www.ncei.noaa.gov/pub/data/ghcn/v4/ghcnm.tavg.latest.qcf.tar.gz`.
   - GHCN-M v4 precipitation (inventory plus 466 per-station CSVs under `https://www.ncei.noaa.gov/data/ghcnm/v4/precipitation/`).

The chunks are streamed in one pass per variable (8–16 threads). Each chunk is decoded with `numcodecs` (blosc),
only the needed cells are kept, and the chunk is then discarded. Nothing larger than the per-cell arrays is written
to disk. The cell set is the union over the 86 targets and the 524 reference centres: **662 cells**.

### Geographic mapping (UCDB polygon → ERA5 cells)
- **Rule 1** (`centres_in_polygon_land`): every ERA5 cell whose centre lies inside the UCDB polygon and whose
  `land_sea_mask` is ≥ 0.5. The city value is the cos(latitude)-weighted mean over those cells.
- **Rule 2** (`nearest_land_cell_to_representative_point`): if Rule 1 finds no cell, the land cell (lsm ≥ 0.5)
  nearest (great-circle) to the polygon's `point_on_surface`, searched within ±2°.
- If neither rule finds a cell, the value is missing.
- Targets: 64 use Rule 1 and 22 use Rule 2. Cells per city: 1 cell for 51 cities, 2 for 15, 3 for 10, and up to
  9 (Dhaka).
- Rule 2 cities, with distance to the cell in km: Barcelona 6.8, Bogotá 18.7, Cape Town 15.9 (its single
  in-polygon centre is sea), Casablanca 13.3, Dublin 9.7, Edinburgh 7.5, Havana 14.8, Hong Kong 21.2, Honolulu 21.8,
  Kathmandu 9.7, Marrakesh 13.1, Montevideo 12.5, Munich 12.7, Oslo 13.2, Prague 9.7, Reykjavík 14.4, Rome 14.4,
  Sapporo 12.4, Singapore 19.1, Tbilisi 5.1, Ulaanbaatar 11.0, Zurich 11.5.
- A 0.25° cell (~28 × 28 km at the equator) is usually larger than these polygons, so the polygon and the cell
  footprint do not match well. Rule 2 cities are represented by one cell up to 22 km away, and that cell's
  orography is corrected for (temperature only; see below).
- Reference set: 254 centres use Rule 1, 269 use Rule 2, and **1 is missing**: `uc-4512` Naha (Okinawa). It has no
  ERA5 land cell within 2°, because the island is below lsm 0.5 at 0.25°.

### Conversions
- **Monthly temperature and dewpoint**: the mean of all 00/06/12/18 UTC values in that calendar month over
  1990–2019, minus 273.15. The annual mean is weighted by month length.
- **Warmest and coldest month**: the argmax and argmin of the 12 city-mean monthly temperatures.
- **Precipitation**:
  - Semantics: `total_precipitation_24hr` at hour h is the ERA5 accumulation over the 24 h ending at h (WB2
    `AggregatePrecipitationAccumulation`, which sums `total_precipitation_6hr`). Its climatology is the mean
    24-h total in metres.
  - Daily mean (mm/day) = mean over the 4 end hours × 1000. Check: the annual mean of tp24 differs between the
    four end hours by at most 0.79 % (cells wetter than 0.3 mm/day). This is what you expect if all four are
    full-day accumulations.
  - Day-of-year to month mapping: day of year 1..365 uses a 365-day calendar, and day 366 is dropped. In the
    7 leap years out of 30, dates after 28 Feb are shifted by one day. Against the 61-day smoothing this is
    negligible.
  - Monthly total = mean daily mm × the mean month length over 1990–2019. February is 28 + 7/30 days
    (1992, 1996, 2000, 2004, 2008, 2012 and 2016 are leap years), so the year is 365.233 days.
  - Annual = the sum of the 12 monthly totals.
- **Cloud cover**: the mean over 4 hours × 365 days × 100.

### Lapse-rate decision (temperatures only)
ERA5 2 m temperature is valid at the model orography. Mean |UCDB elevation − ERA5 orography| over the 86 targets is
67 m (mean −55 m: cities sit in valleys below the smoothed model terrain). It exceeds 100 m for 19 cities and
300 m for 3: Almaty −631 m, Tehran −536 m, Tbilisi −414 m. Mexico City is −289 m; Bogotá is +169 m (its fallback
cell is lower).

We tested a correction against **independent stations** (GHCN-M v4 QCF).
- Stations: those **inside** the 524 reference polygons, each with a 1990–2019 normal of at least 20 valid years
  in every month. That gives 356 stations in 248 centres. One station was dropped because its inventory
  elevation was more than 1 km from the city's GLO-90 mean (a Buenos Aires station listed at about 3,300 m).
- Comparison: city ERA5 annual mean vs the mean of the stations, with and without shifting ERA5 by
  −6.5 K/km × (station elevation − ERA5 orography).

| | bias | MAE | RMSE |
|---|---|---|---|
| ERA5 raw − station (248 centres) | −0.68 K | 0.84 K | 1.12 K |
| ERA5 lapse-adjusted − station | −0.31 K | **0.59 K** | **0.73 K** |
| raw, the 29 centres with \|Δz\| > 200 m | −2.02 K | 2.12 K | |
| lapse-adjusted, \|Δz\| > 200 m | −0.16 K | **0.68 K** | |

- A regression of (station − ERA5) on Δz gives an empirical lapse rate of **5.2 K/km**, close to the standard 6.5.
- Example targets, ERA5 − station before → after: Tehran −5.35 → −1.54, Almaty −4.77 → −0.93, Lima −0.82 → +1.69
  (a coastal inversion, where a lapse rate is the wrong physics), Taipei −1.78 → −0.18, Vancouver −1.63 → −0.19,
  Kathmandu −1.37 → −0.14, Cape Town −1.17 → −0.06, Bogotá +1.52 → +0.75.

**Decision.**
- We apply the ICAO / U.S. Standard Atmosphere 1976 tropospheric lapse rate, **6.5 K/km**. It is an external
  constant, not fitted to our data.
- The shift goes from the ERA5 orography to the **city mean elevation** (`GE_ELV_AVG_2025`, from Copernicus
  GLO-90), and applies to every monthly temperature. `seasonal_range` is therefore unchanged.
- The shift is applied to all cities for consistency. Values whose shift is larger than 0.5 K are labelled
  `quality: "estimated"`. That covers 23 targets: Almaty +4.10, Tehran +3.48, Tbilisi +2.69, Mexico City +1.88,
  Ulaanbaatar +1.23, Lima +1.17, Bogotá −1.10, Cape Town +1.10, Taipei +1.08, Vancouver +1.06, Kathmandu +1.05,
  Oslo +0.90, Reykjavík +0.85, Rio +0.84, Osaka +0.80, Zurich +0.79, Honolulu +0.74, Dublin +0.72,
  San Francisco +0.71, Los Angeles +0.61, Barcelona +0.54, Rome +0.51, Fukuoka +0.50.
- The unadjusted value is kept in `detail.unadjusted_c`.
- **Dewpoint is not adjusted.** The dewpoint lapse rate depends on the regime, and we had no station test for it.
  This is flagged by `elev_diff_m` in `temp_warmest.detail`.
- High-altitude cities named in the brief have small orography mismatches, so their ERA5 temperatures already
  reflect their altitude: Quito −63 m, Addis Ababa, Nairobi, Denver, Johannesburg. The exceptions are Mexico City
  (−289 m) and Bogotá (+169 m).

## Validation

### 1. GHS-UCDB CLIMATE theme
- What the columns are: `CL_B01_CUR_2010` is the "Annual Mean Temperature in the decade" (°C) and
  `CL_B12_CUR_2010` the "Annual Precipitation mean in the decade" (mm/yr). Both come from *Wouters (2021), Global
  bioclimatic indicators from 1979 to 2018 derived from reanalysis*, C3S CDS, DOI 10.24381/cds.bce175f0 (UCDB
  R2024 V1.2 PDF, pp. 356/365). UCDB takes the zonal average of the pixels *touching* the urban centre.
- **That dataset is itself derived from ERA5**, on a coarser 0.5° grid. So this comparison checks our pipeline
  (units, period, aggregation), not ERA5. Unadjusted ERA5 is compared here.

| comparison | n | temp r | temp bias | temp MAE | precip r | precip mean bias | median ratio |
|---|---|---|---|---|---|---|---|
| targets vs `_CUR_2010` | 86 | 0.983 | −0.12 K | 0.83 K | 0.939 | −27 mm | 0.991 |
| targets vs mean of `_CUR_1990/2000/2010` | 86 | 0.983 | +0.13 K | 0.77 K | 0.943 | −16 mm | 0.996 |
| 523 reference centres vs mean of the 3 decades | 523 | 0.983 | +0.06 K | 0.68 K | 0.889 | +13 mm | 1.003 |

- Largest temperature gaps (ours − UCDB, 3-decade mean): Denver +5.6, Zurich +3.9, Kathmandu −3.8, Tehran −3.7,
  Marrakesh +3.7, Almaty +2.5 K. These are mountain-edge cities, where UCDB's 0.5° "touching" pixels include
  mountains (Denver, Zurich, Marrakesh) or lowland (Tehran, Kathmandu). GHCN stations side with our value: Denver
  ERA5 − station is −1.4 K, while UCDB would be −7 K.
- Largest precipitation gaps: Quito −991 mm (ratio 0.74), Addis Ababa +919 mm (1.96), Vancouver +773 mm (1.49),
  Kathmandu +586 mm, Jakarta −567 mm, São Paulo −438 mm. These are the same kind of resolution and edge effects.

### 2. Independent stations (GHCN-M v4)
- Temperature: see the lapse table above. After adjustment, a **−0.3 K cold bias** remains against urban stations.
  This is consistent with ERA5 having no urban canopy (no urban heat island). It is not corrected.
- Precipitation: 201 reference centres and 357 stations, each with a 1990–2019 normal and at least 20 valid years
  per month.

| | value |
|---|---|
| Pearson r | 0.84 |
| r of the logs | 0.93 |
| median ERA5 / station | 1.06 |
| mean bias | +77 mm |
| share within ±25 % | 70 % |
| share with ratio > 1.5 | 7 % |

  Targets outside 0.67–1.5×:

  | target | ERA5 / station | mm (ERA5 vs station) |
  |---|---|---|
  | Bogotá | **3.14** | 2,699 vs 859 |
  | Quito | 1.96 | 2,882 vs 1,472 |
  | Kathmandu | 1.92 | 2,818 vs 1,471 |
  | Santiago | 1.82 | |
  | Cape Town | 1.59 | |
  | Mexico City | 1.52 | |
  | Sydney | 0.67 | |
  | Mumbai | 0.64 | |

  This is the known ERA5 wet bias over steep tropical and sub-tropical orography, and its under-resolution of
  coastal and orographic gradients. The values are **not altered**. The ratio is exposed in
  `precip_annual.detail.era5_to_station_ratio` so that downstream code or the UI can caveat them. Bogotá's ERA5
  value should be treated as unreliable.
- 6-hourly sampling bias, measured on 48 days × 24 h of 2010: the mean of 24 hourly values minus the mean of
  00/06/12/18 UTC.
  - t2m over the targets: mean +0.01 K, range −0.34 (Bengaluru) to +0.27 K (Quito). Tehran −0.26, Santiago
    +0.26, Mumbai −0.23.
  - Cloud cover: mean +0.1 points, at most 2.8 points.
  - This is small because 4 equally spaced samples cancel diurnal harmonics 1–3 exactly. Not corrected; the
    per-city value is in `detail`.
- Smoothing effect of the WB2 climatology (61-day triangular window), comparing the smoothed t2m climatology with
  our unsmoothed monthly means:
  - Warmest month is on average 0.19 K too cool (up to 0.49 K).
  - Coldest month is 0.20 K too warm (up to 0.71 K).
  - The annual mean is identical (≤ 0.005 K).
  - This is why temperature is taken from the hourly store. Monthly precipitation in `detail` *is* smoothed in the
    same way (its annual total is not affected).

### 3. Sanity (86 targets): min / max
| metric | min | max | median |
|---|---|---|---|
| temp_warmest | 12.5 °C Reykjavík | 35.9 °C Dubai | 23.6 |
| temp_coldest | −21.9 °C Ulaanbaatar | 26.5 °C Ho Chi Minh | 9.4 |
| seasonal_range | 0.9 K Quito | 40.1 K Ulaanbaatar | 13.3 |
| precip_annual | 21 mm Cairo | 2,882 mm Quito (wet-biased, see above) | 879 |
| cloud_cover_annual | 18.5 % Dubai | 87.9 % Bogotá | 59.9 |
| dewpoint_max_month | 4.4 °C Tehran | 25.9 °C Dhaka | 16.1 |
| dewpoint_warmest | 4.4 °C Tehran | 25.9 °C Dhaka | 16.0 |

Spot checks: Tokyo Aug 26.9 / Jan 4.9 °C, 1,536 mm. London Jul 17.8 / 5.2 °C, 691 mm. Singapore 27.5 / 26.0 °C,
2,666 mm. Dubai 35.9 / 19.7 °C, 81 mm. Helsinki 18.1 / −4.8 °C. All are plausible.

## Missing
- Targets: **none** (86/86 for all 7 metrics, missing rate 0 %).
- Reference set: `uc-4512` Naha, because it has no ERA5 land cell (lsm ≥ 0.5) in the polygon or within 2°.

## Known biases and caveats
- **Resolution.** A 0.25° grid with 1–9 cells per city does not resolve the urban heat island, coastal fog belts
  (Lima, San Francisco) or valley-floor inversions (Almaty, Santiago, Ulaanbaatar winter).
- **Urban bias.** ERA5 is about 0.3 K cooler than urban stations after the lapse adjustment.
- **Precipitation over steep terrain.** Wet-biased by up to ×2–3 (Bogotá, Quito, Kathmandu). Dry-biased on some
  monsoon coasts (Mumbai 0.64×).
- **Fallback cells.** 22 targets use a single neighbouring cell up to 22 km away.
- **Cloud cover is not sunshine.** It is model total cloud fraction (all levels), which ignores day length and
  optical thickness. It ranks sunniness reasonably but is not sunshine hours.
- **Mixed sources inside ERA5.** Temperature and dewpoint are unsmoothed monthly normals. Precipitation and cloud
  come from the WB2 smoothed climatology. Annual quantities are unaffected; monthly precipitation is smoothed by
  about one month.

## License and attribution
- **ERA5 (C3S).**
  - The CDS catalogue entry for *ERA5 hourly data on single levels* (DOI 10.24381/cds.adbb2d47), fetched from
    `https://cds.climate.copernicus.eu/api/catalogue/v1/collections/reanalysis-era5-single-levels` and cached, has
    `"license": "CC-BY-4.0"` and links to `https://spdx.org/licenses/CC-BY-4.0`. The CDS licence text
    (`cc-byv1…md` in the CDS object store) says: *"This dataset is released for use under the CC-BY licence."*
  - The WB2 bucket ships the older licence at `gs://weatherbench2/datasets/era5-hourly-climatology/LICENSE` and
    `…/era5/LICENSE` (both cached). It is "Licence to Use Copernicus Products", whose §4.2 says *"Access to
    Copernicus Products is given for any purpose in so far as it is lawful"*. Its §5.1.2 says: *"Where the Licensee
    makes or contributes to a publication or distribution containing adapted or modified Copernicus Products, the
    Licensee shall provide the following or any similar notice: 'Contains modified Copernicus Climate Change
    Service information [Year]'"*. Its §5.1.3 says the publication *"shall state that neither the European
    Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it
    contains."*
  - Both licences allow commercial and public use with attribution.
  - **Required attribution text:** "Contains modified Copernicus Climate Change Service information (ERA5,
    1990–2019) [2026]. Neither the European Commission nor ECMWF is responsible for any use that may be made of the
    Copernicus information or data it contains." Also cite Hersbach et al. (2020), *The ERA5 global reanalysis*,
    QJRMS 146:1999–2049, doi:10.1002/qj.3803, and the C3S dataset DOI 10.24381/cds.adbb2d47.
  - Data access via WeatherBench 2 (Rasp et al. 2024, JAMES, doi:10.1029/2023MS004019). WB2 code is Apache-2.0;
    WB2 says to "check the LICENSE files for each dataset in the respective GCS buckets".
- **GHCN-M v4 (NOAA NCEI).** Used for validation only. Station normals appear only as diagnostics in `detail`.
  The NCEI product page gives no licence or use restriction. Cite Menne et al. (2018), J. Climate,
  doi:10.1175/JCLI-D-18-0094.1 (temperature), and NCEI GHCNm v4 precipitation, metadata gov.noaa.ncdc:C00839.
- **GHS-UCDB** (polygons, elevation, CLIMATE theme): see the GHSL module notes.

## Alternatives considered
- **Copernicus CDS API** (ERA5 monthly means, ERA5-Land 0.1°): needs an account key we do not have. ERA5-Land
  would be better for mountain cities.
- **Open-Meteo climate API**: quota-blocked; it is also an ERA5 re-serve.
- **UCDB CLIMATE theme**: only annual temperature and precipitation, at a coarser 0.5° grid with "touching
  pixel" aggregation, and no monthly values. Used for validation only.
- **WorldClim / CHELSA** (1 km, station-interpolated, better in mountains): not tried in this run, and their licence terms would have to
  be read first. This is a candidate if the precipitation
  caveats above matter.
- **WB2 1990–2017 climatology**: the same NaN dewpoint and radiation fields, and a shorter period.
