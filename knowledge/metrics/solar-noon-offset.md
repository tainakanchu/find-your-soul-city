---
type: Metric
title: 時計と太陽のずれ（太陽が南中する時計の時刻 − 12 時）
description: 不採用。国の時間帯の制度を表す値で、暮らしの中で直接感じにくい。
status: rejected
tags: [metric, rejected, daylight]
metric_key: solar_noon_offset
adoption: rejected
source: daylight
rejection_reason: "国の時間帯の制度を表す値で、暮らしの中で直接感じにくい。夏の日の入り時刻（順位相関 0.49）がこのずれの影響をすでに含む。"
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 不採用の理由

国の時間帯の制度を表す値で、暮らしの中で直接感じにくい。夏の日の入り時刻（順位相関 0.49）がこのずれの影響をすでに含む。

値は `data/interim/daylight.json` に残しているが、診断には使わない。

出典候補: [daylight](/sources/daylight.md)
