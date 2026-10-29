---
type: City
title: "Perth"
description: "パース（AU）の都市プロファイル。GHS-UCDB 都市圏 498 上で集計した実データ。"
status: generated
tags: [city, "Australia and New Zealand"]
city_id: perth
name_ja: "パース"
country: AU
region: "Australia and New Zealand"
lat: -31.9178
lon: 115.8624
boundary:
  source: ghsl-ucdb
  id: 498
  name: "Perth"
  area_km2: 784.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 38.2, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 37.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.16, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 2534, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 14.4, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 9.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 586.8, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 9.46, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 13.8, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.1, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 17.7, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1357382, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 32.3, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 498「Perth」。面積 784.0 km²、2025 年人口 1,357,382 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 38.2 % | 2024 | observed |
| 年平均雲量 | 37.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.16 件/km² | 2026 | estimated |
| 人口加重密度 | 2534 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 14.4 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 9.0 µg/m³ | 2020 | estimated |
| 年降水量 | 586.8 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 9.46 % | 2024 | observed |
| 最寒月の平均気温 | 13.8 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 24.1 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 17.7 % | 2021 | observed |
| 都市圏の人口 | 1357382 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 32.3 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
