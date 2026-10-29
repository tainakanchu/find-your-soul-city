---
type: City
title: "Cebu City"
description: "セブ（PH）の都市プロファイル。GHS-UCDB 都市圏 5065 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: cebu
name_ja: "セブ"
country: PH
region: "Eastern and South-Eastern Asia"
lat: 10.3129
lon: 123.9362
boundary:
  source: ghsl-ucdb
  id: 5065
  name: "Cebu City"
  area_km2: 416.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 0.14, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 74.8, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.07, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 17446, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 25.2, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 5.99, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 30.4, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 61.6, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 20.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 2215, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 100.0, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 18.1, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 27.2, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 29.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 48.8, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 2.33, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 3191585, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 43.1, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5065「Cebu City」。面積 416.0 km²、2025 年人口 3,191,585 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.14 % | 2024 | observed |
| 年平均雲量 | 74.8 % | 1990-2019 | observed |
| 文化施設の密度 | 0.07 件/km² | 2026 | estimated |
| 人口加重密度 | 17446 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 25.2 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 5.99 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 30.4 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 61.6 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 20.0 µg/m³ | 2020 | estimated |
| 年降水量 | 2215 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 100.0 % | 2026 | estimated |
| 夏至の日の入り時刻 | 18.1 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 27.2 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 29.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 48.8 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 2.33 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 3191585 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 43.1 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
