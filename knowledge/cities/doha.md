---
type: City
title: "Doha"
description: "ドーハ（QA）の都市プロファイル。GHS-UCDB 都市圏 153 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: doha
name_ja: "ドーハ"
country: QA
region: "Northern Africa and Western Asia"
lat: 25.2871
lon: 51.4768
boundary:
  source: ghsl-ucdb
  id: 153
  name: "Doha"
  area_km2: 392.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 5.96, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 17.6, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.1, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 10932, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.1, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 84.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 66.0, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 7.61, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 17.8, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 35.7, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 0.66, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1980416, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 21.2, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 153「Doha」。面積 392.0 km²、2025 年人口 1,980,416 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 5.96 % | 2024 | observed |
| 年平均雲量 | 17.6 % | 1990-2019 | observed |
| 文化施設の密度 | 0.1 件/km² | 2026 | estimated |
| 人口加重密度 | 10932 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.1 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 84.0 µg/m³ | 2020 | estimated |
| 年降水量 | 66.0 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 7.61 % | 2024 | observed |
| 最寒月の平均気温 | 17.8 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 35.7 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 0.66 % | 2021 | observed |
| 都市圏の人口 | 1980416 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 21.2 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
