---
type: City
title: "Santiago"
description: "サンティアゴ（CL）の都市プロファイル。GHS-UCDB 都市圏 2334 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: santiago
name_ja: "サンティアゴ"
country: CL
region: "Latin America and the Caribbean"
lat: -33.4809
lon: -70.6505
boundary:
  source: ghsl-ucdb
  id: 2334
  name: "Santiago"
  area_km2: 801.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 25.4, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 35.7, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.46, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 12962, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 12.0, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 2.49, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 29.5, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "opening_hours tagged on 4.9% of 2496 groceries POIs (minimum 5%)" }
  pm25: { value: 22.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: null, quality: missing, source: era5, year: null, reason: "ERA5 の年降水量 523 mm が近傍の気象観測所（GHCN-M v4）の 287 mm と 1.82 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用" }
  rapid_transit: { value: 22.1, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "opening_hours tagged on 4.9% of 2496 groceries POIs (minimum 5%)" }
  sunset_summer: { value: 20.9, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 8.34, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 21.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 11.0, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 6633767, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 68.1, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 2334「Santiago」。面積 801.0 km²、2025 年人口 6,633,767 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 25.4 % | 2024 | observed |
| 年平均雲量 | 35.7 % | 1990-2019 | observed |
| 文化施設の密度 | 0.46 件/km² | 2026 | estimated |
| 人口加重密度 | 12962 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 12.0 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 2.49 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 29.5 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 欠損 | — | opening_hours tagged on 4.9% of 2496 groceries POIs (minimum 5%) |
| PM2.5 年平均濃度（人口加重） | 22.0 µg/m³ | 2020 | estimated |
| 年降水量 | 欠損 | — | ERA5 の年降水量 523 mm が近傍の気象観測所（GHCN-M v4）の 287 mm と 1.82 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用 |
| 高速公共交通の近くに住む人口の割合 | 22.1 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 欠損 | — | opening_hours tagged on 4.9% of 2496 groceries POIs (minimum 5%) |
| 夏至の日の入り時刻 | 20.9 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 8.34 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 21.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 11.0 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 6633767 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 68.1 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
