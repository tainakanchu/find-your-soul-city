---
type: City
title: "Lahore"
description: "ラホール（PK）の都市プロファイル。GHS-UCDB 都市圏 7794 上で集計した実データ。"
status: generated
tags: [city, "Central and Southern Asia"]
city_id: lahore
name_ja: "ラホール"
country: PK
region: "Central and Southern Asia"
lat: 31.535
lon: 74.3591
boundary:
  source: ghsl-ucdb
  id: 7794
  name: "Lahore"
  area_km2: 898.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 31.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.06, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 26759, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 25.6, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 11.7, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 69.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 684.8, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 5.72, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 12.2, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 33.5, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 7.65, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 14305060, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 26.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 7794「Lahore」。面積 898.0 km²、2025 年人口 14,305,060 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 31.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.06 件/km² | 2026 | estimated |
| 人口加重密度 | 26759 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 25.6 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 11.7 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 69.0 µg/m³ | 2020 | estimated |
| 年降水量 | 684.8 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 5.72 % | 2024 | observed |
| 最寒月の平均気温 | 12.2 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 33.5 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 7.65 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 14305060 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 26.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
