---
type: Question
title: ふだんの空はどうあってほしい？
description: cloud_cover_annual について尋ねる設問（理想値）。
status: draft
tags: [question]
question_id: sky
order: 5
metric: cloud_cover_annual
answer_kind: ideal
importance_control: true
options:
  - { label: "たいてい晴れて青空が見える（雲量 35% 前後）", value: 35 }
  - { label: "晴れの日も曇りの日もある（雲量 55% 前後）", value: 55 }
  - { label: "雲の多いやわらかい空が落ち着く（雲量 72% 前後）", value: 72 }
  - { label: "ほとんど毎日、雲が空を覆っているくらいでいい（雲量 82% 前後）", value: 82 }
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [cloud_cover_annual](/metrics/) の理想値として使う。重要度（気にしない / ふつう / 重要）は別に尋ね、0 / 1 / 2 の重みにする。

# 選択肢の根拠

選択肢の値は、対象 86 都市の分布（おおむね 15・50・85 パーセンタイル付近）に置き、赤道付近の都市（クアラルンプール・シンガポール・ジャカルタ）にも届くよう熱帯側の選択肢を加えた。どの選択肢にも近い都市が複数あるようにした。括弧内の数値を画面に出し、言葉の印象と実測値のずれを減らす。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
