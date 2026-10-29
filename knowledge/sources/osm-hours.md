---
type: Data Source
title: OpenStreetMap 営業時間タグ
description: 食料品店（スーパー・コンビニ）と飲食店の opening_hours タグから、深夜・日曜に開いている店の割合。QLever の osm-planet SPARQL（planet 2026-09-21）から取得。ODbL 1.0。
status: verified
resource: https://www.openstreetmap.org/copyright
tags: [data-source, osm, odbl]
source_id: osm-hours
adoption: adopted
provider: "OpenStreetMap contributors（取得経路は University of Freiburg の QLever osm-planet エンドポイント）"
version: planet-260921.osm.pbf（2026-09-21）via osm2rdf
geo_granularity: 点・線・面（重心で都市圏ポリゴン内判定）
license: ODbL-1.0
license_url: https://opendatacommons.org/licenses/odbl/1-0/
license_status: verified
attribution: "© OpenStreetMap contributors. OpenStreetMap のデータは Open Database License (ODbL) 1.0 で提供されています。https://www.openstreetmap.org/copyright"
etl_module: etl/soulcity_etl/opening_hours.py
methodology: etl/notes/osm-hours.md
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 用途

[深夜に開いている食料品店](/metrics/late-shops.md)、[深夜に開いている飲食店](/metrics/late-dining.md)、[日曜に開いている食料品店](/metrics/sunday-shops.md)。

# 取得経路と方法

[OpenStreetMap](/sources/osm.md) と同じ QLever osm-planet SPARQL。`shop=supermarket|convenience` と `amenity=restaurant|cafe|fast_food` のうち、解析できる `opening_hours` タグを持つ店で、基準週（2026-10-05〜11）の水曜 23:00・日曜 12:00 などに開いている割合を求める。祝日の規則は無視する。

タグはチェーン店に付きやすいため、チェーン（`brand` タグあり）と非チェーンの率を、全店に占めるチェーンの割合で重み付けし直す（事後層化）。タグ付きの店が 50 未満、または店の 5% 未満にしかタグがない都市は欠損。詳細は `etl/notes/osm-hours.md`。

# 注意点

- タグ付きの店は無作為標本ではない。値はすべて `estimated`。
- 人口 100 万人以上の 524 都市圏のうち値があるのは食料品店で約 230、飲食店で約 290（主にアフリカ・南アジア・中東でタグが少ない）。
- 休日を日曜として数えるため、金曜・土曜が休日の国（イスラエル、中東の一部）の休日の様子は表さない。

# ライセンス

ODbL 1.0。割合は "Produced Work" で、公開するときは "© OpenStreetMap contributors" と ODbL であることを表示する（§4.3）。
