---
type: City
title: "Barcelona"
description: "バルセロナ（ES）の都市プロファイル。GHS-UCDB 都市圏 5071 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: barcelona
name_ja: "バルセロナ"
country: ES
region: "Europe"
lat: 41.4471
lon: 2.2082
boundary:
  source: ghsl-ucdb
  id: 5071
  name: "Barcelona"
  area_km2: 438.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 44.3, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 48.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 1.0, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 22097, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 19.2, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 4.8, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 44.1, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 16.7, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 12.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 619.8, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 53.9, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 50.4, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 21.5, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 9.03, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.2, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 24.1, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 3908362, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 60.1, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5071「Barcelona」。面積 438.0 km²、2025 年人口 3,908,362 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 44.3 % | 2024 | observed |
| 年平均雲量 | 48.0 % | 1990-2019 | observed |
| 文化施設の密度 | 1.0 件/km² | 2026 | estimated |
| 人口加重密度 | 22097 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 19.2 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 4.8 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 44.1 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 16.7 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 12.0 µg/m³ | 2020 | estimated |
| 年降水量 | 619.8 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 53.9 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 50.4 % | 2026 | estimated |
| 夏至の日の入り時刻 | 21.5 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 9.03 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 24.2 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 24.1 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 3908362 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 60.1 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
