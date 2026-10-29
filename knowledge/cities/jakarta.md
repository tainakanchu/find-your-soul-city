---
type: City
title: "Jakarta"
description: "ジャカルタ（ID）の都市プロファイル。GHS-UCDB 都市圏 5472 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: jakarta
name_ja: "ジャカルタ"
country: ID
region: "Eastern and South-Eastern Asia"
lat: -6.5119
lon: 106.8137
boundary:
  source: ghsl-ucdb
  id: 5472
  name: "Jakarta"
  area_km2: 4614
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 0.39, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 75.9, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.04, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 14212, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 23.7, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 33.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 2369, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 5.21, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 25.7, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 26.9, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 30.8, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 40545126, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 35.9, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5472「Jakarta」。面積 4614 km²、2025 年人口 40,545,126 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.39 % | 2024 | observed |
| 年平均雲量 | 75.9 % | 1990-2019 | observed |
| 文化施設の密度 | 0.04 件/km² | 2026 | estimated |
| 人口加重密度 | 14212 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 23.7 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 33.0 µg/m³ | 2020 | estimated |
| 年降水量 | 2369 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 5.21 % | 2024 | observed |
| 最寒月の平均気温 | 25.7 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 26.9 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 30.8 % | 2021 | observed |
| 都市圏の人口 | 40545126 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 35.9 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
