---
type: Question
title: 一年の移り変わりはどれくらいほしい？
description: seasonal_range への理想値を尋ねる設問。
status: draft
tags: [question]
question_id: seasons
order: 3
metric: seasonal_range
answer_kind: ideal
importance_control: true
options:
  - { label: 一年中ほぼ同じ気候が楽, value: 4 }
  - { label: 季節の変化がほどほどにある, value: 14 }
  - { label: 夏と冬がはっきり違うのがいい, value: 24 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [seasonal_range](/metrics/seasonal-range.md) の理想値として使う。重要度（気にしない / ふつう / 重要）は別コントロールで 0 / 1 / 2 の重みに変換する。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
