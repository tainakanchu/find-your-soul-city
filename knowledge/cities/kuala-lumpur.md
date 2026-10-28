---
type: City
title: "Kuala Lumpur"
description: "クアラルンプール（MY）の都市プロファイル。GHS-UCDB 都市圏 1648 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: kuala-lumpur
name_ja: "クアラルンプール"
country: MY
region: "Eastern and South-Eastern Asia"
lat: 3.1022
lon: 101.5658
boundary:
  source: ghsl-ucdb
  id: 1648
  name: "Kuala Lumpur"
  area_km2: 1340
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T21:28:39Z }
metrics:
  bike_protected: { value: 1.79, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 83.2, quality: observed, source: era5, year: "1990-2019" }
  density_weighted: { value: 9412, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.4, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 17.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 2572, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: null, quality: missing, source: itdp-atlas, year: null, reason: "Atlas rapid-transit station data incomplete: 14 stations on 191 line-km (0.07/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 1.5 % is not credible" }
  temp_coldest: { value: 26.2, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 27.6, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 34.2, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 8413206, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 31.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1648「Kuala Lumpur」。面積 1340 km²、2025 年人口 8,413,206 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 1.79 % | 2024 | observed |
| 年平均雲量 | 83.2 % | 1990-2019 | observed |
| 人口加重密度 | 9412 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.4 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 17.0 µg/m³ | 2020 | estimated |
| 年降水量 | 2572 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 欠損 | — | Atlas rapid-transit station data incomplete: 14 stations on 191 line-km (0.07/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 1.5 % is not credible |
| 最寒月の平均気温 | 26.2 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 27.6 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 34.2 % | 2021 | observed |
| 都市圏の人口 | 8413206 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 31.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
