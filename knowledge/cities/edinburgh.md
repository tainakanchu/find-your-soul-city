---
type: City
title: "Edinburgh"
description: "エディンバラ（GB）の都市プロファイル。GHS-UCDB 都市圏 2186 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: edinburgh
name_ja: "エディンバラ"
country: GB
region: "Europe"
lat: 55.9493
lon: -3.1707
boundary:
  source: ghsl-ucdb
  id: 2186
  name: "Edinburgh"
  area_km2: 130.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-28T22:03:04Z }
metrics:
  bike_protected: { value: 37.9, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 73.0, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 1.06, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 6458, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 11.3, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 7.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 872.8, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 10.1, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 4.99, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 15.5, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 31.8, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 530165, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 68.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 2186「Edinburgh」。面積 130.0 km²、2025 年人口 530,165 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 37.9 % | 2024 | observed |
| 年平均雲量 | 73.0 % | 1990-2019 | observed |
| 文化施設の密度 | 1.06 件/km² | 2026 | estimated |
| 人口加重密度 | 6458 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 11.3 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 7.0 µg/m³ | 2020 | estimated |
| 年降水量 | 872.8 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 10.1 % | 2024 | observed |
| 最寒月の平均気温 | 4.99 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 15.5 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 31.8 % | 2021 | observed |
| 都市圏の人口 | 530165 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 68.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
