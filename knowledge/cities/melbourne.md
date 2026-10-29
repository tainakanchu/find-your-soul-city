---
type: City
title: "Melbourne"
description: "メルボルン（AU）の都市プロファイル。GHS-UCDB 都市圏 1747 上で集計した実データ。"
status: generated
tags: [city, "Australia and New Zealand"]
city_id: melbourne
name_ja: "メルボルン"
country: AU
region: "Australia and New Zealand"
lat: -37.8483
lon: 145.0371
boundary:
  source: ghsl-ucdb
  id: 1747
  name: "Melbourne"
  area_km2: 1611
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 38.5, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 57.8, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.2, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 4139, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 12.4, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 13.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 654.9, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: null, quality: missing, source: itdp-atlas, year: null, reason: "Atlas rapid-transit station data incomplete: 4 stations on 559 line-km (0.01/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 1.0 % is not credible" }
  temp_coldest: { value: 9.59, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 19.7, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 29.5, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 4010658, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 53.2, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1747「Melbourne」。面積 1611 km²、2025 年人口 4,010,658 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 38.5 % | 2024 | observed |
| 年平均雲量 | 57.8 % | 1990-2019 | observed |
| 文化施設の密度 | 0.2 件/km² | 2026 | estimated |
| 人口加重密度 | 4139 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 12.4 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 13.0 µg/m³ | 2020 | estimated |
| 年降水量 | 654.9 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 欠損 | — | Atlas rapid-transit station data incomplete: 4 stations on 559 line-km (0.01/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 1.0 % is not credible |
| 最寒月の平均気温 | 9.59 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 19.7 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 29.5 % | 2021 | observed |
| 都市圏の人口 | 4010658 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 53.2 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
