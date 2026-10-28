---
type: Question
title: 住む街の大きさは？
description: urban_pop への理想値を尋ねる設問。
status: draft
tags: [question]
question_id: size
order: 7
metric: urban_pop
answer_kind: ideal
importance_control: true
options:
  - { label: 全体を把握できる中くらいの都市, value: 1 }
  - { label: なんでも揃う大都市, value: 5 }
  - { label: 終わりが見えない巨大都市圏, value: 20 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [urban_pop](/metrics/urban-pop.md) の理想値として使う。重要度（気にしない / ふつう / 重要）は別コントロールで 0 / 1 / 2 の重みに変換する。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
