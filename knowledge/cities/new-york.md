---
type: City
title: "New York City"
description: "ニューヨーク（US）の都市プロファイル。GHS-UCDB 都市圏 8099 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: new-york
name_ja: "ニューヨーク"
country: US
region: "Northern America"
lat: 40.736
lon: -73.7292
boundary:
  source: ghsl-ucdb
  id: 8099
  name: "New York City"
  area_km2: 3031
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 13.6, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 56.2, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.43, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 13617, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 18.4, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 7.32, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 16.6, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 42.0, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 7.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1182, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 32.6, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 96.7, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 20.5, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 0.44, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 36.6, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.33, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 14197659, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 45.9, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 8099「New York City」。面積 3031 km²、2025 年人口 14,197,659 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 13.6 % | 2024 | observed |
| 年平均雲量 | 56.2 % | 1990-2019 | observed |
| 文化施設の密度 | 0.43 件/km² | 2026 | estimated |
| 人口加重密度 | 13617 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 18.4 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 7.32 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 16.6 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 42.0 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 7.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1182 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 32.6 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 96.7 % | 2026 | estimated |
| 夏至の日の入り時刻 | 20.5 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 0.44 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 24.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 36.6 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.33 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 14197659 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 45.9 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
