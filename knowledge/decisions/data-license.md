---
type: Decision Record
title: 都市指標データ一式を ODbL 1.0 で提供する
description: ITDP Atlas（ODbL）の share-alike 条件を満たすため、生成した都市データは ODbL とし、全ソースの帰属表示をアプリに載せる。
status: accepted
tags: [decision, license]
decision_status: accepted
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 判断

`data/`、`knowledge/cities/`、ビルド時に生成する `src/generated/knowledge.json` の都市指標データは Open Database License 1.0 で提供する（`DATA-LICENSE.md`）。

# 理由

- [ITDP Atlas](/sources/itdp-atlas.md) は ODbL。抽出した値を含むデータベースを公開するなら、その派生データベースは ODbL で提供し、作成方法（`etl/`）を示す必要がある（ODbL §4.4, §4.6）。
- ほかのソース（GHSL・ESA WorldCover・ERA5）は CC BY 4.0 で、帰属表示と改変の明示を条件に別のライセンスでの再配布を妨げない。
- そのため、データ一式を ODbL に統一し、アプリの「データと計算方法」に全ソースの帰属表示を原文のまま表示する。

# 確認したライセンス

| ソース | ライセンス | 商用利用 | 主な義務 |
| --- | --- | --- | --- |
| GHS-UCDB / GHS-POP | CC BY 4.0 | 可 | 出典表示・改変の明示 |
| ERA5（C3S） | CC BY 4.0 | 可 | "Contains modified Copernicus..." の表示 |
| ESA WorldCover | CC BY 4.0 | 可 | "© ESA WorldCover project 2021 / ..." の表示 |
| ITDP Atlas | ODbL 1.0 | 可 | 表示・派生 DB の share-alike |

アプリのソースコード自体のライセンスは別途オーナーが決める。
