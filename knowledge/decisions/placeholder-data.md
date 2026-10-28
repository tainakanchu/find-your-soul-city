---
type: Decision Record
title: P0 完了まではデモ用の仮値で動かす
description: 実データ取得前は仮値で UI とスコアを検証し、置き換えは指標単位で行う。
status: draft
tags: [decision]
decision_status: accepted
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 判断

実データ（P0）が揃う前に P1 の UI とスコア関数を作るため、[デモ用の仮値](/sources/demo-placeholder.md) を使う。

# ルール

- 仮値は `quality: placeholder` とし、UI に常に明示する。
- 置き換えは指標単位。`source` を実ソースの `source_id` に、`quality` を observed / estimated / imputed に、`year` を観測年に更新する。
- 1 つでも placeholder を使った結果は、品質ラベルが placeholder になる。
