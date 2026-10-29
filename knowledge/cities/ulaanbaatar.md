---
type: City
title: "Ulaanbaatar"
description: "ウランバートル（MN）の都市プロファイル。GHS-UCDB 都市圏 337 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: ulaanbaatar
name_ja: "ウランバートル"
country: MN
region: "Eastern and South-Eastern Asia"
lat: 47.9346
lon: 106.8893
boundary:
  source: ghsl-ucdb
  id: 337
  name: "Ulaanbaatar"
  area_km2: 235.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 3.48, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 48.2, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.25, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 10403, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 10.1, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 1.59, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 41.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 359.9, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: -21.9, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 18.2, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 1.45, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 1634097, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 41.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 337「Ulaanbaatar」。面積 235.0 km²、2025 年人口 1,634,097 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 3.48 % | 2024 | observed |
| 年平均雲量 | 48.2 % | 1990-2019 | observed |
| 文化施設の密度 | 0.25 件/km² | 2026 | estimated |
| 人口加重密度 | 10403 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 10.1 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 1.59 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 41.0 µg/m³ | 2020 | estimated |
| 年降水量 | 359.9 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | -21.9 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 18.2 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 1.45 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 1634097 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 41.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
