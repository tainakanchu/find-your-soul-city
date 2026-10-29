---
type: Metric
title: 深夜 23 時に開いている食料品店の割合
description: スーパー・コンビニのうち、平日 23 時に開いている店の割合（OSM の営業時間タグから推定）。
status: adopted
tags: [metric, osm-hours]
metric_key: late_shops
etl_key: grocery_late_open_share
reference_column: groceries_late23_post
reference_partial: "OSM の営業時間タグが十分にある都市だけ（基準集合 524 のうち約 230）"
adoption: adopted
unit: "%"
kind: ideal
transform: linear
tolerance: 12
source: osm-hours
period: "2026 年（OSM planet 2026-09-21、基準週の水曜 23:00）"
geography: "重心が都市圏ポリゴン内にある shop=supermarket|convenience"
method: "解析できる opening_hours タグを持つ店のうち水曜 23:00 に開いている割合を、チェーン（brand タグ）と非チェーンに分けて求め、全店に占めるチェーンの割合で重み付けし直す"
caveat: "タグ付きの店は無作為標本ではない。タグが少ない 30 都市（主にアフリカ・南アジア・中東）は欠損"
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

スーパーとコンビニのうち、平日の 23 時に開いている店の割合。「夜遅くでも買い物ができるか」を表す。

# スコアへの入り方

理想値型。ユーザーの理想の割合との差をガウス関数で 0〜1 にする（σ = 12 ポイント）。夜の静けさを好む人もいるため、多いほど良い型にはしない。

# 根拠と検証

対象都市の 15・50・85 パーセンタイルは 7.7・20・59%。コンビニのある都市が高く（東京 79%、大阪 80%、台北 78%、ソウル 71%）、欧州は中央値 12%。チェーンの補正で値が動く幅は中央値 3 ポイント未満。σ = 12 は選択肢の間隔（13〜30 ポイント）に合わせた設計値。タグの標本誤差は数ポイントあるため、これより細かい差は区別しない。

24 時間営業の割合は順位相関 0.91 でほぼ同じ内容のため採用しない（[24 時間営業](/metrics/shops-24h.md)）。

# 注意点

タグ付きの店は無作為標本ではない（チェーンほどタグが付きやすく、事後層化で補正）。タグが少ない都市は欠損のまま。詳細は `etl/notes/osm-hours.md`。

出典: [osm-hours](/sources/osm-hours.md)
