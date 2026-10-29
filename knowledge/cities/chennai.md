---
type: City
title: "Chennai"
description: "チェンナイ（IN）の都市プロファイル。GHS-UCDB 都市圏 10300 上で集計した実データ。"
status: generated
tags: [city, "Central and Southern Asia"]
city_id: chennai
name_ja: "チェンナイ"
country: IN
region: "Central and Southern Asia"
lat: 13.0115
lon: 80.1763
boundary:
  source: ghsl-ucdb
  id: 10300
  name: "Chennai"
  area_km2: 1052
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 62.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.15, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 22677, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.6, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 31.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 997.4, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 12.1, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 24.8, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 31.5, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 26.0, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 11466400, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 40.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 10300「Chennai」。面積 1052 km²、2025 年人口 11,466,400 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 62.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.15 件/km² | 2026 | estimated |
| 人口加重密度 | 22677 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.6 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 31.0 µg/m³ | 2020 | estimated |
| 年降水量 | 997.4 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 12.1 % | 2024 | observed |
| 最寒月の平均気温 | 24.8 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 31.5 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 26.0 % | 2021 | observed |
| 都市圏の人口 | 11466400 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 40.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
