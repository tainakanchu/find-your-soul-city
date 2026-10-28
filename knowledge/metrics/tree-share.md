---
type: Metric
title: 樹木被覆率
description: 都市圏の陸地のうち樹木に覆われた割合。
status: adopted
tags: [metric, esa-worldcover]
metric_key: tree_share
adoption: adopted
unit: "%"
kind: higher_better
transform: linear
source: esa-worldcover
period: "2021 年"
geography: "都市圏ポリゴン内の 10 m 画素（緯度で面積を補正、水域を分母から除く）"
method: "WorldCover の class 10（tree cover）の面積 / 陸地面積"
caveat: "都市圏が郊外の森林をどれだけ含むかの影響を受ける。草地・公園の芝生は含まない"
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 定義

都市圏の陸地のうち樹木に覆われた割合。

- 期間: 2021 年
- 範囲: 都市圏ポリゴン内の 10 m 画素（緯度で面積を補正、水域を分母から除く）
- 算出: WorldCover の class 10（tree cover）の面積 / 陸地面積

# スコアへの入り方

多いほど良い型。対象都市の 10〜90 パーセンタイルで 0〜1 に線形変換し、重要度で重み付けする。

# 根拠と検証

UCDB の植生指標（Landsat NDVI）との順位相関 0.85。草地を含む緑被率は乾燥地の低木・草原も数えてしまうため、設問「木の多い街」には樹木被覆率を使う。

# 注意点

都市圏が郊外の森林をどれだけ含むかの影響を受ける。草地・公園の芝生は含まない。

出典: [esa-worldcover](/sources/esa-worldcover.md)
