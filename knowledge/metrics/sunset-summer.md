---
type: Metric
title: 夏至の日の入り時刻
description: 夏至の日（南半球は 12 月 21 日）に日が沈む時計の時刻（夏時間を含む）。夏の夜が何時まで明るいか。
status: adopted
tags: [metric, daylight]
metric_key: sunset_summer
etl_key: sunset_summer_local
reference_column: sunset_summer_local
adoption: adopted
unit: "時刻"
kind: ideal
transform: linear
tolerance: 0.75
source: daylight
period: "2025 年の暦（夏至の日）"
geography: "都市圏の代表点（GHS-UCDB ポリゴン内の点）"
method: "astral（NOAA の式）で太陽の上端が海面の地平線に沈む時刻を求め、IANA tzdata のその日の時計時刻（夏時間を含む）で表す。0 時を過ぎる場合は 24 + x"
caveat: "地形・標高・建物による日没の早まりは含まない。時計の時刻は国の時間帯・夏時間の制度で決まり、天文的な昼の長さと一致しない（スペインは経度の割に遅い）"
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

夏至の日に日が沈む、その都市の時計の時刻。「夏の夜、何時ごろまで明るいか」を表す。緯度（昼の長さ）と、時間帯・夏時間の制度（時計と太陽のずれ）の両方で決まる。

# スコアへの入り方

理想値型。ユーザーの理想の時刻との差（時間）をガウス関数で 0〜1 にする（σ = 0.75 時間）。

# 根拠と検証

対象 130 都市の 15・50・85 パーセンタイルは 18.5・19.5・21.1 時（18:31・19:31・21:03）。熱帯は 18 時台、北欧は 22 時以降（レイキャビク 0:02）。σ = 0.75 時間は「夕方の明るさの体感がはっきり変わる差」として置いた設計値で、選択肢の間隔（1〜1.5 時間）の半分程度。

外部データを使わない計算で、欠損はない。品質は `estimated`（地形を含まない計算値）。

冬至の日の入りと時計と太陽のずれは採用しない（[冬の日の入り](/metrics/sunset-winter.md)、[時計と太陽のずれ](/metrics/solar-noon-offset.md)）。

# 注意点

地形・標高・建物による日没の早まりは含まない。

出典: [daylight](/sources/daylight.md)
