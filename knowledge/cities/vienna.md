---
type: City
title: "Vienna"
description: "ウィーン（AT）の都市プロファイル。GHS-UCDB 都市圏 1081 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: vienna
name_ja: "ウィーン"
country: AT
region: "Europe"
lat: 48.1841
lon: 16.3673
boundary:
  source: ghsl-ucdb
  id: 1081
  name: "Vienna"
  area_km2: 325.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 48.2, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 61.1, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 1.65, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 11063, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 13.7, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 11.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 693.4, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 43.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 0.34, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 21.3, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 31.7, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 2056565, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 73.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1081「Vienna」。面積 325.0 km²、2025 年人口 2,056,565 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 48.2 % | 2024 | observed |
| 年平均雲量 | 61.1 % | 1990-2019 | observed |
| 文化施設の密度 | 1.65 件/km² | 2026 | estimated |
| 人口加重密度 | 11063 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 13.7 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 11.0 µg/m³ | 2020 | estimated |
| 年降水量 | 693.4 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 43.0 % | 2024 | observed |
| 最寒月の平均気温 | 0.34 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 21.3 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 31.7 % | 2021 | observed |
| 都市圏の人口 | 2056565 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 73.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
