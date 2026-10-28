---
type: Question
title: 家の近所の人の多さは？
description: density_weighted について尋ねる設問（理想値）。
status: draft
tags: [question]
question_id: crowd
order: 6
metric: density_weighted
answer_kind: ideal
importance_control: true
options:
  - { label: "人の気配が少ない、ゆったりした街（5,000 人/km² 前後）", value: 5000 }
  - { label: "ほどよく賑わっている街（11,000 人/km² 前後）", value: 11000 }
  - { label: "いつも人であふれている街（28,000 人/km² 前後）", value: 28000 }
  - { label: "世界有数の過密な街（45,000 人/km² 前後）", value: 45000 }
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [density_weighted](/metrics/) の理想値として使う。重要度（気にしない / ふつう / 重要）は別に尋ね、0 / 1 / 2 の重みにする。

# 選択肢の根拠

選択肢の値は、対象 86 都市の分布（おおむね 15・50・85 パーセンタイル付近）に置き、分布の端の都市（酷暑のドバイ・デリー、過密なムンバイ・ダッカ・カイロ）にも届くよう最上位の選択肢を加えた。どの選択肢にも近い都市が複数あるようにした。括弧内の数値を画面に出し、言葉の印象と実測値のずれを減らす。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
