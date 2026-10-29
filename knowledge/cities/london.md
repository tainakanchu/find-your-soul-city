---
type: City
title: "London"
description: "ロンドン（GB）の都市プロファイル。GHS-UCDB 都市圏 5816 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: london
name_ja: "ロンドン"
country: GB
region: "Europe"
lat: 51.5373
lon: -0.1275
boundary:
  source: ghsl-ucdb
  id: 5816
  name: "London"
  area_km2: 1649
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 27.1, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 68.7, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.69, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 9905, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 12.7, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 10.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 691.1, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: null, quality: missing, source: itdp-atlas, year: null, reason: "Atlas rapid-transit station data incomplete: 3 stations on 536 line-km (0.01/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 0.5 % is not credible" }
  temp_coldest: { value: 5.22, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 17.8, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 35.1, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 10408332, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 70.3, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 5816「London」。面積 1649 km²、2025 年人口 10,408,332 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 27.1 % | 2024 | observed |
| 年平均雲量 | 68.7 % | 1990-2019 | observed |
| 文化施設の密度 | 0.69 件/km² | 2026 | estimated |
| 人口加重密度 | 9905 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 12.7 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 10.0 µg/m³ | 2020 | estimated |
| 年降水量 | 691.1 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 欠損 | — | Atlas rapid-transit station data incomplete: 3 stations on 536 line-km (0.01/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 0.5 % is not credible |
| 最寒月の平均気温 | 5.22 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 17.8 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 35.1 % | 2021 | observed |
| 都市圏の人口 | 10408332 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 70.3 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
