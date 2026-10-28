---
type: Question
title: 冬の朝、窓の外はどうなっていてほしい？
description: temp_coldest への理想値を尋ねる設問。
status: draft
tags: [question]
question_id: winter
order: 2
metric: temp_coldest
answer_kind: ideal
importance_control: true
options:
  - { label: 雪や霜が降りる、しっかり寒い冬, value: -3 }
  - { label: コートが要るくらいの冬, value: 5 }
  - { label: 冬でも上着が要らないくらい, value: 16 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [temp_coldest](/metrics/temp-coldest.md) の理想値として使う。重要度（気にしない / ふつう / 重要）は別コントロールで 0 / 1 / 2 の重みに変換する。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
