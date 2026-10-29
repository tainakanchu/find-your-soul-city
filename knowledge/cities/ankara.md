---
type: City
title: "Ankara"
description: "アンカラ（TR）の都市プロファイル。GHS-UCDB 都市圏 4921 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: ankara
name_ja: "アンカラ"
country: TR
region: "Northern Africa and Western Asia"
lat: 39.9562
lon: 32.8324
boundary:
  source: ghsl-ucdb
  id: 4921
  name: "Ankara"
  area_km2: 357.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 0.07, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 39.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.3, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 21380, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 9.0, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 22.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 457.1, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 11.9, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 0.75, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.4, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 13.0, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 3695989, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 65.9, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 4921「Ankara」。面積 357.0 km²、2025 年人口 3,695,989 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.07 % | 2024 | observed |
| 年平均雲量 | 39.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.3 件/km² | 2026 | estimated |
| 人口加重密度 | 21380 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 9.0 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 22.0 µg/m³ | 2020 | estimated |
| 年降水量 | 457.1 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 11.9 % | 2024 | observed |
| 最寒月の平均気温 | 0.75 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 24.4 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 13.0 % | 2021 | observed |
| 都市圏の人口 | 3695989 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 65.9 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
