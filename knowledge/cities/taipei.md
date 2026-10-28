---
type: City
title: "Taipei"
description: "台北（TW）の都市プロファイル。GHS-UCDB 都市圏 1142 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: taipei
name_ja: "台北"
country: TW
region: "Eastern and South-Eastern Asia"
lat: 25.0183
lon: 121.4986
boundary:
  source: ghsl-ucdb
  id: 1142
  name: "Taipei"
  area_km2: 972.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T22:03:04Z }
metrics:
  bike_protected: { value: 15.2, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 67.4, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.43, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 23023, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 23.7, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 13.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1884, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 22.1, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 15.8, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 29.2, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 44.0, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 9686521, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 49.3, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1142「Taipei」。面積 972.0 km²、2025 年人口 9,686,521 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 15.2 % | 2024 | observed |
| 年平均雲量 | 67.4 % | 1990-2019 | observed |
| 文化施設の密度 | 0.43 件/km² | 2026 | estimated |
| 人口加重密度 | 23023 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 23.7 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 13.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1884 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 22.1 % | 2024 | observed |
| 最寒月の平均気温 | 15.8 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 29.2 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 44.0 % | 2021 | observed |
| 都市圏の人口 | 9686521 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 49.3 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
