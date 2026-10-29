---
type: Data Source
title: ERA5 再解析（Copernicus C3S）
description: 1990–2019 年の月別気温・降水・雲量・露点。WeatherBench 2 の公開コピーから取得。CC BY 4.0。
status: verified
resource: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
tags: [data-source, climate]
source_id: era5
adoption: adopted
provider: Copernicus Climate Change Service (C3S) / ECMWF。取得経路は Google WeatherBench 2 の GCS 公開バケット
version: ERA5 hourly single levels, doi:10.24381/cds.adbb2d47。WB2 の 1959-2022-6h-1440x721 と era5-hourly-climatology 1990-2019
geo_granularity: 0.25° グリッド（約 25 km）
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
license_status: verified
attribution: "Contains modified Copernicus Climate Change Service information (ERA5, 1990–2019) [2026]. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains. Hersbach et al. (2020), doi:10.1002/qj.3803."
etl_module: etl/soulcity_etl/era5.py
methodology: etl/notes/era5.md
generated: { by: claude, at: 2026-10-28T00:00:00Z }
---

# 用途

[最暖月の気温](/metrics/temp-warmest.md)、[最寒月の気温](/metrics/temp-coldest.md)、[年降水量](/metrics/precip-annual.md)、[雲量](/metrics/cloud-cover.md)、[蒸し暑さ](/metrics/dewpoint.md)。

# 取得経路の判断

CDS API はアカウントキーが必要で、この環境からは使えなかった。Open-Meteo は共有 IP の日次上限で拒否された。Google が WeatherBench 2 として GCS に公開している ERA5 のコピーを使い、zarr のチャンクを直接読んだ。

# ライセンス（原文で確認済み）

CDS カタログの ERA5 エントリは `"license": "CC-BY-4.0"`。WB2 バケット同梱の旧 "Licence to Use Copernicus Products" も §4.2 で "Access to Copernicus Products is given for any purpose in so far as it is lawful" とし、改変物には "Contains modified Copernicus Climate Change Service information [Year]" の表示を求める。

# 注意点

- 都市圏ポリゴン内の陸セル平均（セルがなければ最寄りの陸セル）。都市熱島は再現されず、観測所より約 0.3 K 低い。
- 気温は標高差を 6.5 K/km で補正。補正量 0.5 K 超の 23 都市は `estimated`。
- 降水は山地で過大。観測所（GHCN-M v4）と 1.5 倍以上ずれた 7 都市は欠損扱い。

詳細は [etl/notes/era5.md](../../etl/notes/era5.md)。
