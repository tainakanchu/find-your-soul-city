---
type: Data Source
title: GHS Urban Centre Database R2024A
description: European Commission JRC が提供。用途：都市規模・人口加重密度・市街地環境
status: draft
resource: https://human-settlement.emergency.copernicus.eu/ucdb2024Overview.php
tags: [data-source]
source_id: ghsl-ucdb
provider: European Commission JRC
geo_granularity: 都市圏
license_status: unverified
generated: { by: claude, at: 2026-10-29T00:00:00Z }
sources:
  - { id: proposal, resource: /references/proposal-v1-0.md, title: 企画書 v1.0 §4 }
---

# 用途

都市規模・人口加重密度・市街地環境

# 注意点

カラム定義・観測年・欠損を確認する。都市境界は urban centre 定義であり行政市域とは一致しない。[^proposal]

# ライセンス

未確認。公開前に提供元の現行ライセンス・帰属表示・派生データ配布条件・API 利用制限を原文で確認し、`license_status` を更新する。

[^proposal]: 企画書 v1.0 §4 データソース戦略
