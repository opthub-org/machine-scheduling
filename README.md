# 機械加工スケジューリング問題のサンプルコード

## コンテンツ
```
.
├── LP
│   ├── prob_test0.lp
│   ├── prob_test1.lp
│   ├── prob_test10.lp
│   ├── prob_test11.lp
│   ├── prob_test12.lp
│   ├── prob_test13.lp
│   ├── prob_test14.lp
│   ├── prob_test15.lp
│   ├── prob_test16.lp
│   ├── prob_test17.lp
│   ├── prob_test18.lp
│   ├── prob_test19.lp
│   ├── prob_test2.lp
│   ├── prob_test20.lp
│   ├── prob_test21.lp
│   ├── prob_test22.lp
│   ├── prob_test23.lp
│   ├── prob_test24.lp
│   ├── prob_test25.lp
│   ├── prob_test26.lp
│   ├── prob_test3.lp
│   ├── prob_test4.lp
│   ├── prob_test5.lp
│   ├── prob_test6.lp
│   ├── prob_test7.lp
│   ├── prob_test8.lp
│   └── prob_test9.lp
├── Log
│   ├── Log1694940265.log
│   ├── Log1694940294.log
│   ├── Log1694940594.log
│   ├── Log1694940765.log
│   ├── Log1694940850.log
│   ├── Log1694940879.log
│   ├── Log1694941179.log
│   ├── Log1694941479.log
│   ├── Log1694941508.log
│   ├── Log1694941536.log
│   ├── Log1694941565.log
│   ├── Log1694941594.log
│   ├── Log1694941894.log
│   ├── Log1694942088.log
│   ├── Log1694942281.log
│   ├── Log1694942475.log
│   ├── Log1694942503.log
│   ├── Log1694942525.log
│   ├── Log1694942554.log
│   ├── Log1694942582.log
│   ├── Log1694942610.log
│   ├── Log1694942778.log
│   ├── Log1694943079.log
│   ├── Log1694943107.log
│   ├── Log1694943135.log
│   ├── Log1694943219.log
│   ├── Log1694943519.log
│   ├── Log1694943548.log
│   ├── Log1694943741.log
│   ├── Log1694943934.log
│   ├── Log1694944128.log
│   ├── Log1694944156.log
│   ├── Log1694944185.log
│   ├── Log1694944213.log
│   ├── Log1694944241.log
│   ├── Log1694944325.log
│   ├── Log1694944353.log
│   ├── Log1694944438.log
│   ├── Log1694944738.log
│   ├── Log1694944766.log
│   ├── Log1694944795.log
│   ├── Log1694944823.log
│   ├── Log1694944851.log
│   ├── Log1694944879.log
│   ├── Log1694944908.log
│   ├── Log1694944936.log
│   ├── Log1694944964.log
│   ├── Log1694944993.log
│   ├── Log1694945021.log
│   ├── Log1694945050.log
│   ├── Log1694945078.log
│   ├── Log1694945107.log
│   ├── Log1694945136.log
│   ├── Log1694945164.log
│   ├── Log1694945180.log
│   ├── Log1694945208.log
│   ├── Log1694945237.log
│   ├── Log1694945266.log
│   ├── Log1694945295.log
│   ├── Log1694945324.log
│   ├── Log1694945352.log
│   ├── Log1694945380.log
│   ├── Log1694945408.log
│   ├── Log1694945437.log
│   ├── Log1694945465.log
│   ├── Log1694945493.log
│   ├── Log1694945522.log
│   ├── Log1694945550.log
│   ├── Log1694945578.log
│   ├── Log1694945607.log
│   ├── Log1694945635.log
│   ├── Log1694945663.log
│   ├── Log1694945668.log
│   ├── Log1694945696.log
│   ├── Log1694945724.log
│   ├── Log1694945753.log
│   ├── Log1694945781.log
│   ├── Log1694945809.log
│   ├── Log1694945838.log
│   ├── Log1694945864.log
│   ├── Log1694945891.log
│   ├── Log1694945918.log
│   ├── Log1694945944.log
│   ├── Log1694945971.log
│   ├── Log1694945998.log
│   ├── Log1694946025.log
│   ├── Log1694946053.log
│   ├── Log1694946082.log
│   ├── Log1694946110.log
│   ├── Log1694946138.log
│   ├── Log1694946167.log
│   ├── Log1694946195.log
│   ├── Log1694946223.log
│   ├── Log1694946252.log
│   ├── Log1694946280.log
│   ├── Log1694946308.log
│   ├── Log1694946337.log
│   ├── Log1694946365.log
│   ├── Log1694946393.log
│   ├── Log1694946422.log
│   ├── Log1694946455.log
│   ├── Log1694946484.log
│   ├── Log1694946784.log
│   ├── Log1694946813.log
│   ├── Log1694946841.log
│   ├── Log1694947141.log
│   ├── Log1694947169.log
│   ├── Log1694947197.log
│   ├── Log1694947226.log
│   ├── Log1694947254.log
│   ├── Log1694947282.log
│   ├── Log1694947311.log
│   ├── Log1694947339.log
│   ├── Log1694947367.log
│   ├── Log1694947395.log
│   ├── Log1694947424.log
│   ├── Log1694947452.log
│   ├── Log1694947481.log
│   ├── Log1694947494.log
│   ├── Log1694947522.log
│   ├── Log1694947551.log
│   ├── Log1694947851.log
│   ├── Log1694947879.log
│   ├── Log1694947907.log
│   ├── Log1694947935.log
│   ├── Log1694947964.log
│   ├── Log1694947992.log
│   ├── Log1694948020.log
│   ├── Log1694948049.log
│   ├── Log1694948077.log
│   ├── Log1694948105.log
│   ├── Log1694948405.log
│   ├── Log1694948434.log
│   ├── Log1694948462.log
│   ├── Log1694948490.log
│   ├── Log1694948790.log
│   ├── Log1694948819.log
│   ├── Log1694948848.log
│   ├── Log1694948877.log
│   ├── Log1694948905.log
│   ├── Log1694948934.log
│   ├── Log1694948962.log
│   ├── Log1694948991.log
│   ├── Log1694949020.log
│   ├── Log1694949025.log
│   ├── Log1694949054.log
│   ├── Log1694949082.log
│   ├── Log1694949111.log
│   ├── Log1694949139.log
│   ├── Log1694949167.log
│   ├── Log1694949196.log
│   ├── Log1694949224.log
│   ├── Log1694949252.log
│   ├── Log1694949281.log
│   ├── Log1694949309.log
│   ├── Log1694949337.log
│   ├── Log1694949365.log
│   ├── Log1694949394.log
│   ├── Log1694949422.log
│   ├── Log1694949451.log
│   ├── log_test0.log
│   ├── log_test1.log
│   ├── log_test10.log
│   ├── log_test11.log
│   ├── log_test12.log
│   ├── log_test13.log
│   ├── log_test14.log
│   ├── log_test15.log
│   ├── log_test16.log
│   ├── log_test17.log
│   ├── log_test18.log
│   ├── log_test19.log
│   ├── log_test2.log
│   ├── log_test20.log
│   ├── log_test21.log
│   ├── log_test22.log
│   ├── log_test23.log
│   ├── log_test24.log
│   ├── log_test25.log
│   ├── log_test26.log
│   ├── log_test3.log
│   ├── log_test4.log
│   ├── log_test5.log
│   ├── log_test6.log
│   ├── log_test7.log
│   ├── log_test8.log
│   └── log_test9.log
├── README.md
├── Sol
│   ├── sol_test0.sol
│   ├── sol_test1.sol
│   ├── sol_test10.sol
│   ├── sol_test11.sol
│   ├── sol_test12.sol
│   ├── sol_test13.sol
│   ├── sol_test14.sol
│   ├── sol_test15.sol
│   ├── sol_test16.sol
│   ├── sol_test17.sol
│   ├── sol_test18.sol
│   ├── sol_test19.sol
│   ├── sol_test2.sol
│   ├── sol_test20.sol
│   ├── sol_test21.sol
│   ├── sol_test22.sol
│   ├── sol_test23.sol
│   ├── sol_test24.sol
│   ├── sol_test25.sol
│   ├── sol_test26.sol
│   ├── sol_test3.sol
│   ├── sol_test4.sol
│   ├── sol_test5.sol
│   ├── sol_test6.sol
│   ├── sol_test7.sol
│   ├── sol_test8.sol
│   └── sol_test9.sol
├── best_sol.txt
├── command.txt
├── jig_origin.csv
├── log.txt
├── main.py
├── model.py
├── test.lp
└── work_test.txt

3 directories, 250 files
```

## Dependencies
- Python 3.7+
- SCIP 8.0+

## Build
```
docker build . -t opthub/machine-scheduling:latest
```

## Usage

```
python main.py
```
