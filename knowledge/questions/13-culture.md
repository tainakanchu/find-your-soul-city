---
type: Question
title: 美術館や劇場、映画館、ライブ会場が身近にたくさんあることは？
description: culture について尋ねる設問（重要度）。
status: draft
tags: [question]
question_id: culture
order: 13
metric: culture
answer_kind: importance
importance_control: false
options:
  - { label: "あまり行かない", value: 0 }
  - { label: "あると嬉しい", value: 1 }
  - { label: "絶対にほしい", value: 2 }
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 回答の変換

選択肢の `value`（0 / 1 / 2）をそのまま [culture](/metrics/culture.md) の重みにする。方向は「多いほど良い」で固定。

# 選択肢の根拠

重要度だけを尋ねる。夜の店（バー・クラブ）は OSM の登録率の地域差が大きいため設問にしない（[nightlife](/metrics/nightlife.md)）。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
