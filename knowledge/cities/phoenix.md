---
type: City
title: "Phoenix"
description: "フェニックス（US）の都市プロファイル。GHS-UCDB 都市圏 4699 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: phoenix
name_ja: "フェニックス"
country: US
region: "Northern America"
lat: 33.5589
lon: -112.0932
boundary:
  source: ghsl-ucdb
  id: 4699
  name: "Phoenix"
  area_km2: 1304
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 6.22, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 28.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.11, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 2975, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 14.4, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 7.13, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 15.3, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 46.6, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 10.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 251.0, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 3.16, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 94.7, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 19.7, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 11.9, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 34.9, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 8.81, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 2608874, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 27.1, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 4699「Phoenix」。面積 1304 km²、2025 年人口 2,608,874 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 6.22 % | 2024 | observed |
| 年平均雲量 | 28.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.11 件/km² | 2026 | estimated |
| 人口加重密度 | 2975 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 14.4 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 7.13 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 15.3 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 46.6 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 10.0 µg/m³ | 2020 | estimated |
| 年降水量 | 251.0 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 3.16 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 94.7 % | 2026 | estimated |
| 夏至の日の入り時刻 | 19.7 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 11.9 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 34.9 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 8.81 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 2608874 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 27.1 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
