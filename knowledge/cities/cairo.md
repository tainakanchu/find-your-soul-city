---
type: City
title: "Cairo"
description: "カイロ（EG）の都市プロファイル。GHS-UCDB 都市圏 4605 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: cairo
name_ja: "カイロ"
country: EG
region: "Northern Africa and Western Asia"
lat: 30.0226
lon: 31.2323
boundary:
  source: ghsl-ucdb
  id: 4605
  name: "Cairo"
  area_km2: 1680
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 19.7, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.09, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 49637, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 18.7, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 74.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 21.3, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 14.8, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 13.6, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 29.3, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 9.28, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 25230325, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 18.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 4605「Cairo」。面積 1680 km²、2025 年人口 25,230,325 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 19.7 % | 1990-2019 | observed |
| 文化施設の密度 | 0.09 件/km² | 2026 | estimated |
| 人口加重密度 | 49637 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 18.7 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 74.0 µg/m³ | 2020 | estimated |
| 年降水量 | 21.3 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 14.8 % | 2024 | observed |
| 最寒月の平均気温 | 13.6 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 29.3 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 9.28 % | 2021 | observed |
| 都市圏の人口 | 25230325 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 18.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
