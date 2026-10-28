---
type: Decision Record
title: 仮値を廃止し、本番ビルドで検出したら失敗させる
description: P1 のデモ用仮値をすべて実データに置き換え、仮値の混入をビルドで止める。
status: accepted
tags: [decision, data-quality]
decision_status: accepted
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 判断

P1 の 30 都市 × 11 指標の仮値（`demo-placeholder`）を削除し、ETL で取得した実データだけを使う。

# 仕組み

- 指標値の `quality` は observed / estimated / imputed / missing のみ。`placeholder` は `knowledge:build` が拒否する。
- `src/model/guard.ts` の `findPlaceholders` を、`knowledge:build`、Vite 本番ビルド（`placeholder-guard` プラグイン）、テストの 3 か所で実行する。
- 値のない指標は 0 や推定で埋めず `value: null, quality: missing` とし、理由（`reason`）を必須にする。
