---
type: City
title: "Montreal"
description: "モントリオール（CA）の都市プロファイル。GHS-UCDB 都市圏 3700 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: montreal
name_ja: "モントリオール"
country: CA
region: "Northern America"
lat: 45.5379
lon: -73.6947
boundary:
  source: ghsl-ucdb
  id: 3700
  name: "Montreal"
  area_km2: 1020
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 34.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 62.7, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.29, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 6042, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 15.9, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.98, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 7.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1135, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 19.1, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: -9.12, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 21.5, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 30.5, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 3221844, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 52.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 3700「Montreal」。面積 1020 km²、2025 年人口 3,221,844 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 34.0 % | 2024 | observed |
| 年平均雲量 | 62.7 % | 1990-2019 | observed |
| 文化施設の密度 | 0.29 件/km² | 2026 | estimated |
| 人口加重密度 | 6042 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 15.9 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.98 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 7.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1135 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 19.1 % | 2024 | observed |
| 最寒月の平均気温 | -9.12 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 21.5 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 30.5 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 3221844 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 52.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
