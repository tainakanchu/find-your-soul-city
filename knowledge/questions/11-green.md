---
type: Question
title: 街の中に木や芝生が多いことは？
description: green_share への重要度を尋ねる設問。
status: draft
tags: [question]
question_id: green
order: 11
metric: green_share
answer_kind: importance
importance_control: false
options:
  - { label: 特に気にしない, value: 0 }
  - { label: あると嬉しい, value: 1 }
  - { label: 緑の中で暮らしたい, value: 2 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` をそのまま [green_share](/metrics/green-share.md) の重み（0 / 1 / 2）として使う。方向は「高いほど良い」で固定。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
