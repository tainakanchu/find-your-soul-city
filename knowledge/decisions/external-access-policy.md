---
type: Decision Record
title: 外部サービスへのアクセス方針
description: データ取得は提供元が用意した経路に限り、Web UI の自動操作はしない。2026-10-28 の ITDP Atlas での事象を受けて制定。
status: accepted
tags: [decision, etl, ethics]
decision_status: accepted
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 経緯

2026-10-28 20:40 UTC ごろ、ETL のサブエージェントが ITDP Atlas（R Shiny アプリ）のダウンロード処理を websocket 経由でスクリプトから呼び出した。必要な入力をそろえずに呼んだため、サーバが "The application unexpectedly exited" を返した。アプリのセッションを 1 回から数回、異常終了させた可能性がある。サービスはその後も応答しており（同日中に HTTP 200 を確認）、データは ITDP が GitHub release で公開している正規のファイルから取得した。

原因は、委任した作業指示に「公式の取得経路以外を使わない」「相手に障害を与えうる操作をしない」が書かれていなかったこと。

# ルール

1. データは提供元が取得用に用意した経路（ファイル配布、文書化された API、公開バケット、公式リリース）からだけ取る。Web UI（Shiny/websocket のハンドラ、フォーム送信、非公開エンドポイント、ヘッドレスブラウザ）を自動操作してデータを抜かない。
2. 先に利用規約とレート制限を読む。`soulcity_etl.common.fetch()`（識別できる User-Agent、指数バックオフ）を使い、文書で許されていない限り逐次で送る。
3. 429・5xx・タイムアウト・"server too busy"・自分が起こしたエラーが出たら、その時点で止める。同じ操作を繰り返さず、`etl/notes/<source>.md` に記録して利用者に報告する。
4. 文書化されていない経路しか残らないときは、自分で判断せず利用者に確認する。
5. サブエージェントに委任するときは、このルールを指示に含める（`etl/notes/BRIEF.md`、リポジトリの `CLAUDE.md`）。
