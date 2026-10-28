---
type: City
title: "Budapest"
description: "ブダペスト（HU）の都市プロファイル。GHS-UCDB 都市圏 964 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: budapest
name_ja: "ブダペスト"
country: HU
region: "Europe"
lat: 47.5027
lon: 19.0929
boundary:
  source: ghsl-ucdb
  id: 964
  name: "Budapest"
  area_km2: 368.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T21:28:39Z }
metrics:
  bike_protected: { value: 20.2, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 57.9, quality: observed, source: era5, year: "1990-2019" }
  density_weighted: { value: 8055, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 14.2, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 13.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 667.7, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 21.8, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: -0.09, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 22.1, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 40.3, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1743875, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 67.2, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 964「Budapest」。面積 368.0 km²、2025 年人口 1,743,875 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 20.2 % | 2024 | observed |
| 年平均雲量 | 57.9 % | 1990-2019 | observed |
| 人口加重密度 | 8055 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 14.2 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 13.0 µg/m³ | 2020 | estimated |
| 年降水量 | 667.7 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 21.8 % | 2024 | observed |
| 最寒月の平均気温 | -0.09 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 22.1 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 40.3 % | 2021 | observed |
| 都市圏の人口 | 1743875 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 67.2 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
