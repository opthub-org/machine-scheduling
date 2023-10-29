import os
from typing import Tuple


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
    process_num = sum([int(len(n) / 7) for n in problem[13:]])  # 加工回数（scheduleの配列長）

    return process_num


def get_max_date(default_max: int = 9) -> int:
    return int(os.getenv("MAX_DATE", default_max))
