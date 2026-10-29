---
type: Metric
title: 文化施設の密度
description: 都市圏 1 km² あたりの美術館・ギャラリー・劇場・アートセンター・映画館・音楽ホール/ライブ会場の数。
status: adopted
tags: [metric, osm]
metric_key: culture
etl_key: culture_venues_per_km2
reference_column: culture_per_km2
adoption: adopted
unit: "件/km²"
kind: higher_better
transform: log10
source: osm
period: "2026 年（OSM planet 2026-09-21）"
geography: "重心が都市圏ポリゴン内にある OSM の点・線・面"
method: "tourism=museum|gallery、amenity=theatre|arts_centre|cinema|music_venue|concert_hall を数え（同名・150 m 以内の重複は 1 件）、ポリゴン面積で割る"
caveat: "施設の規模や質は区別しない（大美術館も小さなギャラリーも 1 件）。OSM の登録漏れがあり、ジャカルタとラゴスは独立ソースとの比較で 2 倍以上の過小評価の可能性がある"
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 定義

都市圏 1 km² あたりの文化施設の数。「身の回りに文化施設が多いか」を表すため人口あたりではなく面積あたりにした（人口あたりはチューリッヒ・レイキャビクのような小都市を押し上げる）。

# スコアへの入り方

多いほど良い型。[基準分布](/model/reference-distribution.md)（人口 100 万人以上の全都市圏）の中での百分位（対数）。

# 根拠と検証

OSM の登録率の地域差を 2 つの独立ソースで確かめた（[etl/notes/osm.md](../../etl/notes/osm.md)）。

- Wikidata の著名な美術館・劇場・音楽ホールのうち OSM で見つかった割合（524 都市圏、地域別中央値）: 欧州 0.71、東/東南アジア 0.68、中南米 0.67、北米 0.66、サハラ以南 0.66、北アフリカ/西アジア 0.60、中央/南アジア 0.60、豪州/NZ 0.58。欧州と南半球の間に明確な差はない。
- Overture Maps（OSM を含まない）の美術館＋映画館との比: 地域別中央値 0.37〜0.67 で地域の傾きなし。都市の順位は Overture と Spearman 0.86、Wikidata と 0.88 で一致。

品質は `estimated`（登録データの数え上げで、網羅率が 6〜7 割の推定）。

# 注意点

施設の規模や質は区別しない。ジャカルタ・ラゴスは過小評価の可能性。

出典: [osm](/sources/osm.md)
