---
type: City
title: "Denver"
description: "デンバー（US）の都市プロファイル。GHS-UCDB 都市圏 5932 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: denver
name_ja: "デンバー"
country: US
region: "Northern America"
lat: 39.7416
lon: -104.9772
boundary:
  source: ghsl-ucdb
  id: 5932
  name: "Denver"
  area_km2: 1194
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 29.5, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 43.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.19, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 2822, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 9.43, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.98, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 12.0, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 39.3, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 8.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 544.6, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 6.19, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 96.8, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 20.5, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: -1.59, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 22.3, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 22.3, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 2425086, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 29.1, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5932「Denver」。面積 1194 km²、2025 年人口 2,425,086 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 29.5 % | 2024 | observed |
| 年平均雲量 | 43.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.19 件/km² | 2026 | estimated |
| 人口加重密度 | 2822 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 9.43 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.98 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 12.0 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 39.3 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 8.0 µg/m³ | 2020 | estimated |
| 年降水量 | 544.6 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 6.19 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 96.8 % | 2026 | estimated |
| 夏至の日の入り時刻 | 20.5 時刻 | 2025 | estimated |
| 最寒月の平均気温 | -1.59 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 22.3 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 22.3 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 2425086 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 29.1 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
