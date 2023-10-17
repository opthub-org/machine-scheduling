# 機械加工スケジューリング問題のサンプルコード

## 動作環境
- Docker

## ビルド方法
```
docker build . -t opthub/machine-scheduling-sop:latest -f sop.dockerfile
```

## 実行方法
コンテナを起動すると入力待ちになる。
```
docker run -it -e MAX_DATE=3  opthub/machine-scheduling-sop:latest
```

解を入力し、Enterを押す。
```json
{"schedule": [1,2,3,4,5,6,7,8,9,1,1,2,3,4,5,6,7,8,9,2], "timeout": 500} 
```

しばらく待つと評価値が出力される。
```json
{"objective": -4918.5, "constraint": null, "error": null, "info": {"exe_time": 500.56001581798773, "delays": [0.0, 0.0, 0.0, 0.0, 0.0, 1055.0, 2548.0, 4080.0, 5400.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1200.0, 2485.0, 3925.0, 5527.0, 0.0
]}}
```

## 設定方法

環境変数:

- `MAX_DATE`: スケジュールの最大日数 (デフォルト値: `9`)
- `PROBLEM`: 問題名 (デフォルト: `work_test.txt`および`jig_origin.csv`を参照)

問題の設定方法:  
`/problems/<prbolem name>/`以下に`work_<problem name>.txt`および`jig_<problem name>.csv`を配置し，
環境変数`PROBLEM`を`<problem name>`に設定．