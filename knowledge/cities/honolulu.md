---
type: City
title: "Honolulu"
description: "ホノルル（US）の都市プロファイル。GHS-UCDB 都市圏 193 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: honolulu
name_ja: "ホノルル"
country: US
region: "Northern America"
lat: 21.3349
lon: -157.8863
boundary:
  source: ghsl-ucdb
  id: 193
  name: "Honolulu"
  area_km2: 177.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 8.25, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 45.3, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.28, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 6064, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 20.1, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 3.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 502.9, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 3.23, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 22.1, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 26.1, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 25.5, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 541957, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 23.9, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 193「Honolulu」。面積 177.0 km²、2025 年人口 541,957 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 8.25 % | 2024 | observed |
| 年平均雲量 | 45.3 % | 1990-2019 | observed |
| 文化施設の密度 | 0.28 件/km² | 2026 | estimated |
| 人口加重密度 | 6064 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 20.1 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 3.0 µg/m³ | 2020 | estimated |
| 年降水量 | 502.9 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 3.23 % | 2024 | observed |
| 最寒月の平均気温 | 22.1 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 26.1 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 25.5 % | 2021 | observed |
| 都市圏の人口 | 541957 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 23.9 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
