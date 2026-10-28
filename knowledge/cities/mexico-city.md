---
type: City
title: "Mexico City"
description: "メキシコシティ（MX）の都市プロファイル。GHS-UCDB 都市圏 5402 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: mexico-city
name_ja: "メキシコシティ"
country: MX
region: "Latin America and the Caribbean"
lat: 19.5027
lon: -99.1515
boundary:
  source: ghsl-ucdb
  id: 5402
  name: "Mexico City"
  area_km2: 2134
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T22:03:04Z }
metrics:
  bike_protected: { value: 7.91, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 56.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.39, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 13258, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 11.3, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 22.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: null, quality: missing, source: era5, year: null, reason: "ERA5 の年降水量 1341 mm が近傍の気象観測所（GHCN-M v4）の 881 mm と 1.52 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用" }
  rapid_transit: { value: 21.2, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 13.3, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 18.9, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 13.6, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 17639164, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 41.9, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5402「Mexico City」。面積 2134 km²、2025 年人口 17,639,164 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 7.91 % | 2024 | observed |
| 年平均雲量 | 56.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.39 件/km² | 2026 | estimated |
| 人口加重密度 | 13258 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 11.3 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 22.0 µg/m³ | 2020 | estimated |
| 年降水量 | 欠損 | — | ERA5 の年降水量 1341 mm が近傍の気象観測所（GHCN-M v4）の 881 mm と 1.52 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用 |
| 高速公共交通の近くに住む人口の割合 | 21.2 % | 2024 | observed |
| 最寒月の平均気温 | 13.3 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 18.9 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 13.6 % | 2021 | observed |
| 都市圏の人口 | 17639164 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 41.9 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
