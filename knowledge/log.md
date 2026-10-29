# Directory Update Log

## 2026-10-29
* **Update**: 熱帯・赤道付近の 18 都市を追加し 104 都市に（[選定](/decisions/city-selection.md)）。無作為回答でのシンガポールの 1 位率 14.6% → 12.7%、実質的に 1 位を分け合う都市数 21.9 → 25.5。

## 2026-10-28
* **Update**: 公開前の調整（類似サービスの更新履歴から抽出）。国・地域名を日本語の通称で表示（[方針](/decisions/place-names.md)、香港は「香港」）、結果画面に「占い・縁ではない／順位は優劣ではない」を明記、端の値を 100・0 に丸めない、根拠欄に誤り報告リンク（GitHub Issue フォーム）、About に運営者・公式 URL・AI との制作・問い合わせ先を追加。
* **Removal**: 企画書原文をバンドルから削除。
* **Replacement**: 仮値（demo-placeholder）を削除し、ETL による実データに置き換えた。対象を 30 → 86 都市に拡大（[選定](/decisions/city-selection.md)）。
* **Creation**: データソース 6 件（GHS-UCDB、GHS-POP、ERA5、ESA WorldCover、ITDP Atlas、OSM）を原文のライセンス確認つきで登録。不採用・検討のみのソースを記録。
* **Update**: 指標を 13 件採用、8 件を理由つきで不採用。設問を 13 問に再設計（季節差・日照時間を削除、蒸し暑さ・空気・雲量に変更）。
* **Update**: [スコア仕様 v0.2](/model/scoring.md)。方向型指標の正規化を対象都市内の q10–q90 から 524 都市圏の基準分布での百分位に変更。欠損時のスコア幅を追加。
* **Creation**: [検証レポート](/reports/validation.md)、意思決定 4 件（境界の統一、都市選定、データのライセンス、仮値の廃止）。

## 2026-10-29
* **Initialization**: P1 用のバンドル構造を作成。
* **Creation**: 指標 12 件、設問 12 件、都市 30 件（すべてデモ用の仮値）を追加。
* **Creation**: [スコアリング仕様 v0.1](/model/scoring-v0-1.md) と意思決定 3 件を追加。
