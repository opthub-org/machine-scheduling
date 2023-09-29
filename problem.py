import json
import os.path
import random
import subprocess
import re
import time
from typing import List
from traceback import format_exc

import model

problem_file = "work_test.txt"
jig_file = "jig_origin.csv"
scip_command_file = "command.txt"
lp_file = "test.lp"
sol_file = "test.sol"
file_num = 27  # 初期解読み込み時の検索ファイル数


def load_problem():
    with open(problem_file, "r") as f:
        data = f.readlines()
    data = [row.replace("\n", "").split(" ") for row in data]

    return data


def load_sample_sol(n):
    """初期解読み込み，n:初期解の数"""
    sol_list, eval_list = [], []
    table = [i for i in range(file_num)]
    while len(sol_list) < n and table:
        num = table.pop(random.randrange(0, len(table)))
        if not os.path.isfile("Sol/sol_test{}.sol".format(num)):
            print("sol_test{}.sol is not exist".format(num))
            continue
        with open("Sol/sol_test{}.sol".format(num), "r") as f:
            sol_data = f.readlines()
        obj = float("-inf")
        k_d = {}
        for row in sol_data:
            if not row:
                continue
            if "objective value:" in row:
                obj = float(row.strip("\n").split(" ")[-1])
                continue
            if row.startswith("y("):
                sep_row = row.strip("\n").split(" ")
                sep_row = [s for s in sep_row if not s == ""]
                k_d.update(
                    {
                        int(re.findall(r",(.*)\)", sep_row[0])[0]): int(
                            re.findall(r"\((.*),", sep_row[0])[0]
                        )
                    }
                )
        if obj == float("-inf") or obj >= 75000:
            continue
        sol_list.append(
            [d[1] for d in sorted(k_d.items(), key=lambda x: x[0]) if d[0] > 36]
        )
        eval_list.append(obj)

    return sol_list, eval_list


def evaluation(solution: List[int], timeout: int = 300) -> float:
    """SCIPを起動して評価値を計算する。

    Parameter
    ---------
    solution
        [work1_load, work1_unload, work2_load, ...]
    timeout
        Time limit for SCIP

    Return
    ------
    float
        Objective function value.
    """
    obj = float("-inf")
    model.write_lp(solution, lp_file, problem_file, jig_file)
    with open(scip_command_file, "w") as f:
        f.write(f"read {lp_file}\n")
        f.write(f"set limits time {timeout}\n")
        f.write("optimize\n")
        f.write("display solution\n")
        f.write(f"write solution {sol_file}\n")
        f.write("quit")
    subprocess.run(
        f"scip -l Log/Log{int(time.time())}.log -b {scip_command_file}",
        shell=True,
    )

    if os.path.isfile(lp_file):
        with open(sol_file, "r") as f:
            data = f.readlines()
            for row in data:
                if "objective value:" in row:
                    obj = float(row.strip("\n").split(" ")[-1])
                    break
        os.remove(sol_file)

    return obj


def main():
    var_json = input()
    var = json.loads(var_json)
    # ここでフォーマットの検証などをjsonschemaでやる
    # 設計変数の数：ワークの総加工数の2倍（取付、取外）
    # 各変数のとりうる値：1以上、9以下の整数（境界値を含む）
    # 時間変数のとりうる範囲：5*60秒以上、8*60*60秒以下（通算評価時間が上限8時間を超えたときは、上限までをスコア計算に使う）

    obj = evaluation(var)
    out_json = json.dumps({"objective": obj, "constraint": None, "error": None})
    print(out_json)


if __name__ == "__main__":
    try:
        main()
    except:
        out_json = json.dumps(
            {"objective": None, "constraint": None, "error": format_exc()}
        )
        print(out_json)
