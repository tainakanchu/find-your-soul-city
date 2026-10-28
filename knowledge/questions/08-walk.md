---
type: Question
title: 学校や病院、日々の用事が歩ける範囲にあることは？
description: walk_services への重要度を尋ねる設問。
status: draft
tags: [question]
question_id: walk
order: 8
metric: walk_services
answer_kind: importance
importance_control: false
options:
  - { label: 乗り物で出かければいい, value: 0 }
  - { label: あると嬉しい, value: 1 }
  - { label: 絶対にほしい, value: 2 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` をそのまま [walk_services](/metrics/walk-services.md) の重み（0 / 1 / 2）として使う。方向は「高いほど良い」で固定。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
