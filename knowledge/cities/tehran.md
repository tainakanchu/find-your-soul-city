---
type: City
title: "Tehran"
description: "テヘラン（IR）の都市プロファイル。GHS-UCDB 都市圏 5174 上で集計した実データ。"
status: generated
tags: [city, "Central and Southern Asia"]
city_id: tehran
name_ja: "テヘラン"
country: IR
region: "Central and Southern Asia"
lat: 35.649
lon: 51.3978
boundary:
  source: ghsl-ucdb
  id: 5174
  name: "Tehran"
  area_km2: 825.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 1.34, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 29.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.46, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 18627, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 4.4, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 1.19, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 49.3, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 35.6, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 32.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 359.6, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 19.5, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 93.8, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 19.4, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 1.05, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 31.2, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 8.58, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 9363124, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 59.7, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5174「Tehran」。面積 825.0 km²、2025 年人口 9,363,124 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 1.34 % | 2024 | observed |
| 年平均雲量 | 29.0 % | 1990-2019 | observed |
| 文化施設の密度 | 0.46 件/km² | 2026 | estimated |
| 人口加重密度 | 18627 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 4.4 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 1.19 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 49.3 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 35.6 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 32.0 µg/m³ | 2020 | estimated |
| 年降水量 | 359.6 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 19.5 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 93.8 % | 2026 | estimated |
| 夏至の日の入り時刻 | 19.4 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 1.05 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 31.2 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 8.58 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 9363124 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 59.7 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
