---
type: City
title: "Zurich"
description: "チューリッヒ（CH）の都市プロファイル。GHS-UCDB 都市圏 1689 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: zurich
name_ja: "チューリッヒ"
country: CH
region: "Europe"
lat: 47.3481
lon: 8.5464
boundary:
  source: ghsl-ucdb
  id: 1689
  name: "Zurich"
  area_km2: 187.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 29.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 64.1, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 1.39, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 6435, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 13.8, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 6.85, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 16.9, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 6.08, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 8.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1469, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 49.3, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 25.4, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 21.4, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 2.46, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 19.7, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 44.3, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 689208, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 64.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1689「Zurich」。面積 187.0 km²、2025 年人口 689,208 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 29.0 % | 2024 | observed |
| 年平均雲量 | 64.1 % | 1990-2019 | observed |
| 文化施設の密度 | 1.39 件/km² | 2026 | estimated |
| 人口加重密度 | 6435 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 13.8 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 6.85 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 16.9 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 6.08 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 8.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1469 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 49.3 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 25.4 % | 2026 | estimated |
| 夏至の日の入り時刻 | 21.4 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 2.46 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 19.7 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 44.3 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 689208 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 64.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
