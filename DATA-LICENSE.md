# Data license

The city metric data produced by this project — `data/`, `knowledge/cities/`, `knowledge/model/reference-distribution.md`
and the generated `src/generated/knowledge.json` — is made available under the
[Open Database License (ODbL) v1.0](https://opendatacommons.org/licenses/odbl/1-0/).
Individual contents are under the [Database Contents License v1.0](https://opendatacommons.org/licenses/dbcl/1-0/).
The method used to produce it is the ETL in `etl/` (ODbL §4.6).

This license covers the data only. The application source code is under the MIT License (`LICENSE`).

## Sources and required attribution

- **GHS-UCDB R2024A** and **GHS-POP R2023A** © European Union, 1995–2026, CC BY 4.0.
  Mari Rivero, I. et al. (2024), doi:10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd.
  Schiavina, M. et al. (2023), doi:10.2905/2FF68A52-5B5B-4A22-8F40-C41DA8332CFE.
  The PM2.5 column of GHS-UCDB is derived from WUSTL ACAG SatPM2.5 (Shen et al. 2024).
- **ERA5**: Contains modified Copernicus Climate Change Service information (ERA5, 1990–2019) [2026].
  Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus
  information or data it contains. Hersbach et al. (2020), doi:10.1002/qj.3803. Accessed via WeatherBench 2.
- **ESA WorldCover**: © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021)
  processed by ESA WorldCover consortium. Zanaga, D. et al. (2022), doi:10.5281/zenodo.7254221.
- **ITDP Atlas of Sustainable City Transport**: Contains information from the Atlas of Sustainable City Transport
  (ITDP, atlas.itdp.org, release update_2024), which is made available under the Open Database License (ODbL).
  Based on OpenStreetMap data © OpenStreetMap contributors.

All values above are aggregated or otherwise modified by this project; see `knowledge/sources/` and `etl/notes/`.
