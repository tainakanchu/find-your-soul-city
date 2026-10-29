"""Integrity checks on committed ETL outputs (no network; runs in CI)."""

import csv
import itertools
import json
import math
import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
INTERIM = REPO / "data" / "interim"
QUALITIES = {"observed", "estimated", "imputed"}
CITY_IDS = {c["city_id"] for c in yaml.safe_load((REPO / "etl/config/cities.yaml").read_text())["cities"]}


def interim_files():
    return [p for p in sorted(INTERIM.glob("*.json")) if p.stem != "city-attributes"]


def test_interim_values_are_real_and_traceable():
    downloads = json.loads((REPO / "data/provenance/downloads.json").read_text())
    for p in interim_files():
        d = json.loads(p.read_text())
        assert d["source_id"] == p.stem
        assert d["inputs"], f"{p.name}: no recorded inputs"
        for key in d["inputs"]:
            assert any(key == k or k.startswith(key) for k in downloads), f"{p.name}: input {key} not in downloads.json"
        for metric, by_city in d["values"].items():
            for city, e in by_city.items():
                assert e["quality"] in QUALITIES, (p.name, metric, city)
                assert isinstance(e["value"], (int, float)) and math.isfinite(e["value"]), (p.name, metric, city)
                assert e["year"] is not None
                assert city not in d["missing"].get(metric, {}), f"{p.name}: {metric}/{city} both value and missing"
        for metric, by_city in d["missing"].items():
            for city, reason in by_city.items():
                assert isinstance(reason, str) and len(reason) > 10, (p.name, metric, city)


def test_every_target_city_is_covered_or_explained():
    for p in interim_files():
        d = json.loads(p.read_text())
        for metric in d["values"]:
            seen = set(d["values"][metric]) | set(d["missing"].get(metric, {}))
            assert CITY_IDS <= seen, f"{p.name}: {metric} silently skips {sorted(CITY_IDS - seen)}"


def test_no_placeholder_anywhere_in_generated_cities():
    for p in (REPO / "knowledge/cities").glob("*.md"):
        text = p.read_text()
        assert "placeholder" not in text and "demo-placeholder" not in text, p.name


def test_reference_distribution_is_monotone():
    text = (REPO / "knowledge/model/reference-distribution.md").read_text()
    fm = yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL).group(1))
    for key, r in fm["metrics"].items():
        q = r["quantiles"]
        assert len(q) == len(fm["levels"]) and all(a <= b for a, b in itertools.pairwise(q)), key
        assert r["n"] >= 400, key


def test_reference_csvs_cover_the_reference_set():
    for p in (REPO / "data/reference").glob("*.csv"):
        with p.open() as f:
            rows = list(csv.DictReader(f))
        assert len(rows) >= 520, p.name
