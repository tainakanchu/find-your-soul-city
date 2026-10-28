---
type: Question
title: 鉄道や BRT ですぐ移動できることは？
description: rapid_transit への重要度を尋ねる設問。
status: draft
tags: [question]
question_id: transit
order: 10
metric: rapid_transit
answer_kind: importance
importance_control: false
options:
  - { label: 車や徒歩で足りる, value: 0 }
  - { label: あると嬉しい, value: 1 }
  - { label: 絶対にほしい, value: 2 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` をそのまま [rapid_transit](/metrics/rapid-transit.md) の重み（0 / 1 / 2）として使う。方向は「高いほど良い」で固定。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
