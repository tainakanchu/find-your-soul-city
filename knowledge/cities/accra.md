---
type: City
title: "Accra"
description: "アクラ（GH）の都市プロファイル。GHS-UCDB 都市圏 3175 上で集計した実データ。"
status: generated
tags: [city, "Sub-Saharan Africa"]
city_id: accra
name_ja: "アクラ"
country: GH
region: "Sub-Saharan Africa"
lat: 5.6244
lon: -0.1601
boundary:
  source: ghsl-ucdb
  id: 3175
  name: "Accra"
  area_km2: 1121
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:09:44Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 65.2, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.02, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 11714, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.1, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 32.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 697.0, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 25.0, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 28.9, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 4.12, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 5890466, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 41.9, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 3175「Accra」。面積 1121 km²、2025 年人口 5,890,466 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 65.2 % | 1990-2019 | observed |
| 文化施設の密度 | 0.02 件/km² | 2026 | estimated |
| 人口加重密度 | 11714 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.1 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 32.0 µg/m³ | 2020 | estimated |
| 年降水量 | 697.0 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 25.0 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 28.9 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 4.12 % | 2021 | observed |
| 都市圏の人口 | 5890466 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 41.9 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
