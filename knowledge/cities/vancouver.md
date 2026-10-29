---
type: City
title: "Vancouver"
description: "バンクーバー（CA）の都市プロファイル。GHS-UCDB 都市圏 358 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: vancouver
name_ja: "バンクーバー"
country: CA
region: "Northern America"
lat: 49.2385
lon: -122.9809
boundary:
  source: ghsl-ucdb
  id: 358
  name: "Vancouver"
  area_km2: 649.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 26.7, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 66.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.31, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 6085, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 12.6, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 6.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 2355, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 16.8, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 3.98, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 18.5, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 44.1, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 2198107, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 49.1, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 358「Vancouver」。面積 649.0 km²、2025 年人口 2,198,107 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 26.7 % | 2024 | observed |
| 年平均雲量 | 66.0 % | 1990-2019 | observed |
| 文化施設の密度 | 0.31 件/km² | 2026 | estimated |
| 人口加重密度 | 6085 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 12.6 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 6.0 µg/m³ | 2020 | estimated |
| 年降水量 | 2355 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 16.8 % | 2024 | observed |
| 最寒月の平均気温 | 3.98 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 18.5 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 44.1 % | 2021 | observed |
| 都市圏の人口 | 2198107 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 49.1 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
