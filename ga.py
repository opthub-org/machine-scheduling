import copy
import random

import problem_sop
import utils

g = 30  # 世代数
p_cross = 0.5  # 交叉率
p_mutate = 0.015  # 突然変異確率
D = 5  # スケジュール日数
N = 10  # 個体数
file_num = 27  # 初期解読み込み時の検索ファイル数


def crossover(current_sol):
    """一点交叉"""
    # current_sol: solution(ワーク順のリスト)のリスト, 評価値なし
    new_sol = []  # 生成した個体のリスト
    random.shuffle(current_sol)  # (0,1), (2,3),...でペアリング
    for i in range(int(len(current_sol) / 2)):
        # 交叉率に従い交叉
        # 交叉位置は必ず取り付けから
        if random.random() < p_cross:
            index = random.randint(1, int(len(current_sol[0]) / 2) - 1)
            new_sol.append(
                current_sol[i * 2][: index * 2] + current_sol[i * 2 + 1][index * 2:]
            )
            new_sol.append(
                current_sol[i * 2 + 1][: index * 2] + current_sol[i * 2][index * 2:]
            )

    return new_sol


def mutation(sol_list, problem_data):
    """突然変異（作業ごとに判定）"""
    # sol_list: 交叉で生成された解リスト
    # problem_data: 加工するワークの情報（パレット初期状態は除く）
    available_days = []  # ワークの着手可能日
    task_list = {}  # ワークの作業番号{ワーク番号(1~): 作業番号(1~)}
    task_num = 0
    for i in range(len(problem_data)):
        available_days.append(int(problem_data[i][-2]))
        available_days.append(int(problem_data[i][-2]))
        task_list[i + 1] = [
            j
            for j in range(
                task_num + 1, task_num + int(len(problem_data[i]) / 7) * 3 + 1
            )
        ]
        task_num = task_list[i + 1][-1]

    for sol in sol_list:
        count = 0
        # 作業ごとに突然変異の判定
        for i in range(len(sol)):
            if random.random() < p_mutate:
                # 割り当て可能な日付のチェック
                if i % 2 == 0:  # 取り付けの場合
                    d_before = available_days[i + 1]  # 着手可能日 or 前工程の取り外しより後
                    # 前工程があるか確認
                    if not i == 0:
                        for tasks in task_list.values():
                            if i // 2 * 3 + 1 in tasks and i // 2 * 3 in tasks:
                                d_before = sol[i - 1]
                                break
                    d_after = sol[i + 1]  # 取り外しより前
                else:  # 取り外しの場合
                    d_before = sol[i - 1]  # 取り付けより後
                    d_after = D  # スケジュール日数 or 次工程の取り付けより前
                    # 次工程があるか確認
                    if not i == len(sol) - 1:
                        for tasks in task_list.values():
                            if i // 2 * 3 + 3 in tasks and i // 2 * 3 + 4 in tasks:
                                d_before = sol[i + 1]
                                break
                # 変異できない場合
                if d_before == d_after:
                    continue
                # 突然変異
                table = [j for j in range(d_before, d_after + 1)]
                table.remove(sol[i])
                sol[i] = random.choice(table)
                count += 1


def roulette(sol_list, eval_list):
    """ルーレット選択"""
    # sol_list: 解リスト
    # eval_list: 評価値リスト
    return_sols = []
    return_evals = []
    table = []
    all_e = sum(eval_list)
    for e in eval_list:
        table.append(e / all_e)
    # 残す個体を選択
    while len(return_sols) < N:
        p = random.random()
        for i in range(len(table)):
            if p < sum(table[: i + 1]):
                return_sols.append(sol_list[i].copy())
                return_evals.append(eval_list[i])
                break

    return return_sols, return_evals


def main():
    problem_file, jig_file = utils.get_problem_paths()
    problem_data = utils.load_problem(problem_file)
    global N
    sol_list, eval_list = utils.load_sample_sol(N)
    N = len(sol_list)
    log = {}
    log["init"] = [(sol, e) for sol, e in zip(sol_list, eval_list)]
    for i in range(g):
        print("第{}世代".format(i + 1))
        log[i + 1] = []
        new_sol = crossover(copy.deepcopy(sol_list))
        mutation(new_sol, problem_data[13:])
        new_eval = []
        for sol in copy.deepcopy(new_sol):
            e = problem_sop.evaluation(sol, 600, problem_file, jig_file)
            if not e == float("-inf"):
                new_eval.append(e)
                log[i + 1].append("update")
                log[i + 1].append(e)
            else:
                new_sol.remove(sol)
                log[i + 1].append("reject")
        sol_list, eval_list = roulette(sol_list + new_sol, eval_list + new_eval)
        # 途中保存用
        with open("log.txt", "w") as f:
            for v in log.keys():
                f.write(str(v) + ": " + ",".join([str(l) for l in log[v]]) + "\n")
    best_index = eval_list.index(max(eval_list))
    best_sol = sol_list[best_index]
    best_eval = eval_list[best_index]
    with open("best_sol.txt", "w") as f:
        f.write("Objective value: {}\n".format(best_eval))
        f.write(",".join([str(d) for d in best_sol]) + "\n")
    with open("log.txt", "w") as f:
        for v in log.keys():
            f.write(str(v) + ": " + ",".join([str(l) for l in log[v]]) + "\n")


if __name__ == "__main__":
    main()
