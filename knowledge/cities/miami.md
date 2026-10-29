---
type: City
title: "Miami"
description: "マイアミ（US）の都市プロファイル。GHS-UCDB 都市圏 7168 上で集計した実データ。"
status: generated
tags: [city, "Northern America"]
city_id: miami
name_ja: "マイアミ"
country: US
region: "Northern America"
lat: 26.213
lon: -80.1905
boundary:
  source: ghsl-ucdb
  id: 7168
  name: "Miami"
  area_km2: 2784
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 3.81, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 53.6, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.11, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 3306, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 23.9, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 7.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1206, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 1.93, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 20.0, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 27.9, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 20.9, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 5733042, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 20.5, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 7168「Miami」。面積 2784 km²、2025 年人口 5,733,042 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 3.81 % | 2024 | observed |
| 年平均雲量 | 53.6 % | 1990-2019 | observed |
| 文化施設の密度 | 0.11 件/km² | 2026 | estimated |
| 人口加重密度 | 3306 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 23.9 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 7.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1206 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 1.93 % | 2024 | observed |
| 最寒月の平均気温 | 20.0 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 27.9 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 20.9 % | 2021 | observed |
| 都市圏の人口 | 5733042 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 20.5 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
