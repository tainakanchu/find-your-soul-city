---
type: Metric
title: 都市圏人口
description: GHSL urban centre 単位の人口。
status: draft
tags: [metric, ghsl-ucdb]
metric_key: urban_pop
unit: "百万人"
kind: ideal
transform: log10
tolerance: 0.35
planned_source: ghsl-ucdb
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

GHSL urban centre 単位の人口。

# スコアへの入り方

理想値型。ユーザーの理想値との距離をガウス関数で 0〜1 に変換する（変換: `log10`、許容幅 σ=0.35）。

# 注意点

行政市域の人口とは一致しない。

予定ソース: [ghsl-ucdb](/sources/ghsl-ucdb.md)
