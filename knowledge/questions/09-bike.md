---
type: Question
title: 車道から守られた自転車道で移動できることは？
description: bike_protected への重要度を尋ねる設問。
status: draft
tags: [question]
question_id: bike
order: 9
metric: bike_protected
answer_kind: importance
importance_control: false
options:
  - { label: 自転車には乗らない, value: 0 }
  - { label: あると嬉しい, value: 1 }
  - { label: 絶対にほしい, value: 2 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` をそのまま [bike_protected](/metrics/bike-protected.md) の重み（0 / 1 / 2）として使う。方向は「高いほど良い」で固定。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
