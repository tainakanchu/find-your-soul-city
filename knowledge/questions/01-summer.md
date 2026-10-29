---
type: Question
title: 真夏の午後、どんな空気の中にいたい？
description: temp_warmest について尋ねる設問（理想値）。
status: draft
tags: [question]
question_id: summer
order: 1
metric: temp_warmest
answer_kind: ideal
importance_control: true
options:
  - { label: "上着が一枚ほしいくらいの涼しい夏（月平均 18 ℃前後）", value: 18 }
  - { label: "半袖でちょうどいい暖かい夏（24 ℃前後）", value: 24 }
  - { label: "汗ばむくらい暑い夏が好き（29 ℃前後）", value: 29 }
  - { label: "うだるような酷暑でも平気（33 ℃前後）", value: 33 }
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [temp_warmest](/metrics/) の理想値として使う。重要度（気にしない / ふつう / 重要）は別に尋ね、0 / 1 / 2 の重みにする。

# 選択肢の根拠

選択肢の値は、対象 86 都市の分布（おおむね 15・50・85 パーセンタイル付近）に置き、分布の端の都市（酷暑のドバイ・デリー、過密なムンバイ・ダッカ・カイロ）にも届くよう最上位の選択肢を加えた。どの選択肢にも近い都市が複数あるようにした。括弧内の数値を画面に出し、言葉の印象と実測値のずれを減らす。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
