---
type: Data Source
title: GHS Urban Centre Database R2024A
description: 都市圏ポリゴン（全指標の共通境界）、人口、PM2.5 などの都市圏集計値。CC BY 4.0。
status: verified
resource: https://human-settlement.emergency.copernicus.eu/ucdb2024Overview.php
tags: [data-source, ghsl]
source_id: ghsl-ucdb
adoption: adopted
provider: European Commission, Joint Research Centre (JRC)
version: R2024A V1.2（2026-05-15 更新）, doi:10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd
geo_granularity: 都市圏（urban centre）ポリゴン、11,422 件
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
license_status: verified
attribution: "GHS-UCDB R2024A © European Union, 1995-2026 (CC BY 4.0). Mari Rivero, I. et al. (2024), doi:10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd. 集計・派生値は本プロジェクトが算出。"
etl_module: etl/soulcity_etl/ghsl.py
methodology: etl/notes/ghsl-ucdb.md
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 用途

- **都市の定義**: 本プロジェクトの「都市」は GHS-UCDB の都市圏ポリゴン 1 つ。すべての指標をこの範囲で集計するか、同じ ID の範囲で算出された値だけを使う（[境界の統一](/decisions/boundary-ucdb.md)）。
- 指標: [都市圏の人口](/metrics/urban-pop.md)、[PM2.5](/metrics/pm25.md)。

# ライセンス（原文で確認済み）

FTP の `copyright.txt`: "Any copyright and/or sui generis right on the dataset is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence. Reuse is allowed provided appropriate credit is given and any changes are indicated."

PM2.5 列（EM_PM2_CON）の上流は WUSTL ACAG SatPM2.5 V6.GL.02.02。ACAG は現行の V6.GL.02.04 と V5.GL.05.02 を CC BY 4.0 と明記しているが、V6.GL.02.02 そのものの条件は掲載がない。本プロジェクトが受け取っているのは JRC が CC BY 4.0 で公開した UCDB の値であり、帰属表示に ACAG（Shen et al. 2024）を併記する。

# 注意点

- 2025 年の人口は観測ではなく、GHSL が UN WPP2022 の推計に合わせた推定値（`quality: estimated`）。
- 都市圏は行政市域と一致しない。東京は横浜・川崎・さいたま・千葉を含み、大阪は神戸・京都を含む。京都は単独で扱えないため対象外。
- 香港の国名は UCDB では China。

詳細な列辞書・検証は [etl/notes/ghsl-ucdb.md](../../etl/notes/ghsl-ucdb.md)。
