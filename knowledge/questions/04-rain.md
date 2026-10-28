---
type: Question
title: 雨とのつきあい方は？
description: precip_annual について尋ねる設問（理想値）。
status: draft
tags: [question]
question_id: rain
order: 4
metric: precip_annual
answer_kind: ideal
importance_control: true
options:
  - { label: "雨はめったに降らないほうがいい（年 400 mm 前後）", value: 400 }
  - { label: "ほどほどに降るのがいい（年 900 mm 前後）", value: 900 }
  - { label: "雨の多い、しっとりした土地が好き（年 1,800 mm 前後）", value: 1800 }
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 回答の変換

選択肢の `value` を [precip_annual](/metrics/) の理想値として使う。重要度（気にしない / ふつう / 重要）は別に尋ね、0 / 1 / 2 の重みにする。

# 選択肢の根拠

選択肢の値は、対象 86 都市の分布（おおむね 15・50・85 パーセンタイル付近）に置き、どの選択肢にも近い都市が複数あるようにした。括弧内の数値を画面に出し、言葉の印象と実測値のずれを減らす。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
