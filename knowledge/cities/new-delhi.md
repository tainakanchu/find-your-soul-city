---
type: City
title: "New Delhi"
description: "デリー（IN）の都市プロファイル。GHS-UCDB 都市圏 7963 上で集計した実データ。"
status: generated
tags: [city, "Central and Southern Asia"]
city_id: new-delhi
name_ja: "デリー"
country: IN
region: "Central and Southern Asia"
lat: 28.6039
lon: 77.2305
boundary:
  source: ghsl-ucdb
  id: 7963
  name: "New Delhi"
  area_km2: 2139
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 0.97, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 32.4, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.13, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 31478, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 25.4, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 94.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 717.6, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 15.3, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 13.7, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 33.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 16.7, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 31422508, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 37.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 7963「New Delhi」。面積 2139 km²、2025 年人口 31,422,508 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.97 % | 2024 | observed |
| 年平均雲量 | 32.4 % | 1990-2019 | observed |
| 文化施設の密度 | 0.13 件/km² | 2026 | estimated |
| 人口加重密度 | 31478 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 25.4 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 94.0 µg/m³ | 2020 | estimated |
| 年降水量 | 717.6 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 15.3 % | 2024 | observed |
| 最寒月の平均気温 | 13.7 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 33.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 16.7 % | 2021 | observed |
| 都市圏の人口 | 31422508 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 37.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
