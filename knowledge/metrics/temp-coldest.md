---
type: Metric
title: 最寒月の平均気温
description: 最も寒い月の月平均気温（平年値）。
status: draft
tags: [metric, era5]
metric_key: temp_coldest
unit: "℃"
kind: ideal
transform: linear
tolerance: 4
planned_source: era5
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

最も寒い月の月平均気温（平年値）。

# スコアへの入り方

理想値型。ユーザーの理想値との距離をガウス関数で 0〜1 に変換する（変換: `linear`、許容幅 σ=4）。

# 注意点

寒冷日数（日最低気温 0℃未満の日数など）への置き換えを P0 で検討する。

予定ソース: [era5](/sources/era5.md)
