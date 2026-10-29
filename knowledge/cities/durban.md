---
type: City
title: "Durban"
description: "ダーバン（ZA）の都市プロファイル。GHS-UCDB 都市圏 4787 上で集計した実データ。"
status: generated
tags: [city, "Sub-Saharan Africa"]
city_id: durban
name_ja: "ダーバン"
country: ZA
region: "Sub-Saharan Africa"
lat: -29.8603
lon: 30.8247
boundary:
  source: ghsl-ucdb
  id: 4787
  name: "Durban"
  area_km2: 807.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 0.01, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 47.8, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.02, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 7459, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 20.4, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 0.33, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 16.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 898.4, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 16.8, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 24.4, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 43.8, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 3270868, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 5.98, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 4787「Durban」。面積 807.0 km²、2025 年人口 3,270,868 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.01 % | 2024 | observed |
| 年平均雲量 | 47.8 % | 1990-2019 | observed |
| 文化施設の密度 | 0.02 件/km² | 2026 | estimated |
| 人口加重密度 | 7459 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 20.4 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 0.33 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 16.0 µg/m³ | 2020 | estimated |
| 年降水量 | 898.4 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 最寒月の平均気温 | 16.8 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 24.4 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 43.8 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 3270868 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 5.98 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
