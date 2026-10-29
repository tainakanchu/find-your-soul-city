---
type: City
title: "Rio de Janeiro"
description: "リオデジャネイロ（BR）の都市プロファイル。GHS-UCDB 都市圏 7799 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: rio-de-janeiro
name_ja: "リオデジャネイロ"
country: BR
region: "Latin America and the Caribbean"
lat: -22.8003
lon: -43.3603
boundary:
  source: ghsl-ucdb
  id: 7799
  name: "Rio de Janeiro"
  area_km2: 1285
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:16:02Z }
metrics:
  bike_protected: { value: 4.3, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 60.2, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.25, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 14563, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 22.0, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 16.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1398, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 10.4, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 20.9, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 27.6, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 30.7, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 9853693, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 42.2, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 7799「Rio de Janeiro」。面積 1285 km²、2025 年人口 9,853,693 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 4.3 % | 2024 | observed |
| 年平均雲量 | 60.2 % | 1990-2019 | observed |
| 文化施設の密度 | 0.25 件/km² | 2026 | estimated |
| 人口加重密度 | 14563 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 22.0 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 16.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1398 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 10.4 % | 2024 | observed |
| 最寒月の平均気温 | 20.9 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 27.6 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 30.7 % | 2021 | observed |
| 都市圏の人口 | 9853693 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 42.2 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
