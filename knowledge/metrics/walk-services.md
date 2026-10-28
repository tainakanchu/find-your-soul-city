---
type: Metric
title: 徒歩で生活サービスに届く人口割合
description: 学校・医療などに徒歩圏で届く人口の割合。
status: draft
tags: [metric, itdp-atlas]
metric_key: walk_services
unit: "%"
kind: higher_better
transform: linear
planned_source: itdp-atlas
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

学校・医療などに徒歩圏で届く人口の割合。

# スコアへの入り方

高いほど良い型。都市横断の 10〜90 パーセンタイルで 0〜1 に線形スケールし、ユーザーの重要度で重み付けする。

# 注意点

ITDP の境界定義と GHSL の境界の対応付けが必要。

予定ソース: [itdp-atlas](/sources/itdp-atlas.md)
