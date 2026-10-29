---
type: Question
title: 夜 11 時、近所の店はどうなっていてほしい？
description: late_shops について尋ねる設問（理想値）。
status: draft
tags: [question]
question_id: late_shops
order: 16
metric: late_shops
answer_kind: ideal
importance_control: true
options:
  - { label: "夜は店が閉まって静かになる（23 時に開いている食料品店 7% 前後）", value: 7 }
  - { label: "開いている店が少しはある（20% 前後）", value: 20 }
  - { label: "探せば開いている店がすぐ見つかる（40% 前後）", value: 40 }
  - { label: "コンビニがいつでも開いている（70% 前後）", value: 70 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value`（%）を [深夜 23 時に開いている食料品店の割合](/metrics/late-shops.md) の理想値として使う。重要度は別に尋ね、0 / 1 / 2 の重みにする。

# 選択肢の根拠

対象都市の 15・50・85 パーセンタイル（7.7・20・59%）と、コンビニのある都市（71〜80%）に置いた。夜の静けさを好む回答もできるよう、低い側の選択肢も同じ重さで扱う。

# 未検証の点

OSM のタグから推定した割合で、画面の数値は目安。設問文の理解度は P2 の利用者検証で確認する。
