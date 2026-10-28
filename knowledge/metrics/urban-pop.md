---
type: Metric
title: 都市圏の人口
description: 都市圏（GHS-UCDB の urban centre）全体の人口。
status: adopted
tags: [metric, ghsl-ucdb]
metric_key: urban_pop
adoption: adopted
unit: "人"
kind: ideal
transform: log10
tolerance: 0.3
source: ghsl-ucdb
period: "2025 年（推定）"
geography: "GHS-UCDB 都市圏ポリゴン"
method: "GHS-UCDB の GC_POP_TOT_2025 をそのまま使う"
caveat: "行政市域の人口ではない。東京（3,316 万人）は横浜・さいたま・千葉を含む"
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 定義

都市圏（GHS-UCDB の urban centre）全体の人口。

- 期間: 2025 年（推定）
- 範囲: GHS-UCDB 都市圏ポリゴン
- 算出: GHS-UCDB の GC_POP_TOT_2025 をそのまま使う

# スコアへの入り方

理想値型。ユーザーの理想値との差をガウス関数で 0〜1 にする（変換 `log10`、σ = 0.3）。

# 根拠と検証

対数で比較する（σ = 0.3 は約 2 倍の差）。

# 注意点

行政市域の人口ではない。東京（3,316 万人）は横浜・さいたま・千葉を含む。

出典: [ghsl-ucdb](/sources/ghsl-ucdb.md)
