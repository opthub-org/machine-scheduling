import json
import os
import os.path
from typing import List, Tuple

from jsonschema import validate

import model
from utils import get_problem_paths, get_n_work, get_max_date, write_command_file, execute_scip

lp_file = "test.lp"
sol_file = "test.sol"


def evaluation(solution: List[int], timeout: int, problem_file: str, jig_file: str) -> Tuple[float, List[float], float]:
    """SCIPを起動して評価値を計算する。

    Parameters
    ----------
    solution
        [work1_load, work1_unload, work2_load, ...]
    timeout
        Time limit for SCIP
    problem_file
        path/to/problem_file
    jig_file
        path/to/jig_file

    Returns
    -------
    obj : float
        Objective function value.
    const : List[float]
        Constraint values.
    exe_time : float
        Execution time of SCIP.
    """
    obj = float("-inf")
    model.write_lp(solution, lp_file, problem_file, jig_file)
    write_command_file(lp_file, sol_file, timeout)

    exe_time = execute_scip()

    with open(problem_file, "r") as f:
        problem = f.readline().strip().split()
    work_num = int(problem[0]) - 12
    const = [0.0] * work_num

    if os.path.isfile(sol_file):
        with open(sol_file, "r") as f:
            data = f.readlines()
        for row in data:
            if row == "":
                continue
            # 目的関数値を取得
            if "objective value:" in row:
                obj = float(row.strip("\n").split(" ")[-1])
            # 各ワークの納期遅れ量を取得
            if "psiP" in row:
                val = row.strip("\n").split(" ")
                val = [i for i in val if not i == ""]
                if len(val[0]) <= 4:
                    continue
                num = int(val[0][4:])
                if num > 12:
                    const[num - 12 - 1] = float(val[-2])
        os.remove(sol_file)

    return obj, const, exe_time


def load_val_json(json_str: str, n_work: int, max_date: int = 9) -> Tuple[List[int], int]:
    """JSON文字列を脱直列化し，データを検証する．

    Parameters
    ----------
    json_str : str
        '{
            "schedule": [work1_load, work1_unload, work2_load, ...],
            "timeout": Time limit for SCIP
        }'
    n_work : int
        n_works = sum_i work_i
    max_date: int , 9
        Maximum date for schedule

    Returns
    -------
    schedule : List[int]
        Schedule (design variables).
    timeout : int
        Time limit for SCIP
    """
    schedule_len = n_work
    schedule_min = 1
    schedule_max = max_date
    time_min = 5 * 60
    time_max = 8 * 60 * 60
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "input schema",
        "type": "object",
        "properties": {
            "schedule": {
                "type": "array",
                "minItems": schedule_len,
                "maxItems": schedule_len,
                "items": {
                    "type": "integer",
                    "minimum": schedule_min,
                    "maximum": schedule_max
                }
            },
            "timeout": {
                "type": "integer",
                "minimum": time_min,
                "maximum": time_max
            }
        },
        "additionalProperties": False,
        "required": ["schedule", "timeout"]
    }

    data = json.loads(json_str)
    validate(data, schema)

    return data["schedule"], data["timeout"]


def main():
    problem_file, jig_file = get_problem_paths()
    n_work = get_n_work(problem_file)
    max_date = get_max_date()
    str_json = input()
    # ここでフォーマットの検証などをjsonschemaでやる
    schedule, timeout = load_val_json(str_json, n_work, max_date)

    obj, const, exe_time = evaluation(schedule, timeout, problem_file, jig_file)
    json_out = json.dumps({
        "objective": -obj,
        "constraint": None,
        "error": None,
        "info": {
            "exe_time": exe_time,
            "delays": const
        }
    })
    print(json_out)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        out_json = json.dumps(
            {"objective": None, "constraint": None, "info": None, "error": str(e)}
        )
        print(out_json)
