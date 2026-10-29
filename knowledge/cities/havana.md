---
type: City
title: "Havana"
description: "ハバナ（CU）の都市プロファイル。GHS-UCDB 都市圏 367 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: havana
name_ja: "ハバナ"
country: CU
region: "Latin America and the Caribbean"
lat: 23.0758
lon: -82.3808
boundary:
  source: ghsl-ucdb
  id: 367
  name: "Havana"
  area_km2: 321.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 46.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 1.04, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 11420, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 23.4, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.58, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: 49.8, quality: estimated, source: osm-hours, year: 2026 }
  late_shops: { value: 4.71, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 13.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 851.1, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 58.8, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 20.3, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 22.1, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 27.9, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 37.8, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 1.67, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 1632772, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 60.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 367「Havana」。面積 321.0 km²、2025 年人口 1,632,772 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 46.0 % | 1990-2019 | observed |
| 文化施設の密度 | 1.04 件/km² | 2026 | estimated |
| 人口加重密度 | 11420 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 23.4 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.58 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 49.8 % | 2026 | estimated |
| 深夜 23 時に開いている食料品店の割合 | 4.71 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 13.0 µg/m³ | 2020 | estimated |
| 年降水量 | 851.1 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 58.8 % | 2026 | estimated |
| 夏至の日の入り時刻 | 20.3 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 22.1 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 27.9 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 37.8 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 1.67 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 1632772 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 60.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
