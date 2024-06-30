# Pythonによる気象・機構データ解析Ⅰ

https://www.asakura.co.jp/detail.php?book_code=16138
https://drive.google.com/drive/folders/1Z3flVWCdjFfneRiIUvQLVySZretux76f?usp=sharing

## 必要なライブラリ

- netcdf4

## Chapter2

### データ元

- [米国海洋大気庁](https://psl.noaa.gov/data/gridded/data.noaa.oisst.v2.html)

#### 海面気温

- sst.mnmean.nc

似た名前がいくつかあるのでファイル名 `sst.mnmean.nc` で識別する

| column    | value                   |
|-----------|-------------------------|
| Variable  | Sea Surface Temperature |
| Statistic | Mean                    |
| Level     | Surface                 |
| TimeScale | Monthly                 |

#### どのグリッドが海か？のマスタ

- [lsmask.nc](https://psl.noaa.gov/repository/entry/show?entryid=b5492d1c-7d9c-47f7-b058-e84030622bbd)
- 陸のグリッドに0, 海のグリッドに1 が入っている

## Chapter3

### データ元

- [気象庁・過去の気象データ](https://www.data.jma.go.jp/gmd/risk/obsdl/index.php)

