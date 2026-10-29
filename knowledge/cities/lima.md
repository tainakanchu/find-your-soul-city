---
type: City
title: "Lima"
description: "リマ（PE）の都市プロファイル。GHS-UCDB 都市圏 2171 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: lima
name_ja: "リマ"
country: PE
region: "Latin America and the Caribbean"
lat: -12.0524
lon: -77.0181
boundary:
  source: ghsl-ucdb
  id: 2171
  name: "Lima"
  area_km2: 984.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 15.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 71.1, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.36, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 17417, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 19.3, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 1.54, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 18.7, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 12.6, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 21.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 209.6, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 9.9, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 86.3, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 18.5, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 18.1, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 23.3, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 1.88, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 10828104, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 67.2, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 2171「Lima」。面積 984.0 km²、2025 年人口 10,828,104 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 15.0 % | 2024 | observed |
| 年平均雲量 | 71.1 % | 1990-2019 | observed |
| 文化施設の密度 | 0.36 件/km² | 2026 | estimated |
| 人口加重密度 | 17417 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 19.3 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 1.54 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 18.7 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 12.6 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 21.0 µg/m³ | 2020 | estimated |
| 年降水量 | 209.6 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 9.9 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 86.3 % | 2026 | estimated |
| 夏至の日の入り時刻 | 18.5 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 18.1 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 23.3 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 1.88 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 10828104 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 67.2 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
