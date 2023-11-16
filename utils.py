import os
import random
import re
import subprocess
import time
from typing import Tuple

file_num = 27  # 初期解読み込み時の検索ファイル数
scip_command_file = "command.txt"


def get_problem_paths(default_problem: str = "work_test.txt", default_jig: str = "jig_origin.csv") -> Tuple[str, str]:
    problem = os.getenv("PROBLEM")
    if problem is None:
        return default_problem, default_jig

    problem_path = f"problems/{problem}/work_{problem}.txt"
    jig_path = f"problems/{problem}/jig_{problem}.csv"

    return problem_path, jig_path


def get_n_work(problem_file: str) -> int:
    with open(problem_file, "r") as f:
        problem = f.readlines()
    problem = [row.replace("\n", "").split(" ") for row in problem]
    process_num = sum([int(len(n) / 7) for n in problem[13:]])  # 加工回数
    n_work = 2 * process_num  # scheduleの配列長

    return n_work


def get_max_date(default_max: int = 9) -> int:
    return int(os.getenv("MAX_DATE", default_max))


def load_problem(problem_file):
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


def write_command_file(lp_file: str, sol_file: str, timeout: int):
    with open(scip_command_file, "w") as f:
        f.write(f"read {lp_file}\n")
        f.write(f"set limits time {timeout}\n")
        f.write("optimize\n")
        f.write("display solution\n")
        f.write(f"write solution {sol_file}\n")
        f.write("quit")


def execute_scip() -> float:
    time_s = time.perf_counter()
    subprocess.run(
        f"scip -l Log/Log{int(time.time())}.log -b {scip_command_file}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time_e = time.perf_counter()
    exe_time = time_e - time_s
    return exe_time
