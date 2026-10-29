---
type: City
title: "Dublin"
description: "ダブリン（IE）の都市プロファイル。GHS-UCDB 都市圏 394 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: dublin
name_ja: "ダブリン"
country: IE
region: "Europe"
lat: 53.3241
lon: -6.3279
boundary:
  source: ghsl-ucdb
  id: 394
  name: "Dublin"
  area_km2: 301.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 29.8, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 73.3, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.5, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 5406, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 11.8, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 8.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 925.3, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 8.28, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 6.11, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 15.9, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 25.3, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1124520, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 69.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 394「Dublin」。面積 301.0 km²、2025 年人口 1,124,520 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 29.8 % | 2024 | observed |
| 年平均雲量 | 73.3 % | 1990-2019 | observed |
| 文化施設の密度 | 0.5 件/km² | 2026 | estimated |
| 人口加重密度 | 5406 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 11.8 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 8.0 µg/m³ | 2020 | estimated |
| 年降水量 | 925.3 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 8.28 % | 2024 | observed |
| 最寒月の平均気温 | 6.11 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 15.9 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 25.3 % | 2021 | observed |
| 都市圏の人口 | 1124520 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 69.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
