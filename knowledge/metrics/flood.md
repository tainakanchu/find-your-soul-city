---
type: Metric
title: 洪水の想定範囲に住む人口の割合
description: 100 年に 1 度の河川洪水または沿岸洪水の想定範囲に住む人口の割合。
status: adopted
tags: [metric, ghsl-hazard]
metric_key: flood
etl_key: flood_pop_share_100y_pct
reference_column: flood_pop_share_100y_pct
adoption: adopted
unit: "%"
kind: lower_better
transform: linear
source: ghsl-hazard
period: "2025 年の人口、100 年に 1 度の想定"
geography: "GHS-UCDB 都市圏（UCDB が算出）"
method: "河川洪水（EX_100_SHP）と沿岸洪水（EX_CF1_SHP）の割合の大きいほう。両方の範囲の重なりは分からないため、合計ではなく大きいほう（二重計上しない下限）とした"
caveat: "堤防などの防護は考慮しない浸水想定。災害の起こりやすさや被害の大きさではない"
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

100 年に 1 度の規模の河川洪水または沿岸洪水で浸水が想定される範囲に住む人の割合。

# スコアへの入り方

少ないほど良い型。設問「[自然災害が少ない街](/questions/14-hazard.md)」で [熱帯低気圧](/metrics/typhoon.md) と重みを等分する。

# 根拠と検証

上海 82%、バンコク 75%、ダッカ 57%、コルカタ 29%、マドリード 0.3%。地震・熱帯低気圧との順位相関は −0.05 / 0.24 でほぼ独立。所得グループ間の差は小さく、豊かさの代理ではない。詳細は `etl/notes/ghsl-hazard.md`。

# 注意点

堤防などの防護は考慮しない浸水想定。災害の起こりやすさや被害の大きさではない。

出典: [ghsl-hazard](/sources/ghsl-hazard.md)
