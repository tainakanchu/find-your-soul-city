---
type: Data Source
title: ESA WorldCover 10 m 2021 v200
description: 10 m 解像度の土地被覆。都市圏内の樹木被覆率に使う。CC BY 4.0。
status: verified
resource: https://esa-worldcover.org/en/data-access
tags: [data-source, land-cover]
source_id: esa-worldcover
adoption: adopted
provider: European Space Agency（WorldCover consortium）
version: 2021 v200, doi:10.5281/zenodo.7254221
geo_granularity: 10 m ラスタ
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
license_status: verified
attribution: "© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium. Zanaga, D. et al. (2022), doi:10.5281/zenodo.7254221. 都市圏ごとの割合は本プロジェクトが算出。"
etl_module: etl/soulcity_etl/worldcover.py
methodology: etl/notes/esa-worldcover.md
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 用途

[樹木被覆率](/metrics/tree-share.md)。

# ライセンス（原文で確認済み）

"The ESA WorldCover product is provided free of charge, without restriction of use. For the full license information see the Creative Commons Attribution 4.0 International License."

# 注意点

全体精度 76.7 ± 0.5%（v200 検証報告）。樹木の利用者精度 80.0%、市街地 65.9%。高密度な中心部では樹木と市街地の混同がありうる。
