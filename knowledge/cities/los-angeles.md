---
type: City
title: "Los Angeles"
description: "ロサンゼルス（US）の都市プロファイル。GHS-UCDB 都市圏 2007 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: los-angeles
name_ja: "ロサンゼルス"
country: US
region: "Northern America"
lat: 33.958
lon: -118.2227
boundary:
  source: ghsl-ucdb
  id: 2007
  name: "Los Angeles"
  area_km2: 4498
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 7.02, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 34.6, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.23, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 4832, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 15.1, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 13.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 386.4, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 7.1, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 12.7, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.0, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 12.2, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 13474333, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 30.3, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 2007「Los Angeles」。面積 4498 km²、2025 年人口 13,474,333 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 7.02 % | 2024 | observed |
| 年平均雲量 | 34.6 % | 1990-2019 | observed |
| 文化施設の密度 | 0.23 件/km² | 2026 | estimated |
| 人口加重密度 | 4832 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 15.1 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 13.0 µg/m³ | 2020 | estimated |
| 年降水量 | 386.4 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 7.1 % | 2024 | observed |
| 最寒月の平均気温 | 12.7 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 24.0 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 12.2 % | 2021 | observed |
| 都市圏の人口 | 13474333 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 30.3 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
