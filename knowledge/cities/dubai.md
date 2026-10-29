---
type: City
title: "Dubai"
description: "ドバイ（AE）の都市プロファイル。GHS-UCDB 都市圏 1007 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: dubai
name_ja: "ドバイ"
country: AE
region: "Northern Africa and Western Asia"
lat: 25.1947
lon: 55.3957
boundary:
  source: ghsl-ucdb
  id: 1007
  name: "Dubai"
  area_km2: 854.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 2.15, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 18.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.14, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 9522, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 23.3, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 44.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 81.2, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 6.86, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 19.7, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 35.9, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 3.09, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 4565478, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 23.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1007「Dubai」。面積 854.0 km²、2025 年人口 4,565,478 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 2.15 % | 2024 | observed |
| 年平均雲量 | 18.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.14 件/km² | 2026 | estimated |
| 人口加重密度 | 9522 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 23.3 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 44.0 µg/m³ | 2020 | estimated |
| 年降水量 | 81.2 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 6.86 % | 2024 | observed |
| 最寒月の平均気温 | 19.7 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 35.9 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 3.09 % | 2021 | observed |
| 都市圏の人口 | 4565478 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 23.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
