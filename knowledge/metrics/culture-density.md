---
type: Metric
title: 文化施設の密度
description: 美術館・劇場・ライブ会場などの POI 数（人口 10 万人あたり）。
status: draft
tags: [metric, osm]
metric_key: culture_density
unit: "件/10万人"
kind: higher_better
transform: linear
planned_source: osm
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

美術館・劇場・ライブ会場などの POI 数（人口 10 万人あたり）。

# スコアへの入り方

高いほど良い型。都市横断の 10〜90 パーセンタイルで 0〜1 に線形スケールし、ユーザーの重要度で重み付けする。

# 注意点

OSM の登録率は地域差が大きい。都市別カバレッジを検証するまで低品質指標として扱う。

予定ソース: [osm](/sources/osm.md)
