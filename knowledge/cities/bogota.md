---
type: City
title: "Bogota"
description: "ボゴタ（CO）の都市プロファイル。GHS-UCDB 都市圏 3881 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: bogota
name_ja: "ボゴタ"
country: CO
region: "Latin America and the Caribbean"
lat: 4.6281
lon: -74.1344
boundary:
  source: ghsl-ucdb
  id: 3881
  name: "Bogota"
  area_km2: 534.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 41.8, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 87.9, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.46, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 27679, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 13.0, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 4.48, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 22.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: null, quality: missing, source: era5, year: null, reason: "ERA5 の年降水量 2699 mm が近傍の気象観測所（GHCN-M v4）の 859 mm と 3.14 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用" }
  rapid_transit: { value: 22.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 13.5, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 15.5, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 12.6, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 10419361, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 69.8, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 3881「Bogota」。面積 534.0 km²、2025 年人口 10,419,361 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 41.8 % | 2024 | observed |
| 年平均雲量 | 87.9 % | 1990-2019 | observed |
| 文化施設の密度 | 0.46 件/km² | 2026 | estimated |
| 人口加重密度 | 27679 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 13.0 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 4.48 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 22.0 µg/m³ | 2020 | estimated |
| 年降水量 | 欠損 | — | ERA5 の年降水量 2699 mm が近傍の気象観測所（GHCN-M v4）の 859 mm と 3.14 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用 |
| 高速公共交通の近くに住む人口の割合 | 22.0 % | 2024 | observed |
| 最寒月の平均気温 | 13.5 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 15.5 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 12.6 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 10419361 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 69.8 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
