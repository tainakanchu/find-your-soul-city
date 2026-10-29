---
type: City
title: "Bengaluru"
description: "ベンガルール（IN）の都市プロファイル。GHS-UCDB 都市圏 9558 上で集計した実データ。"
status: generated
tags: [city, "Central and Southern Asia"]
city_id: bengaluru
name_ja: "ベンガルール"
country: IN
region: "Central and Southern Asia"
lat: 12.9911
lon: 77.6071
boundary:
  source: ghsl-ucdb
  id: 9558
  name: "Bengaluru"
  area_km2: 1008
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 0.55, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 63.8, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.32, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 46588, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 19.8, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 34.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 964.8, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: null, quality: missing, source: itdp-atlas, year: null, reason: "Atlas rapid-transit station data incomplete: 10 stations on 71 line-km (0.14/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 4.4 % is not credible" }
  temp_coldest: { value: 21.0, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 27.3, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 18.4, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 15178533, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 54.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 9558「Bengaluru」。面積 1008 km²、2025 年人口 15,178,533 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.55 % | 2024 | observed |
| 年平均雲量 | 63.8 % | 1990-2019 | observed |
| 文化施設の密度 | 0.32 件/km² | 2026 | estimated |
| 人口加重密度 | 46588 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 19.8 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 34.0 µg/m³ | 2020 | estimated |
| 年降水量 | 964.8 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 欠損 | — | Atlas rapid-transit station data incomplete: 10 stations on 71 line-km (0.14/km < 0.2/km); People Near Rapid Transport is computed from stations, so the published 4.4 % is not credible |
| 最寒月の平均気温 | 21.0 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 27.3 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 18.4 % | 2021 | observed |
| 都市圏の人口 | 15178533 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 54.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
