---
type: City
title: "Hyderabad"
description: "ハイデラバード（IN）の都市プロファイル。GHS-UCDB 都市圏 9524 上で集計した実データ。"
status: generated
tags: [city, "Central and Southern Asia"]
city_id: hyderabad
name_ja: "ハイデラバード"
country: IN
region: "Central and Southern Asia"
lat: 17.4312
lon: 78.471
boundary:
  source: ghsl-ucdb
  id: 9524
  name: "Hyderabad"
  area_km2: 889.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 0.03, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 51.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.21, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 19975, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 21.6, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 43.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 793.5, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 7.2, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 21.8, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 32.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 16.3, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 9455230, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 41.8, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 9524「Hyderabad」。面積 889.0 km²、2025 年人口 9,455,230 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.03 % | 2024 | observed |
| 年平均雲量 | 51.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.21 件/km² | 2026 | estimated |
| 人口加重密度 | 19975 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 21.6 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 43.0 µg/m³ | 2020 | estimated |
| 年降水量 | 793.5 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 7.2 % | 2024 | observed |
| 最寒月の平均気温 | 21.8 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 32.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 16.3 % | 2021 | observed |
| 都市圏の人口 | 9455230 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 41.8 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
