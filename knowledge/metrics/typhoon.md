---
type: Metric
title: 熱帯低気圧（台風・ハリケーン）の被災回数
description: 2004〜2016 年に熱帯低気圧の被害範囲に入った回数の年平均。
status: adopted
tags: [metric, ghsl-hazard]
metric_key: typhoon
etl_key: tropical_cyclone_hazards_per_year
reference_column: tropical_cyclone_hazards_per_year
adoption: adopted
unit: "回/年"
kind: lower_better
transform: linear
source: ghsl-hazard
period: "2004–2016 年（3 年ずつ 3 期間）"
geography: "GHS-UCDB 都市圏（UCDB が MYRIAD-HES の被害範囲と重ねて算出）"
method: "HZ_CEV_TCY（各 3 年間の熱帯低気圧の件数）を 3 期間合計し 9 年で割る"
caveat: "回数だけで強さは含まない。内陸で弱まった後の通過も数える"
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 定義

熱帯低気圧（台風・ハリケーン・サイクロン）の記録上の被害範囲に都市圏が入った回数の年平均。

# スコアへの入り方

少ないほど良い型。設問「[自然災害が少ない街](/questions/14-hazard.md)」で [洪水](/metrics/flood.md) と重みを等分する。

# 根拠と検証

マニラ 3.78、台北 3.44、大阪 2.78、マイアミ 2.67、東京 2.33、欧州は 0。香港 0.78 は被害範囲の取り方による過小の可能性がある。ナイロビは結合対象外で欠損。強さを含む風速データ（STORM）は取得元に接続できず使っていない。

# 注意点

回数だけで強さは含まない。内陸で弱まった後の通過も数える。

出典: [ghsl-hazard](/sources/ghsl-hazard.md)
