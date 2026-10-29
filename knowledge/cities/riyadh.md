---
type: City
title: "Riyadh"
description: "リヤド（SA）の都市プロファイル。GHS-UCDB 都市圏 3026 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: riyadh
name_ja: "リヤド"
country: SA
region: "Northern Africa and Western Asia"
lat: 24.6826
lon: 46.7201
boundary:
  source: ghsl-ucdb
  id: 3026
  name: "Riyadh"
  area_km2: 1108
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 19.2, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.03, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 10112, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 5.06, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 116.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 69.2, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 14.3, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 36.7, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 1.66, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 7970319, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 13.1, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 3026「Riyadh」。面積 1108 km²、2025 年人口 7,970,319 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 19.2 % | 1990-2019 | observed |
| 文化施設の密度 | 0.03 件/km² | 2026 | estimated |
| 人口加重密度 | 10112 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 5.06 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 116.0 µg/m³ | 2020 | estimated |
| 年降水量 | 69.2 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 14.3 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 36.7 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 1.66 % | 2021 | observed |
| 都市圏の人口 | 7970319 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 13.1 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
