---
type: Decision Record
title: ホスティングは当面 GitHub Pages
description: P1 の静的 SPA を GitHub Pages で配信し、P2 以降で再判断する。
status: draft
tags: [decision]
decision_status: proposed
generated: { by: claude, at: 2026-10-29T00:00:00Z }
---

# 判断

P1（診断試作）は GitHub Pages で配信する。

# 理由

- 静的データ + クライアント計算で完結し、サーバーもDBも不要（企画書 §6）。
- リポジトリと同じ場所で Actions から配信でき、追加の契約が要らない。

# 制約

- 公開ページになる。Enterprise Cloud 以外ではアクセス制限ができないため、P2 の限定テストや仮値データの段階で「誰でも見られる」ことを前提にする。
- レスポンスヘッダー（CSP など）を設定できない。
- 結果ごとの動的 OGP 画像は作れない。都市別ページの静的 OGP なら可能。
- private リポジトリから Pages を使うには有料プランが要る。

# 再判断の条件

次のどれかが必要になったら Cloudflare Pages / Workers への移行を検討する: 限定公開（Access）、ヘッダー制御、PR ごとのプレビュー、共有画像のエッジ生成。

# ライセンスとの関係

ホスティング先にかかわらず、JSON として配信するデータは ODbL などの配布条件を受ける。[データソース](/sources/) の `license_status` を確認するまで実データを公開しない。
