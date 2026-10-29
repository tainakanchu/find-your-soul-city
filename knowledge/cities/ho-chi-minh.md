---
type: City
title: "Ho Chi Minh City"
description: "ホーチミン（VN）の都市プロファイル。GHS-UCDB 都市圏 5239 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: ho-chi-minh
name_ja: "ホーチミン"
country: VN
region: "Eastern and South-Eastern Asia"
lat: 10.8502
lon: 106.7013
boundary:
  source: ghsl-ucdb
  id: 5239
  name: "Ho Chi Minh City"
  area_km2: 1487
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 71.1, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.07, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 27617, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.9, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 27.6, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 27.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1940, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 26.4, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 29.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 22.3, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 14557830, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 35.5, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5239「Ho Chi Minh City」。面積 1487 km²、2025 年人口 14,557,830 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 71.1 % | 1990-2019 | observed |
| 文化施設の密度 | 0.07 件/km² | 2026 | estimated |
| 人口加重密度 | 27617 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.9 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 27.6 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 27.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1940 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 26.4 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 29.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 22.3 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 14557830 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 35.5 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
