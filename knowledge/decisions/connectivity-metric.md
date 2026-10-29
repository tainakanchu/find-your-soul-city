---
type: Decision Record
title: 世界とのつながり（直行便）は見送る
description: 現行・全世界・オープンライセンス・文書化された取得経路をすべて満たす路線データがないため、直行便の就航先数は指標にしない。
status: accepted
tags: [decision, data-quality]
decision_status: accepted
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 判断

「直行便でいろんな国に行ける街」の指標は作らない。調査の詳細は `etl/notes/connectivity.md`。

# 理由（2026-10-29 の調査）

- OpenFlights の路線データは 2014 年で更新停止（提供元自身が "of historical value only" としている）。ベルリン、ウランバートル、ダカール、プノンペンは空港が移転・閉鎖し 0 になる。
- Wikidata の定期便就航先（P521）は極端に不完全（ヒースロー 4 件、ドバイ 6 件など）。
- Eurostat（欧州）と米国運輸統計局 BTS（米国）は地域限定。
- Wikipedia の就航先表は CC BY-SA 4.0 で、本プロジェクトのデータ（ODbL 1.0）とは share-alike 条件が両立しない。また取得時に 429 が返り、[外部アクセス方針](/decisions/external-access-policy.md) に従って中止した。
