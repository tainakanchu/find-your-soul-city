---
type: City
title: "Lagos"
description: "ラゴス（NG）の都市プロファイル。GHS-UCDB 都市圏 1289 上で集計した実データ。"
status: generated
tags: [city, "Sub-Saharan Africa"]
city_id: lagos
name_ja: "ラゴス"
country: NG
region: "Sub-Saharan Africa"
lat: 6.6416
lon: 3.2913
boundary:
  source: ghsl-ucdb
  id: 1289
  name: "Lagos"
  area_km2: 1199
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T04:27:29Z }
metrics:
  bike_protected: { value: 0.0, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 70.4, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.02, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 24035, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 24.7, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 11.1, quality: estimated, source: ghsl-hazard, year: 2025 }
  pm25: { value: 36.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1688, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 2.34, quality: observed, source: itdp-atlas, year: 2024 }
  temp_coldest: { value: 24.8, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 28.1, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 12.8, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.0, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 12846045, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 7.74, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1289「Lagos」。面積 1199 km²、2025 年人口 12,846,045 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 0.0 % | 2024 | observed |
| 年平均雲量 | 70.4 % | 1990-2019 | observed |
| 文化施設の密度 | 0.02 件/km² | 2026 | estimated |
| 人口加重密度 | 24035 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 24.7 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 11.1 % | 2025 | estimated |
| PM2.5 年平均濃度（人口加重） | 36.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1688 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 2.34 % | 2024 | observed |
| 最寒月の平均気温 | 24.8 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 28.1 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 12.8 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.0 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 12846045 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 7.74 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
