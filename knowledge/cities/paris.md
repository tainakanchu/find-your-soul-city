---
type: City
title: "Paris"
description: "パリ（FR）の都市プロファイル。GHS-UCDB 都市圏 2878 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: paris
name_ja: "パリ"
country: FR
region: "Europe"
lat: 48.8073
lon: 2.3823
boundary:
  source: ghsl-ucdb
  id: 2878
  name: "Paris"
  area_km2: 1421
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T21:28:39Z }
metrics:
  bike_protected: { value: 36.1, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 66.0, quality: observed, source: era5, year: "1990-2019" }
  density_weighted: { value: 14016, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 13.3, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 10.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 729.8, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 40.3, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 4.43, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 19.7, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 36.7, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 9328385, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 74.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 2878「Paris」。面積 1421 km²、2025 年人口 9,328,385 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 36.1 % | 2024 | observed |
| 年平均雲量 | 66.0 % | 1990-2019 | observed |
| 人口加重密度 | 14016 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 13.3 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 10.0 µg/m³ | 2020 | estimated |
| 年降水量 | 729.8 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 40.3 % | 2024 | observed |
| 最寒月の平均気温 | 4.43 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 19.7 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 36.7 % | 2021 | observed |
| 都市圏の人口 | 9328385 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 74.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
