---
type: Metric
title: 人口加重密度
description: 住民が平均的に体験する密度。
status: draft
tags: [metric, ghsl-ucdb]
metric_key: density
unit: "人/km²"
kind: ideal
transform: log10
tolerance: 0.25
planned_source: ghsl-ucdb
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

住民が平均的に体験する密度。

# スコアへの入り方

理想値型。ユーザーの理想値との距離をガウス関数で 0〜1 に変換する（変換: `log10`、許容幅 σ=0.25）。

# 注意点

「高いほど良い」とせず、好みの密度との距離で評価する。

予定ソース: [ghsl-ucdb](/sources/ghsl-ucdb.md)
