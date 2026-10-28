---
type: Data Source
title: ESA WorldCover
description: European Space Agency が提供。用途：都市圏内の樹木・草地の被覆率
status: draft
resource: https://esa-worldcover.org/en/data-access
tags: [data-source]
source_id: esa-worldcover
provider: European Space Agency
geo_granularity: 10m 土地被覆
license_status: unverified
generated: { by: claude, at: 2026-10-29T00:00:00Z }
sources:
  - { id: proposal, resource: /references/proposal-v1-0.md, title: 企画書 v1.0 §4 }
---

# 用途

都市圏内の樹木・草地の被覆率

# 注意点

版（2020/2021）で分類器が異なる。都市圏境界と組み合わせて集計する。[^proposal]

# ライセンス

未確認。公開前に提供元の現行ライセンス・帰属表示・派生データ配布条件・API 利用制限を原文で確認し、`license_status` を更新する。

[^proposal]: 企画書 v1.0 §4 データソース戦略
