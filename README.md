# あなたの魂の故郷は世界のどこ？

都市統計 × 個人の好みによる都市適合診断。[企画書 v1.0](knowledge/references/proposal-v1-0.md) の P1（診断試作）。

> [!WARNING]
> 都市の指標はすべて**デモ用の仮値**（`quality: placeholder`）で、実測ではない。P0 で実データに置き換えるまで、結果を一般公開の根拠にしない。

## 構成

```
knowledge/        OKF v0.2 バンドル。データ・設問・モデル定義の正本
  references/     企画書原文
  sources/        データソース（license_status を管理）
  metrics/        指標定義（kind / transform / tolerance）
  questions/      設問と回答→理想値・重みの変換
  cities/         都市プロファイルと指標値
  model/          スコアリング仕様
  decisions/      意思決定記録
scripts/knowledge.ts   OKF 準拠チェック、index.md 生成、src/generated/knowledge.json 出力
src/scoring/      スコア関数（純関数、決定論的）
src/components/   UI
```

アプリはビルド時に `knowledge/` から JSON を生成して読むだけ。数値や設問を変えるときはコードではなく `knowledge/` を編集する。

## コマンド

| コマンド                                      | 内容                                         |
| --------------------------------------------- | -------------------------------------------- |
| `pnpm dev`                                    | knowledge を生成して開発サーバー起動         |
| `pnpm knowledge:build`                        | バンドル検証 → `index.md` 再生成 → JSON 出力 |
| `pnpm knowledge:check`                        | 検証のみ（`index.md` が古ければ失敗）。CI 用 |
| `pnpm lint` / `pnpm fmt` / `pnpm fmt:check`   | oxlint / oxfmt                               |
| `pnpm typecheck` / `pnpm test` / `pnpm build` | tsc / vitest / 本番ビルド                    |

Node 22.18 以上（`.ts` を直接実行するため）。

## ナレッジの更新ルール

- 1 ファイル = 1 コンセプト。`type` は必須（OKF §11）。
- 指標値は `{ value, quality, source, year }`。欠損は省略せず `value: null, quality: missing`。0 で埋めない。
- `quality`: `observed` / `estimated` / `imputed` / `placeholder` / `missing`。
- 実データに置き換えたら `source` を実ソースの `source_id`、`year` を観測年に変え、`log.md` に追記する。
- 人が確認したら `verified: { by: human:<id>, at: <ISO8601> }` を付ける（OKF の trust tier）。
- `index.md` は手で書かない。`pnpm knowledge:build` が生成する（ルートの `index.md` を除く）。
- `knowledge/` は oxfmt の対象外。

## デプロイ（GitHub Pages）

`main` への push で `.github/workflows/ci.yml` がチェック → ビルド → Pages へ配信する。初回のみ Pages のソースを GitHub Actions にする:

```sh
gh api -X POST "repos/{owner}/{repo}/pages" -f build_type=workflow
```

`BASE_PATH` はリポジトリ名から設定している。`<owner>.github.io` リポジトリやカスタムドメインで配信する場合は `/` にする。ホスティング判断の経緯は [decisions/hosting-github-pages](knowledge/decisions/hosting-github-pages.md)。
