---
type: Question
title: 夏の夜は何時ごろまで明るいのがいい？
description: sunset_summer について尋ねる設問（理想値）。
status: draft
tags: [question]
question_id: sunset
order: 15
metric: sunset_summer
answer_kind: ideal
importance_control: true
options:
  - { label: "夏でも早めに暗くなる（夏至の日の入り 18:30 ごろ）", value: 18.5 }
  - { label: "夕食のころには暗い（19:30 ごろ）", value: 19.5 }
  - { label: "夜 9 時まで明るい長い夕方（21:00 ごろ）", value: 21 }
  - { label: "白夜に近く、夜遅くまで明るい（22:30 ごろ）", value: 22.5 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value`（時、10 進）を [夏至の日の入り時刻](/metrics/sunset-summer.md) の理想値として使う。重要度（気にしない / ふつう / 重要）は別に尋ね、0 / 1 / 2 の重みにする。

# 選択肢の根拠

対象 130 都市の 15・50・85 パーセンタイル（18.5・19.5・21.1 時）に置き、北欧（ストックホルム・ヘルシンキ・オスロ・レイキャビク）に届くよう 22:30 を加えた。朝型・夜型の好みのうち「夜の明るさ」を尋ねる。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
