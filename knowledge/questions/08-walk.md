---
type: Question
title: 病院や学校が歩いて行ける範囲にあることは？
description: walk_services について尋ねる設問（重要度）。
status: draft
tags: [question]
question_id: walk
order: 8
metric: walk_services
answer_kind: importance
importance_control: false
options:
  - { label: "乗り物で出かければいい", value: 0 }
  - { label: "あると嬉しい", value: 1 }
  - { label: "絶対にほしい", value: 2 }
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 回答の変換

選択肢の `value`（0 / 1 / 2）をそのまま [walk_services](/metrics/) の重みにする。方向は指標の種類（多いほど良い／少ないほど良い）で固定。

# 選択肢の根拠

重要度だけを尋ねる。

# 未検証の点

設問文の理解度と所要時間は P2 の利用者検証で確認する。
