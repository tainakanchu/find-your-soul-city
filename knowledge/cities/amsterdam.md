---
type: City
title: "Amsterdam"
description: "アムステルダム（NL）の都市プロファイル。GHS-UCDB 都市圏 1590 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: amsterdam
name_ja: "アムステルダム"
country: NL
region: "Europe"
lat: 52.3714
lon: 4.8893
boundary:
  source: ghsl-ucdb
  id: 1590
  name: "Amsterdam"
  area_km2: 308.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T02:11:09Z }
metrics:
  bike_protected: { value: 66.3, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 66.9, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 1.22, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 7257, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 14.1, quality: observed, source: era5, year: "1990-2019" }
  pm25: { value: 8.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 927.5, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 16.5, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 4.17, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 17.7, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 25.5, quality: observed, source: esa-worldcover, year: 2021 }
  urban_pop: { value: 1223407, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 52.4, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1590「Amsterdam」。面積 308.0 km²、2025 年人口 1,223,407 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 66.3 % | 2024 | observed |
| 年平均雲量 | 66.9 % | 1990-2019 | observed |
| 文化施設の密度 | 1.22 件/km² | 2026 | estimated |
| 人口加重密度 | 7257 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 14.1 ℃ | 1990-2019 | observed |
| PM2.5 年平均濃度（人口加重） | 8.0 µg/m³ | 2020 | estimated |
| 年降水量 | 927.5 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 16.5 % | 2024 | observed |
| 最寒月の平均気温 | 4.17 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 17.7 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 25.5 % | 2021 | observed |
| 都市圏の人口 | 1223407 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 52.4 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
