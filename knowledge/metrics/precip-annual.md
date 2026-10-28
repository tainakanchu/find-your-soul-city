---
type: Metric
title: 年間降水量
description: 年間の降水量合計（平年値）。
status: draft
tags: [metric, era5]
metric_key: precip_annual
unit: "mm"
kind: ideal
transform: log10
tolerance: 0.2
planned_source: era5
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

年間の降水量合計（平年値）。

# スコアへの入り方

理想値型。ユーザーの理想値との距離をガウス関数で 0〜1 に変換する（変換: `log10`、許容幅 σ=0.2）。

# 注意点

量だけで「雨の多さの体感」は決まらない。降水日数の追加を検討する。

予定ソース: [era5](/sources/era5.md)
