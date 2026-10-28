---
type: Data Source
title: Copernicus ERA5 reanalysis
description: Copernicus Climate Change Service (ECMWF) が提供。用途：月別気温・降水・日射（日照の代理）
status: draft
resource: https://climate.copernicus.eu/climate-reanalysis
tags: [data-source]
source_id: era5
provider: Copernicus Climate Change Service (ECMWF)
geo_granularity: グリッド
license_status: unverified
generated: { by: claude, at: 2026-10-29T00:00:00Z }
sources:
  - { id: proposal, resource: /references/proposal-v1-0.md, title: 企画書 v1.0 §4 }
---

# 用途

月別気温・降水・日射（日照の代理）

# 注意点

都市境界内のグリッド集計方法を決める。再解析の解像度では都市熱島を十分に表現できない。[^proposal]

# ライセンス

未確認。公開前に提供元の現行ライセンス・帰属表示・派生データ配布条件・API 利用制限を原文で確認し、`license_status` を更新する。

[^proposal]: 企画書 v1.0 §4 データソース戦略
