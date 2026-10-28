---
type: Data Source
title: デモ用の仮値
description: 実データ取得前に UI とスコアリングを動かすための概算値。実測ではない。
status: draft
tags: [data-source, placeholder]
source_id: demo-placeholder
provider: Claude による一般知識ベースの概算
geo_granularity: 未定義（都市境界と未対応付け）
license_status: not-applicable
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 位置づけ

P0（データ実証）完了前に、診断フロー・スコア関数・根拠画面を検証するための値。
すべての都市指標は `quality: placeholder` として記録し、UI でも常に明示する。

# やってはいけないこと

- この値を根拠として結果を一般公開する
- この値と実データを同じ品質ラベルで混在させる

実データに置き換えた指標から、`source` と `quality` を更新する（[置き換え方針](/decisions/placeholder-data.md)）。
