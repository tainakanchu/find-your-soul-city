---
type: City
title: "Stockholm"
description: "ストックホルム（SE）の都市プロファイル。GHS-UCDB 都市圏 1693 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: stockholm
name_ja: "ストックホルム"
country: SE
region: "Europe"
lat: 59.3506
lon: 18.0163
boundary:
  source: ghsl-ucdb
  id: 1693
  name: "Stockholm"
  area_km2: 339.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 73.7, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 66.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.73, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 8415, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 12.6, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 6.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 624.8, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 39.8, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: -1.59, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 17.6, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 55.4, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1543892, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 55.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1693「Stockholm」。面積 339.0 km²、2025 年人口 1,543,892 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 73.7 % | 2024 | observed |
| 年平均雲量 | 66.0 % | 1990-2019 | observed |
| 文化施設の密度 | 0.73 件/km² | 2026 | estimated |
| 人口加重密度 | 8415 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 12.6 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 6.0 µg/m³ | 2020 | estimated |
| 年降水量 | 624.8 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 39.8 % | 2024 | observed |
| 最寒月の平均気温 | -1.59 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 17.6 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 55.4 % | 2021 | observed |
| 都市圏の人口 | 1543892 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 55.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
