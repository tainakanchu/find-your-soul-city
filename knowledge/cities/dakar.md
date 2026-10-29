---
type: City
title: "Dakar"
description: "ダカール（SN）の都市プロファイル。GHS-UCDB 都市圏 39 上で集計した実データ。"
status: generated
tags: [city, "Sub-Saharan Africa"]
city_id: dakar
name_ja: "ダカール"
country: SN
region: "Sub-Saharan Africa"
lat: 14.7416
lon: -17.3826
boundary:
  source: ghsl-ucdb
  id: 39
  name: "Dakar"
  area_km2: 277.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 44.1, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.2, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 24623, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.6, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.45, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 46.6, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "only 29 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 671 POIs in total)" }
  pm25: { value: 42.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 301.2, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "only 29 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 671 POIs in total)" }
  sunset_summer: { value: 19.7, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 22.5, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 28.1, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 2.6, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 3970202, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 59.1, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 39「Dakar」。面積 277.0 km²、2025 年人口 3,970,202 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 44.1 % | 1990-2019 | observed |
| 文化施設の密度 | 0.2 件/km² | 2026 | estimated |
| 人口加重密度 | 24623 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.6 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.45 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 46.6 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 欠損 | — | only 29 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 671 POIs in total) |
| PM2.5 年平均濃度（人口加重） | 42.0 µg/m³ | 2020 | estimated |
| 年降水量 | 301.2 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 欠損 | — | only 29 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 671 POIs in total) |
| 夏至の日の入り時刻 | 19.7 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 22.5 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 28.1 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 2.6 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 3970202 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 59.1 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
