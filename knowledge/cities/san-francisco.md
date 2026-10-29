---
type: City
title: "San Francisco"
description: "サンフランシスコ（US）の都市プロファイル。GHS-UCDB 都市圏 1461 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: san-francisco
name_ja: "サンフランシスコ"
country: US
region: "Northern America"
lat: 37.6052
lon: -122.0608
boundary:
  source: ghsl-ucdb
  id: 1461
  name: "San Francisco"
  area_km2: 1614
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 10.8, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 45.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.44, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 5117, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 12.6, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 3.9, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 9.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 572.8, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 14.9, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 10.5, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 18.9, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 20.2, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 4718349, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 43.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1461「San Francisco」。面積 1614 km²、2025 年人口 4,718,349 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 10.8 % | 2024 | observed |
| 年平均雲量 | 45.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.44 件/km² | 2026 | estimated |
| 人口加重密度 | 5117 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 12.6 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 3.9 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 9.0 µg/m³ | 2020 | estimated |
| 年降水量 | 572.8 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 14.9 % | 2024 | observed |
| 最寒月の平均気温 | 10.5 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 18.9 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 20.2 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 4718349 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 43.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
