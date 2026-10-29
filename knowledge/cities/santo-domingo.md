---
type: City
title: "Santo Domingo"
description: "サントドミンゴ（DO）の都市プロファイル。GHS-UCDB 都市圏 1667 上で集計した実データ。"
status: generated
tags: [city, "Latin America and the Caribbean"]
city_id: santo-domingo
name_ja: "サントドミンゴ"
country: DO
region: "Latin America and the Caribbean"
lat: 18.4863
lon: -69.9052
boundary:
  source: ghsl-ucdb
  id: 1667
  name: "Santo Domingo"
  area_km2: 483.0
generated: { by: etl/soulcity_etl/build.py, at: 2026-10-29T19:13:22Z }
metrics:
  bike_protected: { value: 1.7, quality: observed, source: itdp-atlas, year: 2024 }
  cloud_cover_annual: { value: 51.5, quality: observed, source: era5, year: "1990-2019" }
  culture: { value: 0.16, quality: estimated, source: osm, year: 2026 }
  density_weighted: { value: 14271, quality: estimated, source: ghsl-pop, year: 2025 }
  dewpoint_max_month: { value: 23.4, quality: observed, source: era5, year: "1990-2019" }
  flood: { value: 1.01, quality: estimated, source: ghsl-hazard, year: 2025 }
  late_dining: { value: null, quality: missing, source: osm-hours, year: null, reason: "chain/non-chain strata too small for post-stratification (3 chain, 92 non-chain parsed)" }
  late_shops: { value: 33.3, quality: estimated, source: osm-hours, year: 2026 }
  pm25: { value: 16.0, quality: estimated, source: ghsl-ucdb, year: 2020 }
  precip_annual: { value: 1103, quality: observed, source: era5, year: "1990-2019" }
  rapid_transit: { value: 8.19, quality: observed, source: itdp-atlas, year: 2024 }
  sunday_shops: { value: 68.4, quality: estimated, source: osm-hours, year: 2026 }
  sunset_summer: { value: 19.3, quality: estimated, source: daylight, year: 2025 }
  temp_coldest: { value: 23.7, quality: observed, source: era5, year: "1990-2019" }
  temp_warmest: { value: 26.9, quality: observed, source: era5, year: "1990-2019" }
  tree_share: { value: 25.8, quality: observed, source: esa-worldcover, year: 2021 }
  typhoon: { value: 0.67, quality: estimated, source: ghsl-hazard, year: "2004-2016" }
  urban_pop: { value: 4593164, quality: estimated, source: ghsl-ucdb, year: 2025 }
  walk_services: { value: 48.7, quality: observed, source: itdp-atlas, year: 2024 }
---

# 境界

GHS-UCDB R2024A の都市圏（urban centre）ID 1667「Santo Domingo」。面積 483.0 km²、2025 年人口 4,593,164 人。行政市域ではなく、人口密度と連続性で定義された都市圏なので、周辺の市町村を含むことがある。すべての指標をこの範囲で集計している。

# 指標

| 指標 | 値 | 年 | 品質 / 欠損理由 |
| --- | --- | --- | --- |
| 保護自転車道の近くに住む人口の割合 | 1.7 % | 2024 | observed |
| 年平均雲量 | 51.5 % | 1990-2019 | observed |
| 文化施設の密度 | 0.16 件/km² | 2026 | estimated |
| 人口加重密度 | 14271 人/km² | 2025 | estimated |
| 最も蒸す月の露点温度 | 23.4 ℃ | 1990-2019 | observed |
| 洪水の想定範囲に住む人口の割合 | 1.01 % | 2025 | estimated |
| 深夜 23 時に開いている飲食店の割合 | 欠損 | — | chain/non-chain strata too small for post-stratification (3 chain, 92 non-chain parsed) |
| 深夜 23 時に開いている食料品店の割合 | 33.3 % | 2026 | estimated |
| PM2.5 年平均濃度（人口加重） | 16.0 µg/m³ | 2020 | estimated |
| 年降水量 | 1103 mm | 1990-2019 | observed |
| 高速公共交通の近くに住む人口の割合 | 8.19 % | 2024 | observed |
| 日曜の昼に開いている食料品店の割合 | 68.4 % | 2026 | estimated |
| 夏至の日の入り時刻 | 19.3 時刻 | 2025 | estimated |
| 最寒月の平均気温 | 23.7 ℃ | 1990-2019 | observed |
| 最暖月の平均気温 | 26.9 ℃ | 1990-2019 | observed |
| 樹木被覆率 | 25.8 % | 2021 | observed |
| 熱帯低気圧（台風・ハリケーン）の被災回数 | 0.67 回/年 | 2004-2016 | estimated |
| 都市圏の人口 | 4593164 人 | 2025 | estimated |
| 徒歩圏に医療・教育がある人口の割合 | 48.7 % | 2024 | observed |

この文書は `pnpm etl` が生成する。手で編集しない。
