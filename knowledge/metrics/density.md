---
type: Metric
title: 人口加重密度
description: 住民が平均的に体験する人口密度。
status: adopted
tags: [metric, ghsl-pop]
metric_key: density_weighted
adoption: adopted
unit: "人/km²"
kind: ideal
transform: log10
tolerance: 0.2
source: ghsl-pop
period: "2025 年（推定）"
geography: "都市圏ポリゴン内の GHS-POP 1 km セル"
method: "Σ(人口ᵢ × 密度ᵢ) / Σ人口ᵢ。密度ᵢ はセル人口 / セル面積"
caveat: "2025 年の人口は UN 推計に合わせた推定値。1 km 単位なので建物の高さによる密集感は表さない"
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 定義

住民が平均的に体験する人口密度。

- 期間: 2025 年（推定）
- 範囲: 都市圏ポリゴン内の GHS-POP 1 km セル
- 算出: Σ(人口ᵢ × 密度ᵢ) / Σ人口ᵢ。密度ᵢ はセル人口 / セル面積

# スコアへの入り方

理想値型。ユーザーの理想値との差をガウス関数で 0〜1 にする（変換 `log10`、σ = 0.2）。

# 根拠と検証

単純な人口 ÷ 面積はポリゴンが郊外の農地をどこまで含むかで大きく変わる。人口加重密度はその影響が小さく、「人混みの中にいる感覚」に近い。単純密度との順位相関は 0.93（ダッカは 45 位 → 3 位）。

# 注意点

2025 年の人口は UN 推計に合わせた推定値。1 km 単位なので建物の高さによる密集感は表さない。

出典: [ghsl-pop](/sources/ghsl-pop.md)
