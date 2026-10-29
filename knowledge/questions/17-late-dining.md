---
type: Question
title: 夜 10 時すぎの夕食は？
description: late_dining について尋ねる設問（理想値）。
status: draft
tags: [question]
question_id: late_dining
order: 17
metric: late_dining
answer_kind: ideal
importance_control: true
options:
  - { label: "夕食は早めに済ませる街がいい（23 時に開いている飲食店 8% 前後）", value: 8 }
  - { label: "遅めでも何軒かは開いている（20% 前後）", value: 20 }
  - { label: "夜遅い夕食がふつう（40% 前後）", value: 40 }
  - { label: "真夜中まで店がにぎわっている（65% 前後）", value: 65 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value`（%）を [深夜 23 時に開いている飲食店の割合](/metrics/late-dining.md) の理想値として使う。重要度は別に尋ね、0 / 1 / 2 の重みにする。

# 選択肢の根拠

対象都市の 15・50・85 パーセンタイル（9.3・19・42%）と、夕食の遅い都市（マドリード 57%、アテネ 66%）に置いた。

# 未検証の点

OSM のタグから推定した割合で、画面の数値は目安。設問文の理解度は P2 の利用者検証で確認する。
