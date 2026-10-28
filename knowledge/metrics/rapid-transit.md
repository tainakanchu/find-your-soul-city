---
type: Metric
title: 高速公共交通の近くに住む人口の割合
description: 地下鉄・LRT・BRT の駅まで 1 km 以内に住む住民の割合。
status: adopted
tags: [metric, itdp-atlas]
metric_key: rapid_transit
adoption: adopted
unit: "%"
kind: higher_better
transform: linear
source: itdp-atlas
period: "2024 年"
geography: "徒歩圏と同じ"
method: "ITDP の People Near Rapid Transport"
caveat: "ITDP の定義では多くの通勤鉄道・近郊鉄道が対象外で、東京などの鉄道都市を過小評価する。駅データが路線長に比べて極端に少ない都市（ロンドン、メルボルン、クアラルンプール、ベンガルール）は欠損扱い"
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 定義

地下鉄・LRT・BRT の駅まで 1 km 以内に住む住民の割合。

- 期間: 2024 年
- 範囲: 徒歩圏と同じ
- 算出: ITDP の People Near Rapid Transport

# スコアへの入り方

多いほど良い型。対象都市の 10〜90 パーセンタイルで 0〜1 に線形変換し、重要度で重み付けする。

# 根拠と検証

駅密度 0.2 駅/路線 km 未満を「駅データ不足」とする検査は `etl/soulcity_etl/itdp.py` の `screen()`。

# 注意点

ITDP の定義では多くの通勤鉄道・近郊鉄道が対象外で、東京などの鉄道都市を過小評価する。駅データが路線長に比べて極端に少ない都市（ロンドン、メルボルン、クアラルンプール、ベンガルール）は欠損扱い。

出典: [itdp-atlas](/sources/itdp-atlas.md)
