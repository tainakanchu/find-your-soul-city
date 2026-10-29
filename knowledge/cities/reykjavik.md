---
type: City
title: "Reykjavik"
description: "レイキャビク（IS）の都市プロファイル。GHS-UCDB 都市圏 48 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: reykjavik
name_ja: "レイキャビク"
country: IS
region: "Europe"
lat: 64.1185
lon: -21.8712
boundary:
  source: ghsl-ucdb
  id: 48
  name: "Reykjavik"
  area_km2: 97.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: null, quality: missing, source: itdp-atlas, year: null, reason: "not in Atlas release update_2024 (no data_final/ghsl_00048/indicators_00048.rds); UCDB 2025 population 206,895 is below the Atlas inclusion threshold of 500,000 (methodology, General Topic 1a)" }
  cloud_cover_annual: { value: 76.6, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.76, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 3355, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 8.16, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 4.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1556, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: null, quality: missing, source: itdp-atlas, year: null, reason: "not in Atlas release update_2024 (no data_final/ghsl_00048/indicators_00048.rds); UCDB 2025 population 206,895 is below the Atlas inclusion threshold of 500,000 (methodology, General Topic 1a)" }
  temp_coldest: { value: 0.21, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 12.5, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 15.9, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 206895, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: null, quality: missing, source: itdp-atlas, year: null, reason: "not in Atlas release update_2024 (no data_final/ghsl_00048/indicators_00048.rds); UCDB 2025 population 206,895 is below the Atlas inclusion threshold of 500,000 (methodology, General Topic 1a)" }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 48「Reykjavik」。面積 97.0 km²、2025 年人口 206,895 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 欠損 | — | not in Atlas release update_2024 (no data_final/ghsl_00048/indicators_00048.rds); UCDB 2025 population 206,895 is below the Atlas inclusion threshold of 500,000 (methodology, General Topic 1a) |
| 年平均雲量 | 76.6 % | 1990-2019 | observed |
| 文化施設の密度 | 0.76 件/km² | 2026 | estimated |
| 人口加重密度 | 3355 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 8.16 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 4.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1556 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 欠損 | — | not in Atlas release update_2024 (no data_final/ghsl_00048/indicators_00048.rds); UCDB 2025 population 206,895 is below the Atlas inclusion threshold of 500,000 (methodology, General Topic 1a) |
| 最寒月の平均気温 | 0.21 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 12.5 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 15.9 % | 2021 | observed |
| 都市圏の人口 | 206895 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 欠損 | — | not in Atlas release update_2024 (no data_final/ghsl_00048/indicators_00048.rds); UCDB 2025 population 206,895 is below the Atlas inclusion threshold of 500,000 (methodology, General Topic 1a) |

この文書は `pnpm etl` が生成する。手で編集しない。
