# ETL brief (shared by all source modules)

Project: "find your soul city" — a web quiz that ranks world cities by fit to a user's stated preferences.
Repo: /home/user/find-your-soul-city. Python ETL lives in `etl/` (uv project; run with
`cd etl && UV_SYSTEM_CERTS=1 uv run python -m soulcity_etl.<module>`; unset UV_NATIVE_TLS if uv warns).
The goal is real, traceable public statistics — NOT a prototype.

## Hard rules

1. No hand-typed numbers, no unfounded estimates. Every value is computed by code from a downloaded/queried input.
2. A value that cannot be computed is recorded as missing with a reason (`Interim.miss`). Never fill gaps.
3. Comparability: a "city" is exactly one GHS-UCDB R2024A urban-centre polygon (`soulcity_etl.cities.load_cities()`,
   EPSG:4326 shapely geometry, plus `reference_centres()` = all 524 centres with pop >= 1M). Compute on that polygon.
   If a source uses another boundary, quantify the mismatch (e.g. IoU / area ratio) and document it; do not silently mix.
4. Record provenance: use `common.fetch()` for file downloads (writes data/provenance/downloads.json) or
   `common.record_dataset()` for remote stores/APIs. Raw data goes under `.cache/raw/<source>/` (gitignored).
5. Output: `common.Interim(source_id=...)` → `data/interim/<source_id>.json`. quality is `observed` (direct
   measurement/official statistic aggregated by us), `estimated` (modelled/derived with a documented assumption),
   or `imputed`. `year` is an int or "YYYY-YYYY" period string. Put diagnostics (n_cells, coverage, etc.) in `detail`.
6. ETL must be re-runnable end to end from an empty `.cache/` (idempotent; cached downloads reused).
7. Pin any new Python dependency through `uv add` (pyproject has exclude-newer; keep it). Don't touch the JS app,
   `knowledge/`, or other agents' modules. Don't run git commit/checkout/reset/stash — the orchestrator commits.
8. Licenses: read the provider's actual license text (URL + quote the operative sentence) — do not guess.
9. External services (knowledge/decisions/external-access-policy.md): use only routes the provider documents for
   data access (downloads, documented APIs, public buckets, releases). Never script a web UI (Shiny/websocket
   handlers, form posts, hidden endpoints, headless browsers) to extract data. Read terms/rate limits first, go
   sequential, use common.fetch(). On 429/5xx/timeouts/"too busy" or any error you caused: stop, don't retry,
   write it in your notes and report it. If only an undocumented route is left, stop and ask the orchestrator.

## Deliverables per source

- `etl/soulcity_etl/<module>.py` with a `main()` runnable as `python -m soulcity_etl.<module>`.
- `data/interim/<source_id>.json` produced by actually running it for all 86 target cities.
- Optionally `data/reference/<source_id>.csv` for the 524-centre reference set (normalisation checks).
- `etl/notes/<source_id>.md`: for each metric — definition, unit, observation year/period, geographic unit and how
  it maps to the UCDB polygon, exact method, source URL(s) + version/DOI, license (quoted, with URL) and attribution
  text required, known biases, validation you performed (with numbers), per-city missing list with reasons, and
  alternative sources you considered and why rejected. Be concrete and numeric; this becomes the public methodology.
- Final message to the orchestrator: short summary of metrics produced, missing rate, validation results, caveats.

## Environment

- Outbound HTTPS works via proxy (CA bundle already configured; requests works). Reachable (checked): jeodpp.jrc.ec.europa.eu,
  storage.googleapis.com (weatherbench2 / arco-era5 public buckets), esa-worldcover.s3.eu-central-1.amazonaws.com,
  planetarycomputer.microsoft.com, overturemaps S3, maps.mail.ru Overpass mirror, api.openstreetmap.org, atlas.itdp.org.
  NOT reachable: overpass-api.de, download.geofabrik.de, Copernicus CDS API (needs key), Open-Meteo (daily quota hit).
- GHS-UCDB R2024A V1.2 gpkg is already at .cache/raw/ghsl/GHS_UCDB_GLOBE_R2024A.gpkg with PDFs
  (.cache/raw/ghsl/GHS_UCDB_GLOBE_R2024A.pdf, GHSL_UCDB_R2024_V1_2.pdf) and the xlsx. Theme layers:
  GHSL_UCDB_THEME_{GENERAL_CHARACTERISTICS,CLIMATE,GREENNESS,GHSL,LULC,INFRASTRUCTURES,GEOGRAPHY,HEALTH,SOCIOECONOMIC,
  EMISSIONS,EXPOSURE,HAZARD_RISK,NATURAL_SYSTEMS,SDG,WATER}_GLOBE_R2024A, keyed by ID_UC_G0. Country names in
  GC_CNT_GAD_2025 have mojibake (e.g. "MÃ©xico").
- Disk: ~30 GB free shared by everyone. Stream big remote arrays; delete large temporaries you no longer need.
- 86 target cities: etl/config/cities.yaml.
