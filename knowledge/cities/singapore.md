---
type: City
title: "Singapore"
description: "シンガポール（SG）の都市プロファイル。GHS-UCDB 都市圏 178 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: singapore
name_ja: "シンガポール"
country: SG
region: "Eastern and South-Eastern Asia"
lat: 1.3466
lon: 103.8265
boundary:
  source: ghsl-ucdb
  id: 178
  name: "Singapore"
  area_km2: 438.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 35.3, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 80.6, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.54, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 38975, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 25.0, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 13.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 2666, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 39.4, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 26.0, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 27.5, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 30.2, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 5117759, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 60.5, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 178「Singapore」。面積 438.0 km²、2025 年人口 5,117,759 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 35.3 % | 2024 | observed |
| 年平均雲量 | 80.6 % | 1990-2019 | observed |
| 文化施設の密度 | 0.54 件/km² | 2026 | estimated |
| 人口加重密度 | 38975 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 25.0 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 13.0 µg/m³ | 2020 | estimated |
| 年降水量 | 2666 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 39.4 % | 2024 | observed |
| 最寒月の平均気温 | 26.0 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 27.5 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 30.2 % | 2021 | observed |
| 都市圏の人口 | 5117759 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 60.5 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
