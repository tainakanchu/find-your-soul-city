---
type: Metric
title: 年間日照時間
description: 晴れの多さの目安。
status: draft
tags: [metric, era5]
metric_key: sunshine_annual
unit: "h"
kind: ideal
transform: linear
tolerance: 450
planned_source: era5
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

晴れの多さの目安。

# スコアへの入り方

理想値型。ユーザーの理想値との距離をガウス関数で 0〜1 に変換する（変換: `linear`、許容幅 σ=450）。

# 注意点

ERA5 には日照時間そのものがないため、日射量や雲量からの代理指標になる。定義を P0 で確定する。

予定ソース: [era5](/sources/era5.md)
