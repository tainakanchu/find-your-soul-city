---
type: Metric
title: 日曜の昼に開いている食料品店の割合
description: スーパー・コンビニのうち、日曜 12 時に開いている店の割合（OSM の営業時間タグから推定）。
status: adopted
tags: [metric, osm-hours]
metric_key: sunday_shops
etl_key: grocery_sunday_open_share
reference_column: groceries_sun12_post
reference_partial: "OSM の営業時間タグが十分にある都市だけ（基準集合 524 のうち約 230）"
adoption: adopted
unit: "%"
kind: ideal
transform: linear
tolerance: 15
source: osm-hours
period: "2026 年（OSM planet 2026-09-21、基準週の日曜 12:00）"
geography: "重心が都市圏ポリゴン内にある shop=supermarket|convenience"
method: "解析できる opening_hours タグを持つ店のうち日曜 12:00 に開いている割合を、チェーン（brand タグ）と非チェーンに分けて求め、全店に占めるチェーンの割合で重み付けし直す"
caveat: "休日を日曜として数える。金曜・土曜が休日の国（イスラエル、中東の一部）の休日の様子は表さない。タグが少ない 30 都市は欠損"
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

スーパーとコンビニのうち、日曜の昼 12 時に開いている店の割合。

# スコアへの入り方

理想値型。ユーザーの理想の割合との差をガウス関数で 0〜1 にする（σ = 15 ポイント）。「日曜は店が閉まって静かなほうがいい」という好みもあるため、多いほど良い型にはしない。

方向型（基準分布での百分位）にしないのは、基準集合 524 都市圏のうち値があるのが約 230 で、百分位の基準に必要な 8 割に届かないため。

# 根拠と検証

対象都市の 15・50・85 パーセンタイルは 71・94・98%。はっきり低いのはドイツ語圏・ノルウェー・ギリシャなど日曜休業の法律がある国だけ（ミュンヘン 6.5%、ウィーン 7.8%、ベルリン 16%、チューリッヒ 25%、オスロ 36%、アテネ 33%）。それ以外は 80〜100% で、ほとんど差がつかない。σ = 15 はこの二つの群を分ける幅として置いた設計値。

スーパーだけの割合（深夜営業の売店を除く。ベルリン 2.2%）のほうが実態に近いが、値があるのが 80/130 都市のため採用しない（[日曜のスーパー](/metrics/supermarket-sunday.md)）。

# 注意点

休日を日曜として数える。タグ付きの店は無作為標本ではない。

出典: [osm-hours](/sources/osm-hours.md)
