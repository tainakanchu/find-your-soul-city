---
type: City
title: "Rome"
description: "ローマ（IT）の都市プロファイル。GHS-UCDB 都市圏 3938 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: rome
name_ja: "ローマ"
country: IT
region: "Europe"
lat: 41.8761
lon: 12.5494
boundary:
  source: ghsl-ucdb
  id: 3938
  name: "Rome"
  area_km2: 467.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 12.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 42.6, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.86, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 10732, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 17.3, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 14.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 884.9, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 28.5, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 7.59, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 25.7, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 29.3, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 2476089, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 52.5, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 3938「Rome」。面積 467.0 km²、2025 年人口 2,476,089 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 12.0 % | 2024 | observed |
| 年平均雲量 | 42.6 % | 1990-2019 | observed |
| 文化施設の密度 | 0.86 件/km² | 2026 | estimated |
| 人口加重密度 | 10732 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 17.3 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 14.0 µg/m³ | 2020 | estimated |
| 年降水量 | 884.9 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 28.5 % | 2024 | observed |
| 最寒月の平均気温 | 7.59 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 25.7 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 29.3 % | 2021 | observed |
| 都市圏の人口 | 2476089 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 52.5 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
