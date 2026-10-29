---
type: Question
title: 日曜日の買い物は？
description: sunday_shops について尋ねる設問（理想値）。
status: draft
tags: [question]
question_id: sunday
order: 18
metric: sunday_shops
answer_kind: ideal
importance_control: true
options:
  - { label: "日曜は店が閉まって静かな街がいい（日曜昼に開いている食料品店 15% 前後）", value: 15 }
  - { label: "半分くらい開いていれば十分（50% 前後）", value: 50 }
  - { label: "日曜もふだんどおり買い物したい（95% 前後）", value: 95 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value`（%）を [日曜の昼に開いている食料品店の割合](/metrics/sunday-shops.md) の理想値として使う。重要度は別に尋ね、0 / 1 / 2 の重みにする。

# 選択肢の根拠

日曜休業の法律がある都市（ミュンヘン 6.5%、ウィーン 7.8%、ベルリン 16%、チューリッヒ 25%、オスロ 36%、アテネ 33%）と、それ以外（中央値 94%）の二つの群に分かれるため、両端と中間に置いた。

# 未検証の点

休日を日曜として数えるため、金曜・土曜が休日の国の様子は表さない。設問文の理解度は P2 の利用者検証で確認する。
