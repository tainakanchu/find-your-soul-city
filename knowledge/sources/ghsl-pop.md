---
type: Data Source
title: GHS-POP R2023A（1 km 人口グリッド）
description: 人口加重密度の算出に使う 2025 年の 1 km 人口グリッド。CC BY 4.0。
status: verified
resource: https://human-settlement.emergency.copernicus.eu/ghs_pop2023.php
tags: [data-source, ghsl]
source_id: ghsl-pop
adoption: adopted
provider: European Commission, Joint Research Centre (JRC)
version: R2023A V1-0, epoch 2025, 1 km, Mollweide (ESRI:54009), doi:10.2905/2FF68A52-5B5B-4A22-8F40-C41DA8332CFE
geo_granularity: 1 km グリッド（UCDB ポリゴンと同じグリッドに整列）
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
license_status: verified
attribution: "GHS-POP R2023A © European Union (CC BY 4.0). Schiavina, M. et al. (2023), doi:10.2905/2FF68A52-5B5B-4A22-8F40-C41DA8332CFE. 人口加重密度は本プロジェクトが算出。"
etl_module: etl/soulcity_etl/ghsl.py
methodology: etl/notes/ghsl-ucdb.md
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 用途

[人口加重密度](/metrics/density.md)。UCDB ポリゴンの頂点は 1 km グリッドに乗っており、ポリゴン内のセル人口の合計は 86 都市すべてで UCDB の人口と一致した（比 1.000000）。

# ライセンス

GHSL 共通の `copyright.txt`（CC BY 4.0）。[GHS-UCDB](/sources/ghsl-ucdb.md) と同じ。

# 注意点

2025 年は UN の推計に合わせた推定値。
