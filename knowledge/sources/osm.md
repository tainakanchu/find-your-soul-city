---
type: Data Source
title: OpenStreetMap (via Geofabrik)
description: OpenStreetMap contributors が提供。用途：文化施設 POI 密度
status: draft
resource: https://www.openstreetmap.org/copyright
tags: [data-source]
source_id: osm
provider: OpenStreetMap contributors
geo_granularity: 施設・道路
license_status: unverified
generated: { by: claude, at: 2026-10-29T00:00:00Z }
sources:
  - { id: proposal, resource: /references/proposal-v1-0.md, title: 企画書 v1.0 §4 }
---

# 用途

文化施設 POI 密度

# 注意点

地域ごとに登録率が違う。POI 数を文化の豊かさと同一視しない。派生 DB の配布は ODbL の条件を受ける。[^proposal]

# ライセンス

未確認。公開前に提供元の現行ライセンス・帰属表示・派生データ配布条件・API 利用制限を原文で確認し、`license_status` を更新する。

[^proposal]: 企画書 v1.0 §4 データソース戦略
