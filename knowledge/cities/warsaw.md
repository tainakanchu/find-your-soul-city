---
type: City
title: "Warsaw"
description: "ワルシャワ（PL）の都市プロファイル。GHS-UCDB 都市圏 3712 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: warsaw
name_ja: "ワルシャワ"
country: PL
region: "Europe"
lat: 52.2061
lon: 21.0219
boundary:
  source: ghsl-ucdb
  id: 3712
  name: "Warsaw"
  area_km2: 415.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 55.3, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 66.7, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.88, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 8045, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 13.7, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 16.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 700.0, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 25.8, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: -1.44, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 19.6, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 43.5, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1999986, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 72.3, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 3712「Warsaw」。面積 415.0 km²、2025 年人口 1,999,986 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 55.3 % | 2024 | observed |
| 年平均雲量 | 66.7 % | 1990-2019 | observed |
| 文化施設の密度 | 0.88 件/km² | 2026 | estimated |
| 人口加重密度 | 8045 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 13.7 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 16.0 µg/m³ | 2020 | estimated |
| 年降水量 | 700.0 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 25.8 % | 2024 | observed |
| 最寒月の平均気温 | -1.44 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 19.6 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 43.5 % | 2021 | observed |
| 都市圏の人口 | 1999986 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 72.3 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
