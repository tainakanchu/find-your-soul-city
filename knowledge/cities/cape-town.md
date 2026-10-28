---
type: City
title: "Cape Town"
description: "ケープタウン（ZA）の都市プロファイル。GHS-UCDB 都市圏 431 上で集計した実データ。"
status: generated
tags: [city, "Sub-Saharan Africa"]
city_id: cape-town
name_ja: "ケープタウン"
country: ZA
region: "Sub-Saharan Africa"
lat: -33.9536
lon: 18.5874
boundary:
  source: ghsl-ucdb
  id: 431
  name: "Cape Town"
  area_km2: 695.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T22:03:04Z }
metrics:
  bike_protected: { value: 0.74, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 40.2, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.1, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 13518, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 14.6, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 6.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: null, quality: missing, source: era5, year: null, reason: "ERA5 の年降水量 793 mm が近傍の気象観測所（GHCN-M v4）の 500 mm と 1.59 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 12.9, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 21.6, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 11.6, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 4338251, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 30.3, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 431「Cape Town」。面積 695.0 km²、2025 年人口 4,338,251 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.74 % | 2024 | observed |
| 年平均雲量 | 40.2 % | 1990-2019 | observed |
| 文化施設の密度 | 0.1 件/km² | 2026 | estimated |
| 人口加重密度 | 13518 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 14.6 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 6.0 µg/m³ | 2020 | estimated |
| 年降水量 | 欠損 | — | ERA5 の年降水量 793 mm が近傍の気象観測所（GHCN-M v4）の 500 mm と 1.59 倍ずれており、許容範囲（×0.67〜×1.5）を外れるため不採用 |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 12.9 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 21.6 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 11.6 % | 2021 | observed |
| 都市圏の人口 | 4338251 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 30.3 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
