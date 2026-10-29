---
type: Question
title: 洪水や台風などの自然災害が少ないことは？
description: flood と typhoon をまとめて尋ねる設問（重要度）。
status: draft
tags: [question]
question_id: hazard
order: 14
metrics: [flood, typhoon]
answer_kind: importance
importance_control: false
options:
  - { label: "気にしない", value: 0 }
  - { label: "少ないほうが嬉しい", value: 1 }
  - { label: "いちばん大事", value: 2 }
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 回答の変換

選択肢の `value`（0 / 1 / 2）を [洪水](/metrics/flood.md) と [熱帯低気圧](/metrics/typhoon.md) に等分して重みにする。十分な水準（τ）は回答の値（1 / 2）で決める。

# 設計の判断

洪水と熱帯低気圧はほぼ独立（順位相関 0.24）なので、どちらか一方では代表できない。1 つずつ設問にすると数が増えるため、1 問で尋ねて重みを等分する。この合成は公的な指標ではなく、本プロジェクトの設計。地震は元データのライセンスのため入れていない（[地震](/metrics/quake.md)）。

設問文は「安全な街」ではなく「自然災害が少ない街」とする。防護（堤防など）は考慮していないため。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
