---
type: Question
title: 空の明るさはどれくらいがいい？
description: sunshine_annual への理想値を尋ねる設問。
status: draft
tags: [question]
question_id: sunshine
order: 5
metric: sunshine_annual
answer_kind: ideal
importance_control: true
options:
  - { label: 曇りの日が多くても落ち着く, value: 1600 }
  - { label: 晴れと曇りが半々くらい, value: 2200 }
  - { label: とにかく晴れの日が多いほうがいい, value: 3000 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [sunshine_annual](/metrics/sunshine-annual.md) の理想値として使う。重要度（気にしない / ふつう / 重要）は別コントロールで 0 / 1 / 2 の重みに変換する。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
