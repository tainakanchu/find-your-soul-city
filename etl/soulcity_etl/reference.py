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


def _column(m: dict) -> tuple[str, dict[str, float]]:
    """(metric_key, {city_id: value}) from the metric's reference CSV."""
    col = m.get("reference_column", m.get("etl_key", m["metric_key"]))
    path = REFERENCE / f"{m['source']}.csv"
    if not path.exists():
        raise SystemExit(f"{m['metric_key']}: {path} missing — run the {m['source']} module with --reference")
    with path.open() as f:
        rows = list(csv.DictReader(f))
    if col not in rows[0]:
        raise SystemExit(f"{m['metric_key']}: column {col} not in {path.name}")
    return m["metric_key"], {r["city_id"]: float(r[col]) for r in rows if r[col] not in ("", "nan", "NaN", "None")}


def _ranks(xs: list[float]) -> list[float]:
    """Average ranks (ties share the mean rank)."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2
        i = j + 1
    return out


def spearman(a: dict[str, float], b: dict[str, float]) -> tuple[float, int]:
    ids = sorted(set(a) & set(b))
    ra, rb = _ranks([a[i] for i in ids]), _ranks([b[i] for i in ids])
    n = len(ids)
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb, strict=True))
    va = sum((x - ma) ** 2 for x in ra)
    vb = sum((y - mb) ** 2 for y in rb)
    return cov / math.sqrt(va * vb), n


def correlation_lines(metrics: list[dict]) -> list[str]:
    """Spearman correlation between every pair of adopted metrics over the reference set (pairwise complete)."""
    cols = dict(_column(m) for m in metrics)
    keys = sorted(cols)
    lines = []
    for a in keys:
        cells = []
        for b in keys:
            if a == b:
                continue
            r, n = spearman(cols[a], cols[b])
            if n < 0.5 * len(reference_centres()):
                raise SystemExit(f"correlation {a}/{b}: only {n} common reference cities")
            cells.append(f"{b}: {round(r, 3)}")
        lines.append(f"  {a}: {{ {', '.join(cells)} }}")
    return lines


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
        "# Spearman rank correlation between adopted metrics over the same reference set (pairwise complete).",
        "# Used to share weight between strongly correlated answers (knowledge/model/scoring.md).",
        "correlations:",
        *correlation_lines(adopted_metrics()),
        f"generated: {{ by: etl/soulcity_etl/reference.py, at: {now_iso()} }}",
        "---",
        "",
        "# 使い方",
        "",
        "方向型の指標は、都市の値がこの分布の何パーセンタイルにあたるか（分位点の間は線形補間、同値は中央の順位）を適合度 0〜1 とする。"
        "診断の対象都市ではなく世界の大都市圏全体を基準にするので、対象都市を増減してもほかの都市のスコアは変わらない。",
        "",
        "`correlations` は同じ基準集合での指標どうしの順位相関（Spearman）。相関の強い条件を両方重視したときに重みを分け合うために使う。",
        "",
        "この文書は `pnpm etl` が生成する。手で編集しない。",
        "",
    ])
    (KNOWLEDGE / "model" / "reference-distribution.md").write_text(doc)
    print(f"✓ reference distributions for {len(lines)} directional metrics")


if __name__ == "__main__":
    main()
