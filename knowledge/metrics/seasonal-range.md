---
type: Metric
title: 季節の振れ幅
description: 最暖月と最寒月の平均気温の差。
status: draft
tags: [metric, era5]
metric_key: seasonal_range
unit: "℃"
kind: ideal
transform: linear
tolerance: 5
derived_from: [temp_warmest, temp_coldest]
planned_source: era5
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

最暖月と最寒月の平均気温の差。

# スコアへの入り方

理想値型。ユーザーの理想値との距離をガウス関数で 0〜1 に変換する（変換: `linear`、許容幅 σ=5）。

# 注意点

[最暖月](/metrics/temp-warmest.md) と [最寒月](/metrics/temp-coldest.md) から派生する。両者と相関するため、重みの二重計上に注意する。

予定ソース: [era5](/sources/era5.md)
