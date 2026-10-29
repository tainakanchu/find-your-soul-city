---
type: City
title: "Yangon"
description: "ヤンゴン（MM）の都市プロファイル。GHS-UCDB 都市圏 5029 上で集計した実データ。"
status: generated
tags: [city, "Eastern and South-Eastern Asia"]
city_id: yangon
name_ja: "ヤンゴン"
country: MM
region: "Eastern and South-Eastern Asia"
lat: 16.9003
lon: 96.1478
boundary:
  source: ghsl-ucdb
  id: 5029
  name: "Yangon"
  area_km2: 545.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 57.8, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.12, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 19364, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 25.3, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 28.4, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 36.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 2393, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 24.5, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 31.6, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 40.3, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.11, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 6190958, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 48.9, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5029「Yangon」。面積 545.0 km²、2025 年人口 6,190,958 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 57.8 % | 1990-2019 | observed |
| 文化施設の密度 | 0.12 件/km² | 2026 | estimated |
| 人口加重密度 | 19364 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 25.3 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 28.4 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 36.0 µg/m³ | 2020 | estimated |
| 年降水量 | 2393 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 24.5 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 31.6 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 40.3 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.11 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 6190958 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 48.9 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
