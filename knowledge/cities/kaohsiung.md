---
type: City
title: "Kaohsiung"
description: "高雄（TW）の都市プロファイル。GHS-UCDB 都市圏 1919 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: kaohsiung
name_ja: "高雄"
country: TW
region: "Eastern and South-Eastern Asia"
lat: 22.6335
lon: 120.3421
boundary:
  source: ghsl-ucdb
  id: 1919
  name: "Kaohsiung"
  area_km2: 372.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 13.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 61.7, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.21, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 13678, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 25.2, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 12.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1972, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 25.5, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 18.6, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 28.6, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 22.6, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 2294772, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 43.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1919「Kaohsiung」。面積 372.0 km²、2025 年人口 2,294,772 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 13.0 % | 2024 | observed |
| 年平均雲量 | 61.7 % | 1990-2019 | observed |
| 文化施設の密度 | 0.21 件/km² | 2026 | estimated |
| 人口加重密度 | 13678 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 25.2 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 12.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1972 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 25.5 % | 2024 | observed |
| 最寒月の平均気温 | 18.6 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 28.6 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 22.6 % | 2021 | observed |
| 都市圏の人口 | 2294772 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 43.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
