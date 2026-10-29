---
type: Data Source
title: OpenStreetMap
description: 文化施設の数え上げ。QLever の osm-planet SPARQL（planet 2026-09-21）から取得。ODbL 1.0。
status: verified
resource: https://www.openstreetmap.org/copyright
tags: [data-source, osm, odbl]
source_id: osm
adoption: adopted
provider: "OpenStreetMap contributors（取得経路は University of Freiburg の QLever osm-planet エンドポイント）"
version: planet-260921.osm.pbf（2026-09-21）via osm2rdf
geo_granularity: 点・線・面（重心で都市圏ポリゴン内判定）
license: ODbL-1.0
license_url: https://opendatacommons.org/licenses/odbl/1-0/
license_status: verified
attribution: "© OpenStreetMap contributors. OpenStreetMap のデータは Open Database License (ODbL) 1.0 で提供されています。https://www.openstreetmap.org/copyright"
etl_module: etl/soulcity_etl/osm.py
methodology: etl/notes/osm.md
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 用途

[文化施設の密度](/metrics/culture.md)。夜の店の密度は登録率の地域差のため不採用（[nightlife](/metrics/nightlife.md)）。

# 取得経路

overpass-api.de と Geofabrik は接続不可、到達できた Overpass ミラーはすべてタイムアウトした。QLever の osm-planet SPARQL を使い、小さな範囲で OSM API と件数が一致することを確認した（レイキャビク 92/92、ナイロビ 18/17、バンコク 96/96）。応答の切り詰めを COUNT で検出する。

# ライセンス

ODbL 1.0。件数は "Produced Work" で、公開するときは "© OpenStreetMap contributors" と ODbL であることを表示する（§4.3）。検証にだけ使った Wikidata（CC0）と Overture Maps（CDLA-Permissive-2.0 ほか）の値は診断に使わない。
