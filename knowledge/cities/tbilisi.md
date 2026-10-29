---
type: City
title: "Tbilisi"
description: "トビリシ（GE）の都市プロファイル。GHS-UCDB 都市圏 467 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: tbilisi
name_ja: "トビリシ"
country: GE
region: "Northern Africa and Western Asia"
lat: 41.7179
lon: 44.7944
boundary:
  source: ghsl-ucdb
  id: 467
  name: "Tbilisi"
  area_km2: 151.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 6.26, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 52.7, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.93, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 11402, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 14.3, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 19.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 752.0, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 28.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 1.31, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.8, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 24.0, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 988278, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 63.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 467「Tbilisi」。面積 151.0 km²、2025 年人口 988,278 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 6.26 % | 2024 | observed |
| 年平均雲量 | 52.7 % | 1990-2019 | observed |
| 文化施設の密度 | 0.93 件/km² | 2026 | estimated |
| 人口加重密度 | 11402 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 14.3 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 19.0 µg/m³ | 2020 | estimated |
| 年降水量 | 752.0 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 28.0 % | 2024 | observed |
| 最寒月の平均気温 | 1.31 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 24.8 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 24.0 % | 2021 | observed |
| 都市圏の人口 | 988278 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 63.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
