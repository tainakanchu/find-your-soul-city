---
type: Decision Record
title: 対象 86 都市の選定
description: P1 の 30 都市に地域・気候・規模の分散のため 56 都市を加えた。正規化は対象都市に依存させない。
status: accepted
tags: [decision, cities]
decision_status: accepted
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 判断

`etl/config/cities.yaml` の 86 都市。P1 の 30 都市に、各地域の主要都市と気候・規模の幅を広げる都市を加えた。選定は知名度に偏っており、地域の内訳は欧州 23・東/東南アジア 17・北米 11・中南米 10・北アフリカ/西アジア 7・中央/南アジア 7・サハラ以南 7・豪州/NZ 4。

# 選定の影響を抑える仕組み

- 方向型指標の正規化は対象都市ではなく、人口 100 万人以上の全 524 都市圏の分布で行う（[スコア仕様](/model/scoring.md)）。対象都市を増減しても他都市のスコアは変わらない。
- 地域別の 1 位率を [検証](/reports/validation.md) で監視する。

# 除外

- 京都: GHS-UCDB では大阪の都市圏に含まれる。
