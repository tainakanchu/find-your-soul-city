---
type: City
title: "Kathmandu"
description: "カトマンズ（NP）の都市プロファイル。GHS-UCDB 都市圏 1822 上で集計した実データ。"
status: generated
tags: [city, "Central and Southern Asia"]
city_id: kathmandu
name_ja: "カトマンズ"
country: NP
region: "Central and Southern Asia"
lat: 27.7002
lon: 85.3313
boundary:
  source: ghsl-ucdb
  id: 1822
  name: "Kathmandu"
  area_km2: 350.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T21:28:39Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 57.9, quality: observed, source: era5, year: "1990-2019" }
  density_weighted: { value: 25709, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 20.3, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 44.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: null, quality: missing, source: era5, year: null, reason: "ERA5 の年降水量 2818 mm が近傍の気象観測所（GHCN-M v4）の 1471 mm と 1.92 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 10.5, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 23.1, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 16.8, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 3862697, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 64.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1822「Kathmandu」。面積 350.0 km²、2025 年人口 3,862,697 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 57.9 % | 1990-2019 | observed |
| 人口加重密度 | 25709 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 20.3 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 44.0 µg/m³ | 2020 | estimated |
| 年降水量 | 欠損 | — | ERA5 の年降水量 2818 mm が近傍の気象観測所（GHCN-M v4）の 1471 mm と 1.92 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用 |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 10.5 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 23.1 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 16.8 % | 2021 | observed |
| 都市圏の人口 | 3862697 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 64.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
