---
type: City
title: "Osaka"
description: "大阪（JP）の都市プロファイル。GHS-UCDB 都市圏 4399 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: osaka
name_ja: "大阪"
country: JP
region: "Eastern and South-Eastern Asia"
lat: 34.706
lon: 135.4212
boundary:
  source: ghsl-ucdb
  id: 4399
  name: "Osaka"
  area_km2: 2212
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 6.16, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 60.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.39, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 8376, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 21.7, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 21.6, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 18.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1548, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 18.1, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 5.47, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 29.0, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 16.7, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 2.78, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 12653994, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 71.0, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 4399「Osaka」。面積 2212 km²、2025 年人口 12,653,994 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 6.16 % | 2024 | observed |
| 年平均雲量 | 60.0 % | 1990-2019 | observed |
| 文化施設の密度 | 0.39 件/km² | 2026 | estimated |
| 人口加重密度 | 8376 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 21.7 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 21.6 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 18.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1548 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 18.1 % | 2024 | observed |
| 最寒月の平均気温 | 5.47 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 29.0 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 16.7 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 2.78 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 12653994 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 71.0 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
