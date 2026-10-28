---
type: Metric
title: 最寒月の平均気温
description: 一年で最も寒い月の月平均気温。
status: adopted
tags: [metric, era5]
metric_key: temp_coldest
adoption: adopted
unit: "℃"
kind: ideal
transform: linear
tolerance: 4
source: era5
period: "1990–2019 年の平年値"
geography: "最暖月と同じ"
method: "最暖月と同じ手順で、月平均の最小値"
caveat: "最暖月と同じ。冬の放射冷却や谷の逆転層は 0.25° グリッドでは再現しにくい"
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 定義

一年で最も寒い月の月平均気温。

- 期間: 1990–2019 年の平年値
- 範囲: 最暖月と同じ
- 算出: 最暖月と同じ手順で、月平均の最小値

# スコアへの入り方

理想値型。ユーザーの理想値との差をガウス関数で 0〜1 にする（変換 `linear`、σ = 4）。

# 根拠と検証

許容幅 σ = 4 ℃。都市間の幅（−22〜26 ℃）が夏より広いため、夏より広く取った。

# 注意点

最暖月と同じ。冬の放射冷却や谷の逆転層は 0.25° グリッドでは再現しにくい。

出典: [era5](/sources/era5.md)
