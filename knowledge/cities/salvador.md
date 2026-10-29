---
type: City
title: "Salvador"
description: "サルバドール（BR）の都市プロファイル。GHS-UCDB 都市圏 8238 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: salvador
name_ja: "サルバドール"
country: BR
region: "Latin America and the Caribbean"
lat: -12.9257
lon: -38.4146
boundary:
  source: ghsl-ucdb
  id: 8238
  name: "Salvador"
  area_km2: 323.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 7.01, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 51.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.47, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 20111, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 23.0, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 8.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1326, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: null, quality: missing, source: itdp-atlas, year: null, reason: "Atlas rapid-transit station data incomplete: 6 stations on 38 line-km (0.16/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 2.8 % is not credible" }
  temp_coldest: { value: 23.6, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 26.8, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 33.9, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 3305396, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 43.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 8238「Salvador」。面積 323.0 km²、2025 年人口 3,305,396 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 7.01 % | 2024 | observed |
| 年平均雲量 | 51.0 % | 1990-2019 | observed |
| 文化施設の密度 | 0.47 件/km² | 2026 | estimated |
| 人口加重密度 | 20111 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 23.0 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 8.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1326 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 欠損 | — | Atlas rapid-transit station data incomplete: 6 stations on 38 line-km (0.16/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 2.8 % is not credible |
| 最寒月の平均気温 | 23.6 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 26.8 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 33.9 % | 2021 | observed |
| 都市圏の人口 | 3305396 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 43.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
