---
type: City
title: "Fortaleza"
description: "フォルタレザ（BR）の都市プロファイル。GHS-UCDB 都市圏 8154 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: fortaleza
name_ja: "フォルタレザ"
country: BR
region: "Latin America and the Caribbean"
lat: -3.8104
lon: -38.5418
boundary:
  source: ghsl-ucdb
  id: 8154
  name: "Fortaleza"
  area_km2: 413.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 14.9, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 47.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.24, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 12798, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.0, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.12, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 27.4, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 10.3, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 7.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1047, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: null, quality: missing, source: itdp-atlas, year: null, reason: "Atlas rapid-transit station data incomplete: 4 stations on 24 line-km (0.17/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 1.9 % is not credible" }
  sunday_shops: { value: 83.5, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 17.7, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 26.4, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 27.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 17.6, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 3324149, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 65.3, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 8154「Fortaleza」。面積 413.0 km²、2025 年人口 3,324,149 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 14.9 % | 2024 | observed |
| 年平均雲量 | 47.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.24 件/km² | 2026 | estimated |
| 人口加重密度 | 12798 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.0 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.12 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 27.4 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 10.3 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 7.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1047 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 欠損 | — | Atlas rapid-transit station data incomplete: 4 stations on 24 line-km (0.17/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 1.9 % is not credible |
| 日曜の昼に開いている食料品店の割合 | 83.5 % | 2026 | estimated |
| 夏至の日の入り時刻 | 17.7 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 26.4 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 27.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 17.6 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 3324149 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 65.3 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
