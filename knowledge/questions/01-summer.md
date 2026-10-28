---
type: Question
title: 真夏の午後、どんな空気の中にいたい？
description: temp_warmest への理想値を尋ねる設問。
status: draft
tags: [question]
question_id: summer
order: 1
metric: temp_warmest
answer_kind: ideal
importance_control: true
options:
  - { label: 上着が一枚ほしいくらいの涼しい夏, value: 21 }
  - { label: 半袖でちょうどいい暖かい夏, value: 25 }
  - { label: 汗ばむくらい暑い夏が好き, value: 29 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [temp_warmest](/metrics/temp-warmest.md) の理想値として使う。重要度（気にしない / ふつう / 重要）は別コントロールで 0 / 1 / 2 の重みに変換する。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
