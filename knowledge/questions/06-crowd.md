---
type: Question
title: 人混みの中にいるとき、どう感じる？
description: density への理想値を尋ねる設問。
status: draft
tags: [question]
question_id: crowd
order: 6
metric: density
answer_kind: ideal
importance_control: true
options:
  - { label: 人の気配が少ない静かな街がいい, value: 2500 }
  - { label: ほどよく賑わっているのがいい, value: 7000 }
  - { label: 人波に紛れているほうが落ち着く, value: 18000 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [density](/metrics/density.md) の理想値として使う。重要度（気にしない / ふつう / 重要）は別コントロールで 0 / 1 / 2 の重みに変換する。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
