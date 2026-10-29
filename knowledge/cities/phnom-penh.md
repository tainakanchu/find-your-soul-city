---
type: City
title: "Phnom Penh"
description: "プノンペン（KH）の都市プロファイル。GHS-UCDB 都市圏 1741 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: phnom-penh
name_ja: "プノンペン"
country: KH
region: "Eastern and South-Eastern Asia"
lat: 11.5591
lon: 104.8773
boundary:
  source: ghsl-ucdb
  id: 1741
  name: "Phnom Penh"
  area_km2: 354.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 0.51, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 71.3, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.12, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 15969, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.3, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 57.5, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 14.2, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "only 47 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 322 POIs in total)" }
  pm25: { value: 28.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1362, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "only 47 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 322 POIs in total)" }
  sunset_summer: { value: 18.4, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 26.7, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 30.2, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 15.4, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 2419131, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 42.2, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1741「Phnom Penh」。面積 354.0 km²、2025 年人口 2,419,131 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.51 % | 2024 | observed |
| 年平均雲量 | 71.3 % | 1990-2019 | observed |
| 文化施設の密度 | 0.12 件/km² | 2026 | estimated |
| 人口加重密度 | 15969 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.3 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 57.5 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 14.2 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 欠損 | — | only 47 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 322 POIs in total) |
| PM2.5 年平均濃度（人口加重） | 28.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1362 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 欠損 | — | only 47 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 322 POIs in total) |
| 夏至の日の入り時刻 | 18.4 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 26.7 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 30.2 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 15.4 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 2419131 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 42.2 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
