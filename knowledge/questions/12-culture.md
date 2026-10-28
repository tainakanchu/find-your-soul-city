---
type: Question
title: 美術館、劇場、ライブ会場がたくさんあることは？
description: culture_density への重要度を尋ねる設問。
status: draft
tags: [question]
question_id: culture
order: 12
metric: culture_density
answer_kind: importance
importance_control: false
options:
  - { label: たまに行ければ十分, value: 0 }
  - { label: あると嬉しい, value: 1 }
  - { label: 毎週どこかへ行きたい, value: 2 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` をそのまま [culture_density](/metrics/culture-density.md) の重み（0 / 1 / 2）として使う。方向は「高いほど良い」で固定。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
