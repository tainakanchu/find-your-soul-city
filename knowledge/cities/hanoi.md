---
type: City
title: "Hanoi"
description: "ハノイ（VN）の都市プロファイル。GHS-UCDB 都市圏 1999 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: hanoi
name_ja: "ハノイ"
country: VN
region: "Eastern and South-Eastern Asia"
lat: 21.011
lon: 105.835
boundary:
  source: ghsl-ucdb
  id: 1999
  name: "Hanoi"
  area_km2: 925.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T22:03:04Z }
metrics:
  bike_protected: { value: 1.14, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 74.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.14, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 15680, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 25.9, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 38.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1765, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 2.17, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 16.9, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 29.7, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 28.2, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 4965520, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 33.9, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1999「Hanoi」。面積 925.0 km²、2025 年人口 4,965,520 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 1.14 % | 2024 | observed |
| 年平均雲量 | 74.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.14 件/km² | 2026 | estimated |
| 人口加重密度 | 15680 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 25.9 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 38.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1765 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 2.17 % | 2024 | observed |
| 最寒月の平均気温 | 16.9 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 29.7 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 28.2 % | 2021 | observed |
| 都市圏の人口 | 4965520 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 33.9 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
