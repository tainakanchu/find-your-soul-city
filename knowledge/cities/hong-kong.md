---
type: City
title: "Hong Kong"
description: "香港（HK）の都市プロファイル。GHS-UCDB 都市圏 11185 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: hong-kong
name_ja: "香港"
country: HK
region: "Eastern and South-Eastern Asia"
lat: 22.3168
lon: 114.1934
boundary:
  source: ghsl-ucdb
  id: 11185
  name: "Hong Kong"
  area_km2: 220.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 2.75, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 64.6, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.74, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 56895, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 25.5, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 16.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1760, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 35.8, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 15.2, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 28.8, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 52.2, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 4807599, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 45.7, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 11185「Hong Kong」。面積 220.0 km²、2025 年人口 4,807,599 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 2.75 % | 2024 | observed |
| 年平均雲量 | 64.6 % | 1990-2019 | observed |
| 文化施設の密度 | 0.74 件/km² | 2026 | estimated |
| 人口加重密度 | 56895 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 25.5 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 16.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1760 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 35.8 % | 2024 | observed |
| 最寒月の平均気温 | 15.2 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 28.8 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 52.2 % | 2021 | observed |
| 都市圏の人口 | 4807599 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 45.7 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
