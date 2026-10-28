"""Reference distributions for directional metrics (kind higher_better / lower_better).

A directional metric is scored by the city's percentile within ALL GHS-UCDB urban centres with
>= 1M inhabitants (524), not within the target cities, so adding or removing target cities does
not move anyone's score. Quantiles are written to knowledge/model/reference-distribution.md.
"""

from __future__ import annotations

import csv
import math

from .build import KNOWLEDGE, adopted_metrics
from .cities import REFERENCE_MIN_POP, reference_centres
from .common import REFERENCE, now_iso

LEVELS = [i / 20 for i in range(21)]


def quantile(sorted_xs: list[float], q: float) -> float:
    pos = (len(sorted_xs) - 1) * q
    i = math.floor(pos)
    j = min(i + 1, len(sorted_xs) - 1)
    return sorted_xs[i] + (sorted_xs[j] - sorted_xs[i]) * (pos - i)


def main() -> None:
    n_ref = len(reference_centres())
    lines = []
    for m in adopted_metrics():
        if m["kind"] == "ideal":
            continue
        col = m.get("reference_column", m.get("etl_key", m["metric_key"]))
        path = REFERENCE / f"{m['source']}.csv"
        if not path.exists():
            raise SystemExit(f"{m['metric_key']}: {path} missing — run the {m['source']} module with --reference")
        with path.open() as f:
            rows = list(csv.DictReader(f))
        if col not in rows[0]:
            raise SystemExit(f"{m['metric_key']}: column {col} not in {path.name}")
        xs = sorted(float(r[col]) for r in rows if r[col] not in ("", "nan", "NaN", "None"))
        if len(xs) < 0.8 * n_ref:
            raise SystemExit(f"{m['metric_key']}: only {len(xs)}/{n_ref} reference values")
        qs = [round(quantile(xs, q), 4) for q in LEVELS]
        lines.append(f"  {m['metric_key']}: {{ source: {m['source']}, n: {len(xs)}, quantiles: {qs} }}")
    doc = "\n".join([
        "---",
        "type: Reference Distribution",
        "title: 方向型指標の基準分布",
        f"description: 人口 {REFERENCE_MIN_POP:,} 人以上の全都市圏（{n_ref}）での分位点。多いほど良い／少ないほど良い型の指標の 0〜1 変換に使う。",
        "status: generated",
        "tags: [model, reference]",
        f"reference_set: \"GHS-UCDB R2024A urban centres with GC_POP_TOT_2025 >= {REFERENCE_MIN_POP} ({n_ref})\"",
        f"levels: {LEVELS}",
        "metrics:",
        *lines,
        f"generated: {{ by: etl/soulcity_etl/reference.py, at: {now_iso()} }}",
        "---",
        "",
        "# 使い方",
        "",
        "方向型の指標は、都市の値がこの分布の何パーセンタイルにあたるか（分位点の間は線形補間、同値は中央の順位）を適合度 0〜1 とする。"
        "診断の対象都市ではなく世界の大都市圏全体を基準にするので、対象都市を増減してもほかの都市のスコアは変わらない。",
        "",
        "この文書は `pnpm etl` が生成する。手で編集しない。",
        "",
    ])
    (KNOWLEDGE / "model" / "reference-distribution.md").write_text(doc)
    print(f"✓ reference distributions for {len(lines)} directional metrics")


if __name__ == "__main__":
    main()
