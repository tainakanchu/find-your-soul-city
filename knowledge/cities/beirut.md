---
type: City
title: "Beirut"
description: "ベイルート（LB）の都市プロファイル。GHS-UCDB 都市圏 458 上で集計した実データ。"
status: generated
tags: [city, "Northern Africa and Western Asia"]
city_id: beirut
name_ja: "ベイルート"
country: LB
region: "Northern Africa and Western Asia"
lat: 33.8972
lon: 35.5244
boundary:
  source: ghsl-ucdb
  id: 458
  name: "Beirut"
  area_km2: 199.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 29.7, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.38, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 20091, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 19.1, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.06, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 33.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 636.0, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 11.3, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 27.6, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 37.4, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 1538386, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 46.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 458「Beirut」。面積 199.0 km²、2025 年人口 1,538,386 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 29.7 % | 1990-2019 | observed |
| 文化施設の密度 | 0.38 件/km² | 2026 | estimated |
| 人口加重密度 | 20091 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 19.1 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.06 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 33.0 µg/m³ | 2020 | estimated |
| 年降水量 | 636.0 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 11.3 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 27.6 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 37.4 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 1538386 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 46.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
