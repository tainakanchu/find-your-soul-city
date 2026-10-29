---
type: City
title: "Kampala"
description: "カンパラ（UG）の都市プロファイル。GHS-UCDB 都市圏 1711 上で集計した実データ。"
status: generated
tags: [city, "Sub-Saharan Africa"]
city_id: kampala
name_ja: "カンパラ"
country: UG
region: "Sub-Saharan Africa"
lat: 0.2588
lon: 32.5377
boundary:
  source: ghsl-ucdb
  id: 1711
  name: "Kampala"
  area_km2: 810.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 73.4, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.06, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 9974, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 19.2, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.01, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 83.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1753, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 21.2, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 23.0, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 28.0, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 5177878, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 41.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1711「Kampala」。面積 810.0 km²、2025 年人口 5,177,878 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 73.4 % | 1990-2019 | observed |
| 文化施設の密度 | 0.06 件/km² | 2026 | estimated |
| 人口加重密度 | 9974 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 19.2 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.01 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 83.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1753 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 21.2 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 23.0 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 28.0 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 5177878 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 41.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
