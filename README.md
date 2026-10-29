# あなたの魂の故郷は世界のどこ？

都市統計 × 個人の好みによる都市適合診断。

都市の指標はすべて公開統計から ETL で算出した実データ（130 都市 × 19 指標、欠損 95/2470）。仮値は使っておらず、混入したらビルドが失敗する。

| ソース                           | 指標                                           | ライセンス                   |
| -------------------------------- | ---------------------------------------------- | ---------------------------- |
| GHS-UCDB R2024A / GHS-POP R2023A | 都市境界、人口、人口加重密度、PM2.5            | CC BY 4.0                    |
| ERA5（C3S、WeatherBench 2 経由） | 最暖月・最寒月の気温、露点、降水、雲量         | CC BY 4.0                    |
| ESA WorldCover 2021              | 樹木被覆率                                     | CC BY 4.0                    |
| ITDP Atlas update_2024           | 徒歩圏の医療・教育、保護自転車道、高速公共交通 | ODbL 1.0                     |
| OpenStreetMap（QLever 経由）     | 文化施設の密度、深夜・日曜の店の営業割合       | ODbL 1.0                     |
| 天文計算（astral、tzdata）       | 夏至の日の入り時刻                             | ODbL 1.0（タイムゾーン境界） |

都市データ一式は ODbL 1.0（[DATA-LICENSE.md](DATA-LICENSE.md)）。検証結果は [knowledge/reports/validation.md](knowledge/reports/validation.md)、欠損率は [data/processed/coverage.md](data/processed/coverage.md)。

## 構成

```
knowledge/        OKF v0.2 バンドル。データ・設問・モデル定義の正本
  sources/        データソース（license_status を管理）
  metrics/        指標定義（kind / transform / tolerance）
  questions/      設問と回答→理想値・重みの変換
  cities/         都市プロファイルと指標値
  model/          スコアリング仕様
  decisions/      意思決定記録
  reports/        検証レポート（`pnpm validate` が生成）
etl/              Python ETL（uv）。ソースごとのモジュール、notes/ に詳細な方法論
  config/cities.yaml   対象都市 = GHS-UCDB の都市圏 ID
data/interim/     ソースごとの中間出力（値・品質・年・欠損理由）
data/reference/   人口 100 万人以上の 524 都市圏の値（正規化の基準分布）
data/provenance/  取得したファイルの URL・サイズ・sha256・取得日時
data/processed/   都市×指標の表と欠損率
scripts/knowledge.ts   OKF 準拠チェック、index.md 生成、src/generated/knowledge.json 出力
scripts/validate.ts    スコアの分布・頑健性・地域偏りの検証
src/scoring/      スコア関数（純関数、決定論的）
src/components/   UI
```

アプリはビルド時に `knowledge/` から JSON を生成して読むだけ。数値や設問を変えるときはコードではなく `knowledge/` を編集する。

## コマンド

| コマンド                                      | 内容                                          |
| --------------------------------------------- | --------------------------------------------- |
| `pnpm dev`                                    | knowledge を生成して開発サーバー起動          |
| `pnpm knowledge:build`                        | バンドル検証 → `index.md` 再生成 → JSON 出力  |
| `pnpm knowledge:check`                        | 検証のみ（`index.md` が古ければ失敗）。CI 用  |
| `pnpm lint` / `pnpm fmt` / `pnpm fmt:check`   | oxlint / oxfmt                                |
| `pnpm typecheck` / `pnpm test` / `pnpm build` | tsc / vitest / 本番ビルド                     |
| `pnpm etl`                                    | 全 ETL（取得 → 集計 → knowledge/cities 生成） |
| `pnpm etl build reference`                    | 中間出力から都市文書と基準分布だけ再生成      |
| `pnpm validate`                               | 検証レポートの生成                            |

Node 22.18 以上（`.ts` を直接実行するため）。ETL は Python 3.12 以上と [uv](https://docs.astral.sh/uv/)。初回の全取得は ERA5 の約 200 GB のストリーミングを含み 1 時間以上かかる（取得したファイルは `.cache/raw/` に残り、再実行では再利用する）。

## ナレッジの更新ルール

- 1 ファイル = 1 コンセプト。`type` は必須（OKF §11）。
- `knowledge/cities/` は ETL が生成する。手で編集しない。
- 指標値は `{ value, quality, source, year }`。欠損は省略せず `value: null, quality: missing, reason`。0 や推定で埋めない。
- `quality`: `observed` / `estimated` / `imputed` / `missing`。`placeholder` は禁止。
- 指標を採用・不採用にするときは `knowledge/metrics/` の `adoption` を変え、`log.md` に追記する。
- 人が確認したら `verified: { by: human:<id>, at: <ISO8601> }` を付ける（OKF の trust tier）。
- `index.md` は手で書かない。`pnpm knowledge:build` が生成する（ルートの `index.md` を除く）。
- `knowledge/` は oxfmt の対象外。

## デプロイ（GitHub Pages）

`master` への push で `.github/workflows/ci.yml` がチェック → ビルド → Pages へ配信する。初回のみ Pages のソースを GitHub Actions にする:

```sh
gh api -X POST "repos/{owner}/{repo}/pages" -f build_type=workflow
```

`BASE_PATH` はリポジトリ名から設定している。`<owner>.github.io` リポジトリやカスタムドメインで配信する場合は `/` にする。ホスティング判断の経緯は [decisions/hosting-github-pages](knowledge/decisions/hosting-github-pages.md)。

## ライセンス

- コード: [MIT](LICENSE)
- 都市指標データ（`data/`、`knowledge/cities/`、生成される `src/generated/knowledge.json` など）: [ODbL 1.0](DATA-LICENSE.md)。各ソースの帰属表示も同ファイルとアプリの「データと計算方法」に記載。
