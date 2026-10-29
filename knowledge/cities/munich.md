---
type: City
title: "Munich"
description: "ミュンヘン（DE）の都市プロファイル。GHS-UCDB 都市圏 5249 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: munich
name_ja: "ミュンヘン"
country: DE
region: "Europe"
lat: 48.1417
lon: 11.5564
boundary:
  source: ghsl-ucdb
  id: 5249
  name: "Munich"
  area_km2: 345.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 71.7, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 65.4, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 1.26, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 7866, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 13.0, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 8.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1008, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 40.3, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 0.27, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 18.8, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 41.6, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1827704, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 77.1, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5249「Munich」。面積 345.0 km²、2025 年人口 1,827,704 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 71.7 % | 2024 | observed |
| 年平均雲量 | 65.4 % | 1990-2019 | observed |
| 文化施設の密度 | 1.26 件/km² | 2026 | estimated |
| 人口加重密度 | 7866 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 13.0 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 8.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1008 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 40.3 % | 2024 | observed |
| 最寒月の平均気温 | 0.27 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 18.8 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 41.6 % | 2021 | observed |
| 都市圏の人口 | 1827704 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 77.1 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
