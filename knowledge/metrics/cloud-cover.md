---
type: Metric
title: 年平均雲量
description: 空を雲が覆っている割合の年平均。空の明るさ（晴れやすさ）の代理指標。
status: adopted
tags: [metric, era5]
metric_key: cloud_cover_annual
adoption: adopted
unit: "%"
kind: ideal
transform: linear
tolerance: 10
source: era5
period: "1990–2019 年の平年値"
geography: "最暖月と同じ"
method: "ERA5 の全雲量（0〜1）の 4 時刻・30 年平均を % に換算"
caveat: "日照時間ではない。公開コピーに日照時間・下向き日射のデータがないため雲量で代用した。薄い雲も厚い雲も同じく数える"
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 定義

空を雲が覆っている割合の年平均。空の明るさ（晴れやすさ）の代理指標。

- 期間: 1990–2019 年の平年値
- 範囲: 最暖月と同じ
- 算出: ERA5 の全雲量（0〜1）の 4 時刻・30 年平均を % に換算

# スコアへの入り方

理想値型。ユーザーの理想値との差をガウス関数で 0〜1 にする（変換 `linear`、σ = 10）。

# 根拠と検証

P1 の「年間日照時間」から置き換えた。許容幅 σ = 10 ポイント。

# 注意点

日照時間ではない。公開コピーに日照時間・下向き日射のデータがないため雲量で代用した。薄い雲も厚い雲も同じく数える。

出典: [era5](/sources/era5.md)
