---
type: Data Source
title: 日の入り時刻（天文計算）
description: 都市の代表点の緯度経度とタイムゾーンから計算した、夏至・冬至の日の入りの時計時刻。外部データの取得なし。
status: verified
resource: https://github.com/sffjunkie/astral
tags: [data-source, computed]
source_id: daylight
adoption: adopted
provider: "本プロジェクトの計算（astral 3.2、timezonefinder 9.0.0 + timezonefinder-data 3.2026.4、IANA tzdata 2026.5）"
version: "2025 年の暦"
geo_granularity: 都市圏の代表点（GHS-UCDB ポリゴン内の点）
license: "Apache-2.0（astral）、MIT（timezonefinder）、ODbL-1.0（timezonefinder-data）、Public Domain（IANA tzdata）"
license_url: https://opendatacommons.org/licenses/odbl/1-0/
license_status: verified
attribution: "Contains information from timezone-boundary-builder (https://github.com/evansiroky/timezone-boundary-builder) via timezonefinder, which is made available under the Open Database License (ODbL) 1.0. IANA Time Zone Database (public domain). Solar position computed with astral (Apache-2.0)."
etl_module: etl/soulcity_etl/daylight.py
methodology: etl/notes/daylight.md
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 用途

[夏の日の入り時刻](/metrics/sunset-summer.md)。

# 方法

NOAA の式（astral）で、2025 年の夏至の日（北半球 6/21、南半球 12/21）の日の入り（太陽の上端、標準大気差、海面の地平線）を求め、その地点のタイムゾーンの時計時刻（夏時間を含む）で表す。地形や標高は考慮しない。0 時を過ぎる場合は 24 + x 時（レイキャビク 24.03 時 = 0:02）。詳細は `etl/notes/daylight.md`。

# ライセンス

計算に使うライブラリとタイムゾーン境界のデータのライセンス。境界データ（timezonefinder-data、timezone-boundary-builder 由来）は ODbL 1.0。本プロジェクトのデータは時刻だけで境界の形は含まない。日の入り時刻はそこから計算した "Produced Work" として扱う。
