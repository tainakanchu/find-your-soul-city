"""Merge data/interim/*.json into the knowledge bundle (knowledge/cities/*.md) and data/processed/.

Which metrics end up in the app is decided by knowledge/metrics/*.md: every Metric doc with
`adoption: adopted` is exported, taking its values from data/interim/<source>.json under its
`metric_key`. A city with no value gets `value: null, quality: missing` plus the recorded reason.

Nothing here computes a statistic; it only joins and records provenance.
"""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from .cities import load_cities
from .common import DATA, INTERIM, REPO, now_iso

KNOWLEDGE = REPO / "knowledge"
CITY_DIR = KNOWLEDGE / "cities"
PROCESSED = DATA / "processed"
FM = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def frontmatter(path: Path) -> dict[str, Any]:
    m = FM.match(path.read_text())
    return yaml.safe_load(m.group(1)) if m else {}


def adopted_metrics() -> list[dict[str, Any]]:
    out = []
    for p in sorted((KNOWLEDGE / "metrics").glob("*.md")):
        fm = frontmatter(p)
        if fm.get("type") == "Metric" and fm.get("adoption") == "adopted":
            out.append(fm)
    return out


def load_interim() -> dict[str, dict[str, Any]]:
    return {p.stem: json.loads(p.read_text()) for p in sorted(INTERIM.glob("*.json")) if p.stem != "city-attributes"}


def _yaml_scalar(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False)


def _round(v: float) -> float:
    a = abs(v)
    digits = 0 if a >= 1000 else 1 if a >= 10 else 2
    r = round(v, digits)
    return int(r) if digits == 0 else r


def city_doc(city: Any, attrs: dict[str, Any], rows: list[tuple[dict[str, Any], dict[str, Any]]], at: str) -> str:
    lines = [
        "---",
        "type: City",
        f"title: {_yaml_scalar(city.name_en)}",
        f"description: {_yaml_scalar(f'{city.name_ja}（{city.display_country or attrs.get('iso2', city.country)}）の都市プロファイル。GHS-UCDB 都市圏 {city.ucdb_id} 上で集計した実データ。')}",
        "status: generated",
        f"tags: [city, {_yaml_scalar(city.region)}]",
        f"city_id: {city.city_id}",
        f"name_ja: {_yaml_scalar(city.name_ja)}",
        f"country: {city.display_country or attrs.get('iso2', '')}",
        f"region: {_yaml_scalar(city.region)}",
        f"lat: {city.lat}",
        f"lon: {city.lon}",
        "boundary:",
        "  source: ghsl-ucdb",
        f"  id: {city.ucdb_id}",
        f"  name: {_yaml_scalar(city.name_en)}",
        f"  area_km2: {_round(city.area_km2)}",
        f"generated: {{ by: etl/soulcity_etl/build.py, at: {at} }}",
        "metrics:",
    ]
    body_rows = []
    for m, e in rows:
        key = m["metric_key"]
        if e.get("value") is None:
            lines.append(
                f"  {key}: {{ value: null, quality: missing, source: {m['source']}, year: null, "
                f"reason: {_yaml_scalar(e['reason'])} }}"
            )
            body_rows.append(f"| {m['title']} | 欠損 | — | {e['reason']} |")
        else:
            lines.append(
                f"  {key}: {{ value: {_round(e['value'])}, quality: {e['quality']}, source: {m['source']}, "
                f"year: {_yaml_scalar(e['year'])} }}"
            )
            body_rows.append(f"| {m['title']} | {_round(e['value'])} {m['unit']} | {e['year']} | {e['quality']} |")
    lines += [
        "---",
        "",
        "# 境界",
        "",
        f"GHS-UCDB R2024A の都市圏（urban centre）ID {city.ucdb_id}「{city.name_en}」。面積 {_round(city.area_km2)} km²、"
        f"2025 年人口 {_round(city.pop_2025):,} 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、"
        "周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。",
        "",
        "# 指標",
        "",
        "| 指標 | 値 | 年 | 品質 / 欠損理由 |",
        "| --- | --- | --- | --- |",
        *body_rows,
        "",
        "この文書は `pnpm etl` が生成する。手で編集しない。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    at = now_iso()
    cities = load_cities()
    metrics = adopted_metrics()
    interim = load_interim()
    attrs_path = INTERIM / "city-attributes.json"
    attrs = json.loads(attrs_path.read_text()) if attrs_path.exists() else {}

    table: list[dict[str, Any]] = []
    CITY_DIR.mkdir(parents=True, exist_ok=True)
    for old in CITY_DIR.glob("*.md"):
        if old.name != "index.md":
            old.unlink()
    for c in cities:
        rows = []
        for m in metrics:
            src = interim.get(m["source"], {})
            ek = m.get("etl_key", m["metric_key"])
            v = src.get("values", {}).get(ek, {}).get(c.city_id)
            if v is not None:
                e = v
            else:
                reason = src.get("missing", {}).get(ek, {}).get(c.city_id)
                if reason is None:
                    reason = f"ETL ({m['source']}) がこの都市の値を出力していない"
                e = {"value": None, "reason": reason}
            rows.append((m, e))
            table.append(
                {
                    "city_id": c.city_id,
                    "region": c.region,
                    "metric": m["metric_key"],
                    "source": m["source"],
                    "value": e.get("value"),
                    "quality": e.get("quality", "missing"),
                    "year": e.get("year"),
                    "reason": e.get("reason", ""),
                }
            )
        (CITY_DIR / f"{c.city_id}.md").write_text(city_doc(c, attrs.get(c.city_id, {}), rows, at))

    PROCESSED.mkdir(parents=True, exist_ok=True)
    with (PROCESSED / "city_metrics.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]))
        w.writeheader()
        w.writerows(table)

    # Missing-rate report, overall and by region (fairness monitoring).
    by_metric: dict[str, list[bool]] = defaultdict(list)
    by_region: dict[tuple[str, str], list[bool]] = defaultdict(list)
    for r in table:
        miss = r["value"] is None
        by_metric[r["metric"]].append(miss)
        by_region[(r["metric"], r["region"])].append(miss)
    regions = sorted({c.region for c in cities})
    out = [
        "# 欠損率",
        "",
        f"生成: {at}（`pnpm etl`）。対象 {len(cities)} 都市。",
        "",
        "| 指標 | 出典 | 欠損率 | " + " | ".join(regions) + " |",
        "| --- | --- | --- | " + " | ".join("---" for _ in regions) + " |",
    ]
    for m in metrics:
        k = m["metric_key"]
        xs = by_metric[k]
        cells = []
        for rg in regions:
            ys = by_region[(k, rg)]
            cells.append(f"{sum(ys)}/{len(ys)}")
        out.append(f"| {k} | {m['source']} | {100 * sum(xs) / len(xs):.0f}% | " + " | ".join(cells) + " |")
    (PROCESSED / "coverage.md").write_text("\n".join(out) + "\n")
    n_missing = sum(r["value"] is None for r in table)
    print(f"✓ {len(cities)} cities × {len(metrics)} adopted metrics; missing {n_missing}/{len(table)}")


if __name__ == "__main__":
    main()
