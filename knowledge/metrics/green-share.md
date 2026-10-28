---
type: Metric
title: 緑の被覆率
description: 都市圏内の樹木・草地の被覆率。
status: draft
tags: [metric, esa-worldcover]
metric_key: green_share
unit: "%"
kind: higher_better
transform: linear
planned_source: esa-worldcover
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

都市圏内の樹木・草地の被覆率。

# スコアへの入り方

高いほど良い型。都市横断の 10〜90 パーセンタイルで 0〜1 に線形スケールし、ユーザーの重要度で重み付けする。

# 注意点

公園へのアクセスとは別物。

予定ソース: [esa-worldcover](/sources/esa-worldcover.md)
