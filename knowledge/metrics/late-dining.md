---
type: Metric
title: 深夜 23 時に開いている飲食店の割合
description: レストラン・カフェ・ファストフードのうち、平日 23 時に開いている店の割合（OSM の営業時間タグから推定）。
status: adopted
tags: [metric, osm-hours]
metric_key: late_dining
etl_key: eating_late_open_share
reference_column: eating_late23_post
reference_partial: "OSM の営業時間タグが十分にある都市だけ（基準集合 524 のうち約 290）"
adoption: adopted
unit: "%"
kind: ideal
transform: linear
tolerance: 12
source: osm-hours
period: "2026 年（OSM planet 2026-09-21、基準週の水曜 23:00）"
geography: "重心が都市圏ポリゴン内にある amenity=restaurant|cafe|fast_food"
method: "解析できる opening_hours タグを持つ店のうち水曜 23:00 に開いている割合を、チェーン（brand タグ）と非チェーンに分けて求め、全店に占めるチェーンの割合で重み付けし直す"
caveat: "タグ付きの店は無作為標本ではない。タグが少ない 18 都市（主にアフリカ・南アジア）は欠損"
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

レストラン・カフェ・ファストフードのうち、平日の 23 時に開いている店の割合。「夜遅い夕食が当たり前か」を表す。

# スコアへの入り方

理想値型。ユーザーの理想の割合との差をガウス関数で 0〜1 にする（σ = 12 ポイント）。

# 根拠と検証

対象都市の 15・50・85 パーセンタイルは 9.3・19・42%。夕食の遅い地域が高い（マドリード 57%、アテネ 66%、バルセロナ 44%、ローマ 42%、カイロ 75%、リヤド 87%）。ロンドン 12%、シドニー 8%、米国の都市 7〜25%。食料品店の深夜営業との順位相関は 0.27 で、別の内容として扱う。

朝 7 時に開いている飲食店の割合は、チェーンの補正で値が 12〜33 ポイント動き不安定なため採用しない（[早朝の飲食店](/metrics/early-dining.md)）。

# 注意点

タグ付きの店は無作為標本ではない。カフェ・ファストフードを含むため、高級店の営業時間は分からない。

出典: [osm-hours](/sources/osm-hours.md)
