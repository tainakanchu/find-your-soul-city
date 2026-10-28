---
type: Metric
title: 最暖月の平均気温
description: 最も暖かい月の月平均気温（平年値）。
status: draft
tags: [metric, era5]
metric_key: temp_warmest
unit: "℃"
kind: ideal
transform: linear
tolerance: 3
planned_source: era5
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

最も暖かい月の月平均気温（平年値）。

# スコアへの入り方

理想値型。ユーザーの理想値との距離をガウス関数で 0〜1 に変換する（変換: `linear`、許容幅 σ=3）。

# 注意点

年平均ではなく夏の体感に近い値として使う。都市熱島は再解析では過小評価される。

予定ソース: [era5](/sources/era5.md)
