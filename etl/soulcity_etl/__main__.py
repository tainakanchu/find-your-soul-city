"""Run the whole ETL: `pnpm etl` (= `cd etl && uv run python -m soulcity_etl`).

Order: sources (each writes data/interim/<source>.json and data/reference/<source>.csv) ->
build (knowledge/cities, data/processed) -> reference distributions. Cached raw inputs under
.cache/raw are reused; delete them to re-download everything.
"""

import importlib
import sys

STEPS = ["ghsl", "era5", "worldcover", "itdp", "osm", "hazard", "daylight", "opening_hours", "build", "reference"]
WITH_REFERENCE = {"worldcover", "itdp"}  # modules whose reference set is opt-in

if __name__ == "__main__":
    only = sys.argv[1:] or STEPS
    for step in only:
        print(f"=== {step}", flush=True)
        mod = importlib.import_module(f"soulcity_etl.{step}")
        argv = sys.argv
        sys.argv = [step, "--reference"] if step in WITH_REFERENCE else [step]
        try:
            mod.main()
        finally:
            sys.argv = argv
