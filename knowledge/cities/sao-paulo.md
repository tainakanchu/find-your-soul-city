---
type: City
title: "São Paulo"
description: "サンパウロ（BR）の都市プロファイル。GHS-UCDB 都市圏 7277 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: sao-paulo
name_ja: "サンパウロ"
country: BR
region: "Latin America and the Caribbean"
lat: -23.5938
lon: -46.6531
boundary:
  source: ghsl-ucdb
  id: 7277
  name: "São Paulo"
  area_km2: 2111
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T21:28:39Z }
metrics:
  bike_protected: { value: 3.83, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 67.5, quality: observed, source: era5, year: "1990-2019" }
  density_weighted: { value: 14635, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 19.2, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 15.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1407, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 5.37, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 16.7, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 23.2, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 22.5, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 19485158, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 53.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 7277「São Paulo」。面積 2111 km²、2025 年人口 19,485,158 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 3.83 % | 2024 | observed |
| 年平均雲量 | 67.5 % | 1990-2019 | observed |
| 人口加重密度 | 14635 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 19.2 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 15.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1407 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 5.37 % | 2024 | observed |
| 最寒月の平均気温 | 16.7 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 23.2 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 22.5 % | 2021 | observed |
| 都市圏の人口 | 19485158 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 53.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
