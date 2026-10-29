---
type: City
title: "Oslo"
description: "オスロ（NO）の都市プロファイル。GHS-UCDB 都市圏 828 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: oslo
name_ja: "オスロ"
country: NO
region: "Europe"
lat: 59.8822
lon: 10.7763
boundary:
  source: ghsl-ucdb
  id: 828
  name: "Oslo"
  area_km2: 244.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 50.4, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 67.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.71, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 5608, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 11.1, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 6.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1016, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 42.8, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: -3.21, quality: estimated, source: era5, year: "1990-2019" }
  temp_warmest: { value: 17.8, quality: estimated, source: era5, year: "1990-2019" }
  tree_share: { value: 53.5, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 889573, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 67.5, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 828「Oslo」。面積 244.0 km²、2025 年人口 889,573 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 50.4 % | 2024 | observed |
| 年平均雲量 | 67.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.71 件/km² | 2026 | estimated |
| 人口加重密度 | 5608 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 11.1 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 6.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1016 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 42.8 % | 2024 | observed |
| 最寒月の平均気温 | -3.21 ℃ | 1990-2019 | estimated |
| 最暖月の平均気温 | 17.8 ℃ | 1990-2019 | estimated |
| 樹木被覆率 | 53.5 % | 2021 | observed |
| 都市圏の人口 | 889573 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 67.5 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
