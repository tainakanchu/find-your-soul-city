---
type: City
title: "Istanbul"
description: "イスタンブール（TR）の都市プロファイル。GHS-UCDB 都市圏 2637 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: istanbul
name_ja: "イスタンブール"
country: TR
region: "Northern Africa and Western Asia"
lat: 40.9877
lon: 28.7645
boundary:
  source: ghsl-ucdb
  id: 2637
  name: "Istanbul"
  area_km2: 1269
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 2.31, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 47.6, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.33, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 24674, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 19.1, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.12, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 43.4, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 12.3, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 18.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 743.1, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 28.3, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 74.8, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 20.7, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 6.33, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.3, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 23.9, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 14210222, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 59.8, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 2637「Istanbul」。面積 1269 km²、2025 年人口 14,210,222 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 2.31 % | 2024 | observed |
| 年平均雲量 | 47.6 % | 1990-2019 | observed |
| 文化施設の密度 | 0.33 件/km² | 2026 | estimated |
| 人口加重密度 | 24674 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 19.1 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.12 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 43.4 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 12.3 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 18.0 µg/m³ | 2020 | estimated |
| 年降水量 | 743.1 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 28.3 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 74.8 % | 2026 | estimated |
| 夏至の日の入り時刻 | 20.7 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 6.33 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 24.3 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 23.9 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 14210222 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 59.8 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
