---
type: City
title: "Buenos Aires"
description: "ブエノスアイレス（AR）の都市プロファイル。GHS-UCDB 都市圏 4443 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: buenos-aires
name_ja: "ブエノスアイレス"
country: AR
region: "Latin America and the Caribbean"
lat: -34.6537
lon: -58.5812
boundary:
  source: ghsl-ucdb
  id: 4443
  name: "Buenos Aires"
  area_km2: 2186
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 9.99, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 48.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.29, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 9784, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 17.5, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 14.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1059, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 9.35, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 9.89, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 23.7, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 20.9, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 14179912, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 66.8, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 4443「Buenos Aires」。面積 2186 km²、2025 年人口 14,179,912 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 9.99 % | 2024 | observed |
| 年平均雲量 | 48.0 % | 1990-2019 | observed |
| 文化施設の密度 | 0.29 件/km² | 2026 | estimated |
| 人口加重密度 | 9784 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 17.5 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 14.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1059 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 9.35 % | 2024 | observed |
| 最寒月の平均気温 | 9.89 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 23.7 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 20.9 % | 2021 | observed |
| 都市圏の人口 | 14179912 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 66.8 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
