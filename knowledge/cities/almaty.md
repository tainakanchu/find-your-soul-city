---
type: City
title: "Almaty"
description: "アルマトイ（KZ）の都市プロファイル。GHS-UCDB 都市圏 2847 上で集計した実データ。"
status: generated
tags: [city, "Central and Southern Asia"]
city_id: almaty
name_ja: "アルマトイ"
country: KZ
region: "Central and Southern Asia"
lat: 43.2789
lon: 76.9128
boundary:
  source: ghsl-ucdb
  id: 2847
  name: "Almaty"
  area_km2: 331.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 5.24, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 53.6, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.23, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 10485, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 9.12, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 24.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 772.4, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 8.5, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: -5.31, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 23.4, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 28.1, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 2315538, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 49.3, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 2847「Almaty」。面積 331.0 km²、2025 年人口 2,315,538 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 5.24 % | 2024 | observed |
| 年平均雲量 | 53.6 % | 1990-2019 | observed |
| 文化施設の密度 | 0.23 件/km² | 2026 | estimated |
| 人口加重密度 | 10485 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 9.12 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 24.0 µg/m³ | 2020 | estimated |
| 年降水量 | 772.4 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 8.5 % | 2024 | observed |
| 最寒月の平均気温 | -5.31 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 23.4 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 28.1 % | 2021 | observed |
| 都市圏の人口 | 2315538 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 49.3 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
