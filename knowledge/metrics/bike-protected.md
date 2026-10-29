---
type: Metric
title: 保護自転車道の近くに住む人口の割合
description: 車道から分離された自転車道まで 300 m 以内に住む住民の割合。
status: adopted
tags: [metric, itdp-atlas]
metric_key: bike_protected
adoption: adopted
unit: "%"
kind: higher_better
transform: linear
source: itdp-atlas
period: "2024 年"
geography: "GHS-UCDB 都市圏（Atlas と同一ポリゴン、IoU ≥ 0.9999）"
method: "ITDP の People Near Protected Bikeways"
caveat: "OSM の自転車道の登録状況に依存する。0% の都市が 1 割ある"
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 定義

車道から分離された自転車道まで 300 m 以内に住む住民の割合。

- 期間: 2024 年
- 範囲: GHS-UCDB 都市圏（Atlas と同一ポリゴン、IoU ≥ 0.9999）
- 算出: ITDP の People Near Protected Bikeways

# スコアへの入り方

多いほど良い型。対象都市の 10〜90 パーセンタイルで 0〜1 に線形変換し、重要度で重み付けする。

# 根拠と検証

ITDP の値をそのまま使う（×100）。

# 注意点

OSM の自転車道の登録状況に依存する。0% の都市が 1 割ある。

出典: [itdp-atlas](/sources/itdp-atlas.md)
