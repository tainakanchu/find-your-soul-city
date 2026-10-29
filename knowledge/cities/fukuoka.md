---
type: City
title: "Fukuoka"
description: "福岡（JP）の都市プロファイル。GHS-UCDB 都市圏 907 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: fukuoka
name_ja: "福岡"
country: JP
region: "Eastern and South-Eastern Asia"
lat: 33.6283
lon: 130.4637
boundary:
  source: ghsl-ucdb
  id: 907
  name: "Fukuoka"
  area_km2: 450.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 0.47, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 63.7, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.18, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 7379, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 23.0, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 17.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1688, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 16.4, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 6.64, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 28.7, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 17.4, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 2213305, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 58.7, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 907「Fukuoka」。面積 450.0 km²、2025 年人口 2,213,305 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.47 % | 2024 | observed |
| 年平均雲量 | 63.7 % | 1990-2019 | observed |
| 文化施設の密度 | 0.18 件/km² | 2026 | estimated |
| 人口加重密度 | 7379 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 23.0 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 17.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1688 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 16.4 % | 2024 | observed |
| 最寒月の平均気温 | 6.64 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 28.7 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 17.4 % | 2021 | observed |
| 都市圏の人口 | 2213305 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 58.7 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
