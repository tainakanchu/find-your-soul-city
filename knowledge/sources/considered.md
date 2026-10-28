---
type: Data Source
title: 検討して採用しなかったソース
description: WHO 大気質、NASA Black Marble、EU Quality of Life、GHCN-M（検証専用）などの判断記録。
status: draft
tags: [data-source, rejected]
source_id: considered
adoption: rejected
provider: 複数
license_status: unverified
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# WHO Ambient Air Quality Database

観測所のある都市の年平均値で、都市名で突き合わせる必要があり、観測網の密度・年が都市ごとに異なる。UCDB の衛星由来 PM2.5（同じポリゴンで人口加重）のほうが比較可能性が高いため、そちらを採用した。

# NASA Black Marble（夜間光）

夜間光は電化・経済活動の代理で、夜遊びや文化の豊かさの直接指標ではない。対応する設問がないため不採用。

# EU Quality of Life in European Cities

欧州の都市にしかなく、86 都市の比較に使えない。将来の外的妥当性検証の候補。

# NOAA GHCN-M v4（気象観測所）

ERA5 の気温・降水の検証専用。診断の値には使わない（[ERA5](/sources/era5.md)）。

# Open-Meteo / Copernicus CDS API

Open-Meteo は共有 IP の日次上限で取得できず、CDS API はキーが必要だった。どちらも同じ ERA5 なので、公開コピー（WeatherBench 2）から取得した。

# Overpass（overpass-api.de）/ Geofabrik

この環境から接続できなかった。OSM の取得は別ミラーで行った（[OSM](/sources/osm.md)）。
