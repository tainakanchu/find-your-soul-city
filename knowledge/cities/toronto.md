---
type: City
title: "Toronto"
description: "トロント（CA）の都市プロファイル。GHS-UCDB 都市圏 2869 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: toronto
name_ja: "トロント"
country: CA
region: "Northern America"
lat: 43.708
lon: -79.5337
boundary:
  source: ghsl-ucdb
  id: 2869
  name: "Toronto"
  area_km2: 1620
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 21.5, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 62.1, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.2, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 6141, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 15.0, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.33, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 24.6, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 28.2, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 6.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 869.5, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 13.6, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 94.8, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 21.1, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: -4.86, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 21.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 26.9, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 5566382, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 55.8, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 2869「Toronto」。面積 1620 km²、2025 年人口 5,566,382 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 21.5 % | 2024 | observed |
| 年平均雲量 | 62.1 % | 1990-2019 | observed |
| 文化施設の密度 | 0.2 件/km² | 2026 | estimated |
| 人口加重密度 | 6141 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 15.0 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.33 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 24.6 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 28.2 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 6.0 µg/m³ | 2020 | estimated |
| 年降水量 | 869.5 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 13.6 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 94.8 % | 2026 | estimated |
| 夏至の日の入り時刻 | 21.1 時刻 | 2025 | estimated |
| 最寒月の平均気温 | -4.86 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 21.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 26.9 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 5566382 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 55.8 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
