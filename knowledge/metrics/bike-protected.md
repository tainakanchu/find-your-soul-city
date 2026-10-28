---
type: Metric
title: 保護自転車道の近くに住む人口割合
description: 保護された自転車道から一定距離内に住む人口の割合。
status: draft
tags: [metric, itdp-atlas]
metric_key: bike_protected
unit: "%"
kind: higher_better
transform: linear
planned_source: itdp-atlas
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

保護された自転車道から一定距離内に住む人口の割合。

# スコアへの入り方

高いほど良い型。都市横断の 10〜90 パーセンタイルで 0〜1 に線形スケールし、ユーザーの重要度で重み付けする。

# 注意点

OSM 由来の道路データに依存し、地域の登録率差を受ける。

予定ソース: [itdp-atlas](/sources/itdp-atlas.md)
