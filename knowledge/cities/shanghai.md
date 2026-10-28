---
type: City
title: "Shanghai"
description: "上海（CN）の都市プロファイル。GHS-UCDB 都市圏 11345 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: shanghai
name_ja: "上海"
country: CN
region: "Eastern and South-Eastern Asia"
lat: 31.2043
lon: 121.4788
boundary:
  source: ghsl-ucdb
  id: 11345
  name: "Shanghai"
  area_km2: 3128
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T21:28:39Z }
metrics:
  bike_protected: { value: 9.92, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 61.8, quality: observed, source: era5, year: "1990-2019" }
  density_weighted: { value: 30726, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.7, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 20.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1362, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 25.6, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 5.18, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 28.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 17.3, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 30678616, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 22.7, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 11345「Shanghai」。面積 3128 km²、2025 年人口 30,678,616 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 9.92 % | 2024 | observed |
| 年平均雲量 | 61.8 % | 1990-2019 | observed |
| 人口加重密度 | 30726 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.7 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 20.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1362 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 25.6 % | 2024 | observed |
| 最寒月の平均気温 | 5.18 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 28.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 17.3 % | 2021 | observed |
| 都市圏の人口 | 30678616 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 22.7 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
