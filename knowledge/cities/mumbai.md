---
type: City
title: "Mumbai"
description: "ムンバイ（IN）の都市プロファイル。GHS-UCDB 都市圏 7599 上で集計した実データ。"
status: generated
tags: [city, "Central and Southern Asia"]
city_id: mumbai
name_ja: "ムンバイ"
country: IN
region: "Central and Southern Asia"
lat: 19.1016
lon: 72.874
boundary:
  source: ghsl-ucdb
  id: 7599
  name: "Mumbai"
  area_km2: 738.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 0.4, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 43.2, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.24, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 58855, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 25.3, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 13.4, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 34.5, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "chain/non-chain strata too small for post-stratification (8 chain, 43 non-chain parsed)" }
  pm25: { value: 43.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: null, quality: missing, source: era5, year: null, reason: "ERA5 の年降水量 1447 mm が近傍の気象観測所（GHCN-M v4）の 2247 mm と 0.64 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用" }
  rapid_transit: { value: 5.7, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "chain/non-chain strata too small for post-stratification (8 chain, 43 non-chain parsed)" }
  sunset_summer: { value: 19.3, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 23.6, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 30.3, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 31.0, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.11, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 20453270, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 48.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 7599「Mumbai」。面積 738.0 km²、2025 年人口 20,453,270 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.4 % | 2024 | observed |
| 年平均雲量 | 43.2 % | 1990-2019 | observed |
| 文化施設の密度 | 0.24 件/km² | 2026 | estimated |
| 人口加重密度 | 58855 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 25.3 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 13.4 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 34.5 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 欠損 | — | chain/non-chain strata too small for post-stratification (8 chain, 43 non-chain parsed) |
| PM2.5 年平均濃度（人口加重） | 43.0 µg/m³ | 2020 | estimated |
| 年降水量 | 欠損 | — | ERA5 の年降水量 1447 mm が近傍の気象観測所（GHCN-M v4）の 2247 mm と 0.64 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用 |
| 高速公共交通の近くに住む人口の割合 | 5.7 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 欠損 | — | chain/non-chain strata too small for post-stratification (8 chain, 43 non-chain parsed) |
| 夏至の日の入り時刻 | 19.3 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 23.6 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 30.3 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 31.0 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.11 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 20453270 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 48.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
