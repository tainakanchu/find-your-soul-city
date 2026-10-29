---
type: Metric
title: 地震の揺れの想定
description: 不採用。元データ（GEM 世界地震ハザードマップ）が非商用・継承条件で、本プロジェクトのデータライセンスと両立しない。
status: rejected
tags: [metric, rejected, ghsl-hazard]
metric_key: quake
adoption: rejected
source: ghsl-hazard
rejection_reason: "GHS-UCDB の地震曝露（EX_E01–E10, EX_SHA_POP）は GEM Global Seismic Hazard Map 2023.1 から作られ、GEM は CC BY-NC-SA 4.0（非商用・継承）。本プロジェクトの都市データは商用利用も許す ODbL 1.0 で、非商用条件を引き継げない。パブリックドメインなど両立するライセンスの代替データ（米国地質調査所の地震ハザードマップ等）を調べてから再検討する。"
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 不採用の理由

GHS-UCDB の地震曝露は GEM Global Seismic Hazard Map 2023.1（CC BY-NC-SA 4.0）から作られている。本プロジェクトの都市データは ODbL 1.0 で商用利用も許すため、非商用・継承の条件を引き継げない。

値そのものは妥当だった（人口加重の揺れの超過: 東京 3.05、イスタンブール 2.46、ロサンゼルス 2.44、大阪 2.12、台北 2.10、ロンドン・パリ 0）。

# 次の一手

両立するライセンスの代替データ（パブリックドメインの地震ハザードマップなど）を調べる。

出典候補: [ghsl-hazard](/sources/ghsl-hazard.md)
