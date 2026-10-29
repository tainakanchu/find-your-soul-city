---
type: City
title: "Milan"
description: "ミラノ（IT）の都市プロファイル。GHS-UCDB 都市圏 1498 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: milan
name_ja: "ミラノ"
country: IT
region: "Europe"
lat: 45.5564
lon: 9.1935
boundary:
  source: ghsl-ucdb
  id: 1498
  name: "Milan"
  area_km2: 785.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 44.2, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 52.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.53, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 7879, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 16.3, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.53, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 34.5, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 11.1, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 21.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1167, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 24.2, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 80.2, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 21.3, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 3.19, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.6, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 26.7, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 3135553, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 60.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1498「Milan」。面積 785.0 km²、2025 年人口 3,135,553 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 44.2 % | 2024 | observed |
| 年平均雲量 | 52.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.53 件/km² | 2026 | estimated |
| 人口加重密度 | 7879 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 16.3 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.53 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 34.5 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 11.1 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 21.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1167 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 24.2 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 80.2 % | 2026 | estimated |
| 夏至の日の入り時刻 | 21.3 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 3.19 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 24.6 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 26.7 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 3135553 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 60.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
