---
type: City
title: "Helsinki"
description: "ヘルシンキ（FI）の都市プロファイル。GHS-UCDB 都市圏 572 上で集計した実データ。"
status: generated
tags: [city, "Europe"]
city_id: helsinki
name_ja: "ヘルシンキ"
country: FI
region: "Europe"
lat: 60.2384
lon: 24.9313
boundary:
  source: ghsl-ucdb
  id: 572
  name: "Helsinki"
  area_km2: 381.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 78.5, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 69.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.8, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 4877, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 12.6, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 5.17, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 8.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 734.5, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 22.9, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: -4.84, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 18.1, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 50.2, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 1001125, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 47.6, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 572「Helsinki」。面積 381.0 km²、2025 年人口 1,001,125 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 78.5 % | 2024 | observed |
| 年平均雲量 | 69.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.8 件/km² | 2026 | estimated |
| 人口加重密度 | 4877 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 12.6 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 5.17 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 8.0 µg/m³ | 2020 | estimated |
| 年降水量 | 734.5 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 22.9 % | 2024 | observed |
| 最寒月の平均気温 | -4.84 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 18.1 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 50.2 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 1001125 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 47.6 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
