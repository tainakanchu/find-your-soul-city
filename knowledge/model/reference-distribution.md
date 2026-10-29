---
type: Reference Distribution
title: 方向型指標の基準分布
description: 人口 1,000,000 人以上の全都市圏（524）での分位点。多いほど良い／少ないほど良い型の指標の 0〜1 変換に使う。
status: generated
tags: [model, reference]
reference_set: "GHS-UCDB R2024A urban centres with GC_POP_TOT_2025 >= 1000000 (524)"
levels: [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
metrics:
  bike_protected: { source: itdp-atlas, n: 524, quantiles: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2619, 0.7663, 1.4679, 2.7564, 4.769, 7.2947, 12.4284, 18.476, 33.8648, 82.2216] }
  culture: { source: osm, n: 530, quantiles: [0.0, 0.0, 0.0086, 0.0159, 0.0248, 0.0338, 0.0453, 0.0566, 0.0686, 0.077, 0.0937, 0.1103, 0.1375, 0.1684, 0.1914, 0.2262, 0.2675, 0.3567, 0.4749, 0.7994, 1.8979] }
  pm25: { source: ghsl-ucdb, n: 524, quantiles: [6.0, 8.0, 9.0, 12.0, 14.0, 15.75, 18.0, 20.0, 22.0, 24.0, 27.0, 30.0, 33.0, 36.0, 40.0, 43.0, 48.0, 54.0, 66.0, 76.0, 116.0] }
  rapid_transit: { source: itdp-atlas, n: 512, quantiles: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7533, 4.9651, 7.8507, 11.3216, 15.2105, 19.8229, 23.9243, 31.1887, 53.9383] }
  tree_share: { source: esa-worldcover, n: 524, quantiles: [0.074, 2.5456, 4.3151, 6.7638, 9.0542, 10.9352, 12.6183, 15.2327, 16.6774, 18.7914, 20.732, 22.4886, 24.5472, 26.8571, 29.3106, 31.2387, 34.3178, 38.4544, 42.163, 49.4867, 90.787] }
  walk_services: { source: itdp-atlas, n: 524, quantiles: [0.0, 1.429, 5.6708, 8.5752, 11.5092, 14.7772, 18.5524, 21.1215, 24.6998, 28.7883, 31.337, 34.9702, 40.6692, 43.0933, 46.7927, 50.267, 53.4264, 58.4302, 61.9185, 66.8759, 77.104] }
