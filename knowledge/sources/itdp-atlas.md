---
type: Data Source
title: ITDP Atlas of Sustainable City Transport
description: 徒歩圏の生活サービス・保護自転車道・高速公共交通への近接人口割合。ODbL 1.0。
status: verified
resource: https://atlas.itdp.org/
tags: [data-source, mobility, odbl]
source_id: itdp-atlas
adoption: adopted
provider: Institute for Transportation and Development Policy (ITDP)
version: GitHub release ITDP/atlas update_2024（データ年 2024、資産日付 2025-01-10）
geo_granularity: GHS-UCDB R2024A 都市圏（ID 一致・IoU ≥ 0.9999 を確認）
license: ODbL-1.0
license_url: https://opendatacommons.org/licenses/odbl/1-0/
license_status: verified
attribution: "Contains information from the Atlas of Sustainable City Transport (ITDP, atlas.itdp.org, release update_2024), which is made available under the Open Database License (ODbL). Based on OpenStreetMap data © OpenStreetMap contributors."
etl_module: etl/soulcity_etl/itdp.py
methodology: etl/notes/itdp-atlas.md
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 用途

[徒歩圏の生活サービス](/metrics/walk-services.md)、[保護自転車道](/metrics/bike-protected.md)、[高速公共交通](/metrics/rapid-transit.md)。

# 取得経路

Shiny アプリではなく、ITDP 自身が GitHub release として公開している `data_final` から、必要な都市のファイルだけを HTTP Range で取り出し、CRC を検証して読む。

# ライセンス（原文で確認済み）

<https://atlas.itdp.org/about/about_data.html>: "The data in the Atlas is made available under the Open Database License". 商用利用・再配布は可能。義務は (1) 表示（§4.3）、(2) 派生データベースを公開するなら ODbL で提供（§4.4 share-alike）。本プロジェクトは都市データ一式を ODbL で提供する（[データのライセンス](/decisions/data-license.md)）。

# 注意点

- OSM の登録率に依存し、南半球・低所得国の生活サービス近接は過小評価の可能性がある（例: ラゴスの医療施設は 96 地点）。
- 内部整合性の検査で不合格だった値は欠損扱い（ロンドン等の高速交通：駅データ不足）。
- レイキャビクは人口 50 万人未満で対象外。
