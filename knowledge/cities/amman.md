---
type: City
title: "Amman"
description: "アンマン（JO）の都市プロファイル。GHS-UCDB 都市圏 992 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: amman
name_ja: "アンマン"
country: JO
region: "Northern Africa and Western Asia"
lat: 31.9866
lon: 35.9335
boundary:
  source: ghsl-ucdb
  id: 992
  name: "Amman"
  area_km2: 520.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 23.4, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.1, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 24035, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 14.6, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.09, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: null, quality: missing, source: osm-hours, year: null, reason: "chain/non-chain strata too small for post-stratification (1 chain, 51 non-chain parsed)" }
  late_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "only 36 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 373 POIs in total)" }
  pm25: { value: 36.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 192.0, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "only 36 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 373 POIs in total)" }
  sunset_summer: { value: 19.8, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 7.14, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 25.6, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 2.74, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 6425246, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 27.9, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 992「Amman」。面積 520.0 km²、2025 年人口 6,425,246 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 23.4 % | 1990-2019 | observed |
| 文化施設の密度 | 0.1 件/km² | 2026 | estimated |
| 人口加重密度 | 24035 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 14.6 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.09 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 欠損 | — | chain/non-chain strata too small for post-stratification (1 chain, 51 non-chain parsed) |
| 深夜 23 時に開いている食料品店の割合 | 欠損 | — | only 36 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 373 POIs in total) |
| PM2.5 年平均濃度（人口加重） | 36.0 µg/m³ | 2020 | estimated |
| 年降水量 | 192.0 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 欠損 | — | only 36 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 373 POIs in total) |
| 夏至の日の入り時刻 | 19.8 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 7.14 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 25.6 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 2.74 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 6425246 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 27.9 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
