---
type: Data Source
title: GHS-UCDB R2024A 災害曝露（洪水・熱帯低気圧）
description: GHS-UCDB の EXPOSURE / HAZARD_RISK テーマから、洪水の想定範囲に住む人口の割合と熱帯低気圧の被災回数。CC BY 4.0。
status: verified
resource: https://human-settlement.emergency.copernicus.eu/ucdb2024Overview.php
tags: [data-source, ghsl, hazard]
source_id: ghsl-hazard
adoption: adopted
provider: European Commission, Joint Research Centre (JRC)
version: "GHS-UCDB R2024A V1.2（上流: GloFAS 洪水 Baugh et al. 2024、JRC 沿岸洪水 Vousdoukas et al. 2018、MYRIAD-HES Claassen et al. 2023）"
geo_granularity: 都市圏（urban centre）ポリゴン
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
license_status: verified
attribution: "GHS-UCDB R2024A © European Union (CC BY 4.0), doi:10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd. Flood hazard: JRC GloFAS (Baugh et al. 2024) and JRC coastal flood maps (Vousdoukas et al. 2018); tropical cyclone occurrence: MYRIAD-HES (Claassen et al. 2023, CC BY 4.0, doi:10.5281/zenodo.8269680). 割合の合成と年あたりの換算は本プロジェクトが算出。"
etl_module: etl/soulcity_etl/hazard.py
methodology: etl/notes/ghsl-hazard.md
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 用途

[洪水](/metrics/flood.md)、[熱帯低気圧](/metrics/typhoon.md)。設問「自然災害が少ない街」でまとめて使う。

# ライセンス（原文で確認済み）

- GHS-UCDB: CC BY 4.0（GHSL `copyright.txt`）。
- 河川洪水（GloFAS）: 同じフォルダの `copyright.txt` は CC BY 4.0、`README.txt` は ODbL 1.0 と記載が食い違う。どちらも表示を条件に再利用可。
- 沿岸洪水（JRC LISCOAST）: `copyright.txt` は CC BY 4.0。UCDB が使ったサブフォルダは特定できていない。
- MYRIAD-HES: CC BY 4.0（Zenodo 8269680）。
- 地震（GEM 2023.1）は CC BY-NC-SA 4.0（非商用・継承）で、本プロジェクトの ODbL のデータと両立しないため使わない（[地震](/metrics/quake.md)）。

# 注意点

- 堤防などの防護は考慮しない。「防護がなかった場合の浸水想定」で、災害リスクそのものではない（例: アムステルダムは沿岸洪水の想定範囲に 70%）。
- 熱帯低気圧は回数だけで強さを含まない。内陸で弱まった後の通過も数える（例: メキシコシティ）。
- UCDB の熱帯低気圧の風（EX_*_S1P/S3P）は値が壊れているため使わない（東京・香港が 0、人口の 100% を超える値が多数）。
