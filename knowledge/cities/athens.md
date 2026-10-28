---
type: City
title: "Athens"
description: "アテネ（GR）の都市プロファイル。GHS-UCDB 都市圏 854 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: athens
name_ja: "アテネ"
country: GR
region: "Europe"
lat: 37.981
lon: 23.7114
boundary:
  source: ghsl-ucdb
  id: 854
  name: "Athens"
  area_km2: 412.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T22:03:04Z }
metrics:
  bike_protected: { value: 3.8, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 35.9, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 1.51, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 12599, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 14.9, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 14.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 384.2, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 25.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 8.8, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 28.0, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 16.0, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 3166757, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 75.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 854「Athens」。面積 412.0 km²、2025 年人口 3,166,757 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 3.8 % | 2024 | observed |
| 年平均雲量 | 35.9 % | 1990-2019 | observed |
| 文化施設の密度 | 1.51 件/km² | 2026 | estimated |
| 人口加重密度 | 12599 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 14.9 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 14.0 µg/m³ | 2020 | estimated |
| 年降水量 | 384.2 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 25.0 % | 2024 | observed |
| 最寒月の平均気温 | 8.8 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 28.0 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 16.0 % | 2021 | observed |
| 都市圏の人口 | 3166757 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 75.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
