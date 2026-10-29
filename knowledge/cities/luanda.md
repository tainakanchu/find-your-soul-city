---
type: City
title: "Luanda"
description: "ルアンダ（AO）の都市プロファイル。GHS-UCDB 都市圏 1082 上で集計した実データ。"
status: generated
tags: [city, "Sub-Saharan Africa"]
city_id: luanda
name_ja: "ルアンダ"
country: AO
region: "Sub-Saharan Africa"
lat: -8.9183
lon: 13.3051
boundary:
  source: ghsl-ucdb
  id: 1082
  name: "Luanda"
  area_km2: 936.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 66.3, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.04, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 24907, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 23.7, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.06, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 27.9, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "only 24 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 662 POIs in total)" }
  pm25: { value: 19.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 468.3, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: null, quality: missing, source: osm-hours, year: null, reason: "only 24 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 662 POIs in total)" }
  sunset_summer: { value: 18.4, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 21.5, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 27.3, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 2.35, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 11672134, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 15.3, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1082「Luanda」。面積 936.0 km²、2025 年人口 11,672,134 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 66.3 % | 1990-2019 | observed |
| 文化施設の密度 | 0.04 件/km² | 2026 | estimated |
| 人口加重密度 | 24907 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 23.7 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.06 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 27.9 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 欠損 | — | only 24 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 662 POIs in total) |
| PM2.5 年平均濃度（人口加重） | 19.0 µg/m³ | 2020 | estimated |
| 年降水量 | 468.3 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 欠損 | — | only 24 groceries POIs with a parseable opening_hours tag in the polygon (minimum 50; 662 POIs in total) |
| 夏至の日の入り時刻 | 18.4 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 21.5 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 27.3 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 2.35 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 11672134 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 15.3 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
