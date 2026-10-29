---
type: Metric
title: 日曜の昼に開いているスーパーの割合
description: 不採用。深夜営業の売店を除けるため実態に近いが、タグが十分にある都市が 130 都市中 80 都市（欠損 38%）。
status: rejected
tags: [metric, rejected, osm-hours]
metric_key: supermarket_sunday
adoption: rejected
source: osm-hours
rejection_reason: "深夜営業の売店を除けるため実態に近いが、タグが十分にある都市が 130 都市中 80 都市（欠損 38%）。食料品店全体の割合（100 都市）を採用した。"
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 不採用の理由

深夜営業の売店を除けるため実態に近いが、タグが十分にある都市が 130 都市中 80 都市（欠損 38%）。食料品店全体の割合（100 都市）を採用した。

値は `data/interim/osm-hours.json` に残しているが、診断には使わない。

出典候補: [osm-hours](/sources/osm-hours.md)
