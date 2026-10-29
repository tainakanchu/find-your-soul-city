---
type: Question
title: 冬のいちばん寒い時期、外はどうなっていてほしい？
description: temp_coldest について尋ねる設問（理想値）。
status: draft
tags: [question]
question_id: winter
order: 2
metric: temp_coldest
answer_kind: ideal
importance_control: true
options:
  - { label: "雪が積もるような本格的な冬（月平均 −5 ℃前後）", value: -5 }
  - { label: "コートが必要な、はっきりした冬（4 ℃前後）", value: 4 }
  - { label: "上着一枚で過ごせるおだやかな冬（12 ℃前後）", value: 12 }
  - { label: "冬でも半袖でいられるくらい（22 ℃前後）", value: 22 }
  - { label: "一年中、真夏のような暑さ（26 ℃前後）", value: 26 }
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [temp_coldest](/metrics/) の理想値として使う。重要度（気にしない / ふつう / 重要）は別に尋ね、0 / 1 / 2 の重みにする。

# 選択肢の根拠

選択肢の値は、対象 86 都市の分布（おおむね 15・50・85 パーセンタイル付近）に置き、赤道付近の都市（クアラルンプール・シンガポール・ジャカルタ）にも届くよう熱帯側の選択肢を加えた。どの選択肢にも近い都市が複数あるようにした。括弧内の数値を画面に出し、言葉の印象と実測値のずれを減らす。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
