# 機械加工スケジューリング問題のサンプルコード

## 動作環境
- Docker

## ビルド方法
```
docker build . -t opthub/machine-scheduling:latest
```

## 実行方法
コンテナを起動すると入力待ちになる。
```
docker run -it opthub/machine-scheduling:latest
```

解を入力し、Enterを押す。
```json
[1,2,3,4,5,6,7,8,9]
```

しばらく待つと評価値が出力される。
```json
{"objective": 1.5, "constraint": null, "error": null}
```
