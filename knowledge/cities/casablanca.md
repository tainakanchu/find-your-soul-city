---
type: City
title: "Casablanca"
description: "カサブランカ（MA）の都市プロファイル。GHS-UCDB 都市圏 2102 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: casablanca
name_ja: "カサブランカ"
country: MA
region: "Northern Africa and Western Asia"
lat: 33.6196
lon: -7.4885
boundary:
  source: ghsl-ucdb
  id: 2102
  name: "Casablanca"
  area_km2: 415.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T21:28:39Z }
metrics:
  bike_protected: { value: 0.02, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 40.4, quality: observed, source: era5, year: "1990-2019" }
  density_weighted: { value: 33252, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 18.5, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 21.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 332.0, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 23.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 12.9, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 5.54, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 4577677, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 46.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 2102「Casablanca」。面積 415.0 km²、2025 年人口 4,577,677 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.02 % | 2024 | observed |
| 年平均雲量 | 40.4 % | 1990-2019 | observed |
| 人口加重密度 | 33252 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 18.5 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 21.0 µg/m³ | 2020 | estimated |
| 年降水量 | 332.0 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 23.0 % | 2024 | observed |
| 最寒月の平均気温 | 12.9 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 24.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 5.54 % | 2021 | observed |
| 都市圏の人口 | 4577677 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 46.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
