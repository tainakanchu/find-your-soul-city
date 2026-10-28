---
type: Model Specification
title: 都市適合スコア v0.1
description: 理想値型・高いほど良い型の適合関数と、欠損・品質ラベル・頑健性の扱い。
status: draft
resource: ../../src/scoring/score.ts
tags: [model, scoring]
model_version: 0.1.0
min_coverage: 0.75
generated: { by: claude, at: 2026-10-29T00:00:00Z }
sources:
  - { id: proposal, resource: /references/proposal-v1-0.md, title: 企画書 v1.0 §5 }
---

# 総合スコア

都市 c・ユーザー u・軸 i について、S(u,c) = 100 × Σ w_i f_i / Σ w_i。和は都市 c で欠損していない軸だけで取る。[^proposal]

# 適合関数 f_i

- 理想値型（`kind: ideal`）: 変換後の値 t(v) と理想値 t(p) の差 d に対し f = exp(−½ (d/σ)²)。σ は各 [Metric](/metrics/) の `tolerance`。
- 高いほど良い型（`kind: higher_better`）: 都市横断の 10〜90 パーセンタイル [q10, q90] で f = clamp((v − q10)/(q90 − q10), 0, 1)。パーセンタイルは欠損を除いた都市で計算する。

# 欠損と品質

- 欠損はゼロとして扱わない。その軸を外して重みを再正規化する。
- 重みの充足率（欠損していない軸の重み ÷ 全重み）が `min_coverage` 未満の都市は順位から外し、「データ不足」として別に示す。
- 結果の品質ラベルは、使った軸のうち最も低いもの（placeholder < imputed < estimated < observed）。

# 合う点・合わない点

- 合う点: f ≥ 0.6 の軸を w·f の大きい順に最大 3 つ。
- 合わない点: f < 0.5 の軸を w·(1−f) の大きい順に最大 2 つ。

# 頑健性

重みのある軸それぞれについて重みを ×0.9 / ×1.1 に変えて再計算し、1 位が変わらなかった割合を「安定度」として表示する。これは幸福や移住成功の確率ではない。

# 決定論

同点は `city_id` の昇順で並べる。乱数は使わない。同じ回答・同じデータ版・同じモデル版なら結果は一致する。

[^proposal]: 企画書 v1.0 §5 スコアリング仕様（仮説）
