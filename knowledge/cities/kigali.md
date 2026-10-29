---
type: City
title: "Kigali"
description: "キガリ（RW）の都市プロファイル。GHS-UCDB 都市圏 597 上で集計した実データ。"
status: generated
tags: [city, "Sub-Saharan Africa"]
city_id: kigali
name_ja: "キガリ"
country: RW
region: "Sub-Saharan Africa"
lat: -1.9533
lon: 30.0988
boundary:
  source: ghsl-ucdb
  id: 597
  name: "Kigali"
  area_km2: 286.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 0.21, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 73.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.04, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 9619, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 16.1, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 41.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 996.7, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 19.9, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 21.4, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 18.4, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1621760, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 24.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 597「Kigali」。面積 286.0 km²、2025 年人口 1,621,760 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.21 % | 2024 | observed |
| 年平均雲量 | 73.0 % | 1990-2019 | observed |
| 文化施設の密度 | 0.04 件/km² | 2026 | estimated |
| 人口加重密度 | 9619 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 16.1 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 41.0 µg/m³ | 2020 | estimated |
| 年降水量 | 996.7 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 19.9 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 21.4 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 18.4 % | 2021 | observed |
| 都市圏の人口 | 1621760 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 24.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
