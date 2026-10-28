# decisions

* [都市の範囲を GHS-UCDB の都市圏ポリゴンに統一する](boundary-ucdb.md) - すべての指標を同じポリゴンで集計し、境界の異なる統計を混ぜない。
* [対象 86 都市の選定](city-selection.md) - P1 の 30 都市に地域・気候・規模の分散のため 56 都市を加えた。正規化は対象都市に依存させない。
* [都市指標データ一式を ODbL 1.0 で提供する](data-license.md) - ITDP Atlas（ODbL）の share-alike 条件を満たすため、生成した都市データは ODbL とし、全ソースの帰属表示をアプリに載せる。
* [ホスティングは当面 GitHub Pages](hosting-github-pages.md) - P1 の静的 SPA を GitHub Pages で配信し、P2 以降で再判断する。
* [仮値を廃止し、本番ビルドで検出したら失敗させる](no-placeholder.md) - P1 のデモ用仮値をすべて実データに置き換え、仮値の混入をビルドで止める。
* [価値観スコア（EVS/WVS）は P1 では扱わない](values-score-separate.md) - 国別調査を都市に外挿しないため、価値観の設問は別枠とし P1 には入れない。
