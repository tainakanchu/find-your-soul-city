---
type: Decision Record
title: 都市の範囲を GHS-UCDB の都市圏ポリゴンに統一する
description: すべての指標を同じポリゴンで集計し、境界の異なる統計を混ぜない。
status: accepted
tags: [decision, comparability]
decision_status: accepted
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 判断

「都市」は [GHS-UCDB R2024A](/sources/ghsl-ucdb.md) の都市圏（urban centre）1 つとする。

# 各ソースの対応

| ソース | 対応 | 確認 |
| --- | --- | --- |
| GHS-UCDB / GHS-POP | 同じポリゴン | GHS-POP のセル合計と UCDB 人口の比 1.000000（86 都市） |
| ERA5 | ポリゴン内の陸セル（なければ最寄りの陸セル） | 64 都市がポリゴン内、22 都市が最寄り（最大 22 km） |
| ESA WorldCover | ポリゴン内の 10 m 画素 | 画素面積の合計 / UCDB 面積 = 0.997〜0.998 |
| ITDP Atlas | Atlas 自体が R2024A の同じ ID・ポリゴン | IoU ≥ 0.9999（85 都市） |

# 行政市域との違い

都市圏は人口密度と連続性で定義される。東京は横浜・川崎・さいたま・千葉を、大阪は神戸・京都を、ソウルは仁川を含む。京都は単独の都市圏がないため対象外。行政市域ベースの統計（WHO 大気質データベースなど）は境界が合わないため使わない。
