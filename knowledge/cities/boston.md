---
type: City
title: "Boston"
description: "ボストン（US）の都市プロファイル。GHS-UCDB 都市圏 8255 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: boston
name_ja: "ボストン"
country: US
region: "Northern America"
lat: 42.3696
lon: -71.1118
boundary:
  source: ghsl-ucdb
  id: 8255
  name: "Boston"
  area_km2: 508.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 22.1, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 57.2, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.56, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 5891, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 16.9, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 6.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1168, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 27.4, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: -1.13, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 22.3, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 44.8, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1669310, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 41.5, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 8255「Boston」。面積 508.0 km²、2025 年人口 1,669,310 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 22.1 % | 2024 | observed |
| 年平均雲量 | 57.2 % | 1990-2019 | observed |
| 文化施設の密度 | 0.56 件/km² | 2026 | estimated |
| 人口加重密度 | 5891 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 16.9 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 6.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1168 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 27.4 % | 2024 | observed |
| 最寒月の平均気温 | -1.13 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 22.3 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 44.8 % | 2021 | observed |
| 都市圏の人口 | 1669310 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 41.5 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