# Spearman rank correlation between adopted metrics over the same reference set (pairwise complete).
# Used to share weight between strongly correlated answers (knowledge/model/scoring.md).
correlations:
  bike_protected: { cloud_cover_annual: 0.155, culture: 0.685, density_weighted: -0.338, dewpoint_max_month: -0.385, pm25: -0.587, precip_annual: -0.075, rapid_transit: 0.648, temp_coldest: -0.44, temp_warmest: -0.512, tree_share: 0.209, urban_pop: 0.133, walk_services: 0.441 }
  cloud_cover_annual: { bike_protected: 0.155, culture: 0.107, density_weighted: -0.158, dewpoint_max_month: 0.171, pm25: -0.352, precip_annual: 0.715, rapid_transit: 0.103, temp_coldest: 0.269, temp_warmest: -0.38, tree_share: 0.553, urban_pop: 0.016, walk_services: 0.113 }
  culture: { bike_protected: 0.685, cloud_cover_annual: 0.107, density_weighted: -0.252, dewpoint_max_month: -0.457, pm25: -0.622, precip_annual: -0.111, rapid_transit: 0.616, temp_coldest: -0.332, temp_warmest: -0.491, tree_share: 0.194, urban_pop: 0.105, walk_services: 0.778 }
  density_weighted: { bike_protected: -0.338, cloud_cover_annual: -0.158, culture: -0.252, dewpoint_max_month: 0.255, pm25: 0.465, precip_annual: -0.039, rapid_transit: -0.071, temp_coldest: 0.063, temp_warmest: 0.288, tree_share: -0.211, urban_pop: 0.268, walk_services: -0.208 }
  dewpoint_max_month: { bike_protected: -0.385, cloud_cover_annual: 0.171, culture: -0.457, density_weighted: 0.255, pm25: 0.399, precip_annual: 0.53, rapid_transit: -0.299, temp_coldest: 0.522, temp_warmest: 0.576, tree_share: 0.218, urban_pop: 0.101, walk_services: -0.47 }
  pm25: { bike_protected: -0.587, cloud_cover_annual: -0.352, culture: -0.622, density_weighted: 0.465, dewpoint_max_month: 0.399, precip_annual: -0.086, rapid_transit: -0.387, temp_coldest: 0.115, temp_warmest: 0.612, tree_share: -0.308, urban_pop: 0.082, walk_services: -0.532 }
  precip_annual: { bike_protected: -0.075, cloud_cover_annual: 0.715, culture: -0.111, density_weighted: -0.039, dewpoint_max_month: 0.53, pm25: -0.086, rapid_transit: -0.099, temp_coldest: 0.463, temp_warmest: -0.022, tree_share: 0.562, urban_pop: 0.052, walk_services: -0.099 }
  rapid_transit: { bike_protected: 0.648, cloud_cover_annual: 0.103, culture: 0.616, density_weighted: -0.071, dewpoint_max_month: -0.299, pm25: -0.387, precip_annual: -0.099, temp_coldest: -0.488, temp_warmest: -0.406, tree_share: 0.133, urban_pop: 0.309, walk_services: 0.368 }
  temp_coldest: { bike_protected: -0.44, cloud_cover_annual: 0.269, culture: -0.332, density_weighted: 0.063, dewpoint_max_month: 0.522, pm25: 0.115, precip_annual: 0.463, rapid_transit: -0.488, temp_warmest: 0.358, tree_share: 0.113, urban_pop: 0.074, walk_services: -0.15 }
  temp_warmest: { bike_protected: -0.512, cloud_cover_annual: -0.38, culture: -0.491, density_weighted: 0.288, dewpoint_max_month: 0.576, pm25: 0.612, precip_annual: -0.022, rapid_transit: -0.406, temp_coldest: 0.358, tree_share: -0.208, urban_pop: 0.019, walk_services: -0.43 }
  tree_share: { bike_protected: 0.209, cloud_cover_annual: 0.553, culture: 0.194, density_weighted: -0.211, dewpoint_max_month: 0.218, pm25: -0.308, precip_annual: 0.562, rapid_transit: 0.133, temp_coldest: 0.113, temp_warmest: -0.208, urban_pop: -0.016, walk_services: 0.096 }
  urban_pop: { bike_protected: 0.133, cloud_cover_annual: 0.016, culture: 0.105, density_weighted: 0.268, dewpoint_max_month: 0.101, pm25: 0.082, precip_annual: 0.052, rapid_transit: 0.309, temp_coldest: 0.074, temp_warmest: 0.019, tree_share: -0.016, walk_services: 0.086 }
  walk_services: { bike_protected: 0.441, cloud_cover_annual: 0.113, culture: 0.778, density_weighted: -0.208, dewpoint_max_month: -0.47, pm25: -0.532, precip_annual: -0.099, rapid_transit: 0.368, temp_coldest: -0.15, temp_warmest: -0.43, tree_share: 0.096, urban_pop: 0.086 }
generated: { by: etl/soulcity_etl/reference.py, at: 2026-10-29T03:23:09Z }
---

# 使い方

方向型の指標は、都市の値がこの分布の何パーセンタイルにあたるか（分位点の間は線形補間、同値は中央の順位）を適合度 0〜1 とする。診断の対象都市ではなく世界の大都市圏全体を基準にするので、対象都市を増減してもほかの都市のスコアは変わらない。

`correlations` は同じ基準集合での指標どうしの順位相関（Spearman）。相関の強い条件を両方重視したときに重みを分け合うために使う。

この文書は `pnpm etl` が生成する。手で編集しない。
