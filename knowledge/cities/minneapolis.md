---
type: City
title: "Minneapolis [Saint Paul]"
description: "ミネアポリス（US）の都市プロファイル。GHS-UCDB 都市圏 7181 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: minneapolis
name_ja: "ミネアポリス"
country: US
region: "Northern America"
lat: 44.9747
lon: -93.1644
boundary:
  source: ghsl-ucdb
  id: 7181
  name: "Minneapolis [Saint Paul]"
  area_km2: 611.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 38.7, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 59.3, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.36, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 2749, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 16.2, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.15, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 9.18, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 10.0, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 7.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 875.3, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 8.76, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 96.9, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 21.0, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: -9.08, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 22.7, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 49.1, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 1217972, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 29.2, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 7181「Minneapolis [Saint Paul]」。面積 611.0 km²、2025 年人口 1,217,972 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 38.7 % | 2024 | observed |
| 年平均雲量 | 59.3 % | 1990-2019 | observed |
| 文化施設の密度 | 0.36 件/km² | 2026 | estimated |
| 人口加重密度 | 2749 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 16.2 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.15 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 9.18 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 10.0 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 7.0 µg/m³ | 2020 | estimated |
| 年降水量 | 875.3 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 8.76 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 96.9 % | 2026 | estimated |
| 夏至の日の入り時刻 | 21.0 時刻 | 2025 | estimated |
| 最寒月の平均気温 | -9.08 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 22.7 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 49.1 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 1217972 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 29.2 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
