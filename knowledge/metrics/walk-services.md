---
type: Metric
title: 徒歩圏に医療・教育がある人口の割合
description: 徒歩 1 km 以内に医療施設と学校の両方がある住民の割合。
status: adopted
tags: [metric, itdp-atlas]
metric_key: walk_services
adoption: adopted
unit: "%"
kind: higher_better
transform: linear
source: itdp-atlas
period: "2024 年"
geography: "GHS-UCDB 都市圏（Atlas と同一ポリゴン、IoU ≥ 0.9999）"
method: "ITDP が OSM の歩行ネットワーク距離と GHS-POP 人口で算出した People Near Services を使う"
caveat: "OSM の施設登録率に依存する。登録の少ない地域（特にサハラ以南アフリカ・南アジア）では過小評価の可能性がある"
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 定義

徒歩 1 km 以内に医療施設と学校の両方がある住民の割合。

- 期間: 2024 年
- 範囲: GHS-UCDB 都市圏（Atlas と同一ポリゴン、IoU ≥ 0.9999）
- 算出: ITDP が OSM の歩行ネットワーク距離と GHS-POP 人口で算出した People Near Services を使う

# スコアへの入り方

多いほど良い型。対象都市の 10〜90 パーセンタイルで 0〜1 に線形変換し、重要度で重み付けする。

# 根拠と検証

ITDP の値をそのまま使う（×100）。

# 注意点

OSM の施設登録率に依存する。登録の少ない地域（特にサハラ以南アフリカ・南アジア）では過小評価の可能性がある。

出典: [itdp-atlas](/sources/itdp-atlas.md)
