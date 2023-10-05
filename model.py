import copy
import csv
from typing import List

# 納期を付加したバージョン
# 前のctt書式にも対応
# 目的関数を納期余裕最大化
# 段取り替え時間の実装バージョン
# 治具の情報をcsvから取得
# 治具交換の制約を厳しくしたバージョン
# 9/30制約追加

total_count = 0


def line_count():
    global total_count
    total_count += 1
    return total_count


# def day_span(work_num, work_time):
#     mc_time = 0
#     for i in work_num:
#         mc_time += int((work_time[int(i) - 1]))
#     mc_day = mc_time / 1440
#     day = int(mc_day + (mc_day * 0.2 + 1))
#     return day


def jig_num(st_num, num):
    count = st_num + num
    jig_list = [i for i in range(st_num, count)]
    return jig_list, count


def write_lp(
    solution: List[int]=None,  # 日付割り当てリスト
    lp_file="test.lp",  # 生成する問題ファイル名（送信された解から生成する）
    work_file="work.txt",  # ワークの定義ファイル（問題ごとに固定）
    jig_file="jig.csv"  # 治具の定義ファイル（問題ごとに固定）
):
    if solution is None:
        solution = []
    with open(work_file) as f:
        contents = f.readlines()

    data = {}  # 全てのデータの配列
    for i in range(len(contents)):  # テキストファイルのデータを全て読み取り、配列に格納
        data[i] = contents[i].strip().split()

    W = int(data[0][0])  # ワーク（製品）の数
    M = int(data[0][1])  # 機械の数

    # jig = [[] for _ in range(W)]
    JIG = []
    MW = [[] for _ in range(M)]  # 機械ごとの作業を格納する配列作成

    pallet = 12
    T = 960
    D = 9  # スケジュール期間
    # A = 1440 * (D + 1)\
    A = 1000000
    NS = [480 + 1440 * i for i in range(D)]

    Pt = []  # 作業の処理時間
    usable_day = []  # 1~
    lead_time = []  # 1~
    count = 1

    for i in range(1, W + 1):  # 作業ついてのみの配列と機械ごとの作業の配列作成
        pro_num = int(len(data[i]) / 7)  # 加工回数
        for j in range(len(data[i])):
            if j % 2 == 1 and int(data[i][j]) < 1000 and j < pro_num * 6:
                Pt.append(data[i][j])
            elif int(data[i][j]) < 1000 and j < pro_num * 6:  # int(len(data[i])/7)*6:data配列の最初の治具情報の配列番号
                MW[int(data[i][j])].append(count)
                count += 1
        for j in range(int(len(data[i]) / 7) * 6, int(len(data[i]) / 7) * 6 + int(len(data[i]) / 7)):
            # jig[i - 1].append(data[i][j])
            JIG.append(data[i][j])
        if len(data[i]) > pro_num * 6 + pro_num + 1:
            usable_day.append(data[i][-2])
            lead_time.append(data[i][-1])

    K = [i for i in range(1, len(Pt) + 1)]

    Nj = []  # ワークの作業数を格納
    for i in range(1, len(data)):  # 各ワークの工程数
        Nj.append(int(len(data[i]) / 7) * 3)

    Kb = [MW[0][i] for i in range(0, len(MW[0]), 2)]  # 取り付け作業の作業番号を格納した配列

    # 品番と取り付け作業の整理
    all_wnum = []  # ワークの品番番号の配列
    for i in range(1, len(data)):
        all_wnum += [data[i][-3].split('_')[0]]
    tmp = copy.deepcopy(Kb)
    hs = {}  # 品番と作業番号の辞書型 Key:作業番号　Value: 品番
    for i in range(len(Nj)):
        for j in range(int(Nj[i] / 3)):
            num = tmp.pop(0)
            hs[num] = all_wnum[i]

    dic_jig = {}  # 治具の番号振り

    have_jig = []
    with open(jig_file, encoding='utf-8-sig') as f:
        jig_facility = [i for i in csv.reader(f)]
    for i in jig_facility:
        have_jig.append(int(i[1]))
    # have_jig.append(palet)

    jig_total = 0
    for i in have_jig:
        jig_total += i
    count = 1
    for i in range(len(have_jig)):
        dic_jig[i], count = jig_num(count, have_jig[i])

    stg = 30  # start time gap:本来の開始時刻(8:30)とのGAP

    rs = []  # 休憩時間の開始時刻集合
    rf = []  # 休憩時間の終了時刻集合
    for i in range(D):
        rs.append(90 - stg + 1440 * i)  # 9:00
        rs.append(210 - stg + 1440 * i)  # 12:00
        rs.append(390 - stg + 1440 * i)  # 15:00
        rf.append(100 - stg + 1440 * i)
        rf.append(255 - stg + 1440 * i)
        rf.append(405 - stg + 1440 * i)

    r = []
    for i in range(D * 3):
        r.append(1000 + i)

    f = open(lp_file, "w")
    f.write("maximize\n")
    count = 0
    for k in range(W):
        count += Nj[k]
        f.write(" - tf{}".format(count))  # ワークの納品時刻
    f.write(' - psiP')  # 納期遅れペナルティ
    count = 0
    for k in range(W):
        count += int(lead_time[k]) * 1440 - T
    f.write(" + {}\n".format(count))  # 納期
    f.write("subject to\n")

    # 解固定
    k = 3 * 12
    for sol in solution:
        k += 1
        f.write("c{2}: y({0},{1}) = 1\n".format(sol, k, line_count()))
        k += 2
        f.write("c{2}: y({0},{1}) = 1\n".format(sol, k, line_count()))

    # f.write('c{}:'.format(line_count()))
    # for i in range(W):
    #     f.write(' + psiR{}'.format(i + 1))
    # f.write(' - psiR = 0\n')

    f.write("c{}:".format(line_count()))
    for i in range(W):
        f.write(" + psiP{}".format(i + 1))
    f.write(" - psiP = 0\n")

    # メイクスパン
    # for i in MW[0]:
    #     f.write("c{1}: z - tf{0} >= 0".format(i, line_count()))

    if W < pallet:
        num = W
    else:
        num = pallet
    pKb = [[] for _ in range(num)]
    count = 0
    for i in range(len(pKb)):
        for j in range(int(Nj[i] / 3)):
            pKb[i].append(Kb[count])
            count += 1
        f.write("c{1}: ts{0} = 0\n".format(pKb[i][0], line_count()))

    for i in range(pallet):
        f.write("c{2}: v({0},{1}) = 1\n".format(pKb[i][0], i + 1, line_count()))

    count = 0  # 納期余裕と納期遅れ
    for i in range(0, len(usable_day)):  # 2
        count += Nj[i]
        # f.write('c{3}: psiR{0} + tf{1} <= {2}\n'.format(i + 1, count, int(lead_time[i]) * 1440 - T, line_count()))
        f.write("c{3}: tf{0} - psiP{1} <= {2}\n".format(count, i + 1, int(lead_time[i]) * 1440 - T, line_count()))

    count = 0
    for i in range(0, len(usable_day)):
        count += 1
        f.write("c{2}: ts{0} >= {1}\n".format(count, (int(usable_day[i]) - 1) * 1440, line_count()))  # 3
        count = count + Nj[i] - 1
        # f.write("c{2}: tf{0} <= {1}".format(count, int(usable_day[i]) * 1440 + int(lead_time[i]) * 1440 - T,
        #                                   line_count()))  # 4

    N = 0
    for i in range(W):  # 5
        for j in range(Nj[i] - 1):
            f.write("c{2}: ts{0} - tf{1} >= 0\n".format(N + j + 2, N + j + 1, line_count()))
        N = N + Nj[i]

    rMW = copy.deepcopy(MW)
    rMW[0].extend(r)

    for i in range(M):  # 6, 7
        for j in rMW[i]:
            for k in rMW[i]:
                if j != k:
                    f.write("c{3}: ts{0} - tf{1} - {2} x({1},{0}) >= -{2}\n".format(j, k, A, line_count()))
                    f.write("c{3}: ts{1} - tf{0} + {2} x({1},{0}) >= 0\n".format(j, k, A, line_count()))

    for i in MW[0]:  # 8
        f.write("c{}:".format(line_count()))
        for j in range(1, D):
            f.write(" + y({0},{1})".format(j, i))
        f.write(" + y({0},{1}) = 1\n".format(D, i))

    for i in MW[0]:  # 9
        f.write("c{1}: ts{0} >= 0\n".format(i, line_count()))

    for i in range(len(r)):  # 10,11
        f.write("c{2}: ts{0} = {1}\n".format(r[i], rs[i], line_count()))
        f.write("c{2}: tf{0} = {1}\n".format(r[i], rf[i], line_count()))

    for i in K:  # 11
        f.write("c{2}: tf{0} - ts{0} >= {1}\n".format(i, Pt[i - 1], line_count()))

    for i in range(2, D + 1):  # 12
        for j in MW[0]:
            f.write("c{3}: ts{0} - {1} y({2},{0}) >= 0\n".format(j, NS[i - 2] + T, i, line_count()))

    for i in range(1, D + 1):  # 13
        for j in MW[0]:
            right = -A - NS[i - 1]
            f.write("c{4}: -{0} y({1},{2}) - tf{2} >= {3}\n".format(A, i, j, right, line_count()))

    for i in Kb:  # 14
        f.write("c{}:".format(line_count()))
        for j in range(1, pallet + 1):
            f.write(" + v({0},{1})".format(i, j))
        f.write(" = 1\n")

    for i in Kb:  # 15
        for j in Kb:
            if i != j:
                for k in range(1, pallet + 1):
                    f.write(
                        "c{6}: ts{0} - tf{1} - {4} v({2},{3}) - {4} v({0},{3}) - {4} x({2},{0}) >= {5}\n"
                        .format(i, j + 2, j, k, A, -3 * A, line_count()))

    for i in range(len(Kb)):  # 16
        count = 0
        j_n = int(int(JIG[i]) / 1000 - 1)
        f.write("c{}:".format(line_count()))
        for j in dic_jig[j_n]:
            f.write(" + u({0},{1})".format(Kb[i], j))
            count += 1
        f.write(" = 1\n")

    for i in range(len(Kb)):  # 17
        jig_set = [a for a in range(1, jig_total + 1)]
        j_n_i = int(int(JIG[i]) / 1000 - 1)
        for j in dic_jig[j_n_i]:
            jig_set.remove(j)
        for k in jig_set:
            f.write("c{2}: u({0},{1}) = 0\n".format(Kb[i], k, line_count()))

    for i in range(len(Kb)):  # 18
        for j in range(len(Kb)):
            if i != j:
                j_n_i = int(int(JIG[i]) / 1000 - 1)
                j_n_j = int(int(JIG[j]) / 1000 - 1)
                for k in dic_jig[j_n_i]:
                    f.write("c{6}: ts{0} - tf{1} - {2} u({0},{3}) - {2} u({4},{3}) - {2} x({4},{0}) >= -{5}\n"
                            .format(Kb[i], Kb[j] + 2, A, k, Kb[j], 3 * A, line_count()))

    vj = []
    for i in range(len(JIG)):
        if JIG[i] == "{}000".format(len(have_jig) + 1):  # 治具がない場合 (治具数 + 1) * 1000
            vj += [i]

    vj_w = [3 * i + 1 for i in vj]

    for i in Kb:  # 19,20
        f.write("c{2}: - ts{0} + tf{0} - 22.5 phiB{0} >= {1}\n".format(i, Pt[i - 1], line_count()))
        if i in vj_w:
            f.write("c{3}: tf{0} - ts{0} - 0 phiA{1} >= {2}\n".format(i + 2, i, Pt[i + 1], line_count()))
        else:
            f.write("c{3}: tf{0} - ts{0} - 22.5 phiA{1} >= {2}\n".format(i + 2, i, Pt[i + 1], line_count()))

    for i in Kb:  # 21
        f.write("c{2}: tf{0} - ts{0} - 10 sita{0} >= {1}\n".format(i, Pt[i - 1], line_count()))

    for i in Kb:  # 27
        for j in Kb:
            if i != j:
                for k in range(1, pallet + 1):
                    f.write("c{3}: rho({0},{1},{2}) - v({0},{2}) - v({1},{2}) >= - 1\n".format(i, j, k, line_count()))

    for i in Kb:  # 28
        for j in Kb:
            if i != j:
                for k in range(1, pallet + 1):
                    f.write("c{3}: 2 rho({0},{1},{2}) - v({0},{2}) - v({1},{2}) <= 0\n".format(i, j, k, line_count()))

    for i in Kb:  # 30
        for j in Kb:
            if i != j:
                for k in range(1, pallet + 1):
                    f.write("c{3}: d({0},{1}) - v({0},{2}) - v({1},{2}) >= - 1\n".format(i, j, k, line_count()))

    for i in Kb:  # 31
        for j in Kb:
            if i != j:
                f.write("c{2}: d({0},{1})".format(i, j, line_count()))
                for k in range(1, pallet + 1):
                    f.write(" - rho({0},{1},{2})".format(i, j, k))
                f.write(" = 0\n")

    for i in Kb:
        for j in Kb:
            if i != j:
                f.write("c{2}: dR({0},{1}) + d({0},{1}) = 1\n".format(i, j, line_count()))  # 33
                f.write("c{3}: x({0},{1}) - x({2},{1}) - a({2},{1}) >= -1\n".format(i + 2, j, i, line_count()))  # 38
                f.write("c{2}: aR({0},{1}) + a({0},{1}) = 1\n".format(i, j, line_count()))  # 41
                f.write("c{2}: xJ({0},{1}) - a({0},{1}) <= 0\n".format(i, j, line_count()))  # 51
                f.write("c{2}: xJ({0},{1}) + xJ({1},{0}) <= 1\n".format(i, j, line_count()))  # 52
                f.write("c{2}: xJ({0},{1}) - x({0},{1}) <= 0\n".format(i, j, line_count()))  # 53

                f.write("c{2}: lam({0},{1}) - xp({0},{1}) - aR({0},{1}) >= -1\n".format(i, j, line_count()))  # 57
                f.write("c{2}: 2 lam({0},{1}) - xp({0},{1}) - aR({0},{1}) <= 0\n".format(i, j, line_count()))  # 58

                f.write("c{2}: kap({0},{1}) - xJ({0},{1}) - dR({0},{1}) >= -1\n".format(i, j, line_count()))  # 60
                f.write("c{2}: 2 kap({0},{1}) - xJ({0},{1}) - dR({0},{1}) <= 0\n".format(i, j, line_count()))  # 61

    for i in Kb:  # 63
        count = 0
        for j in Kb:
            if i != j:
                if count == 0:
                    f.write("c{1}: gB{0} ".format(i, line_count()))
                f.write("- lam({1},{0}) ".format(i, j))
                count += 1
        f.write("= 0\n")

    for i in Kb:  # 65
        count = 0
        for j in Kb:
            if i != j:
                if count == 0:
                    f.write("c{1}: gA{0} ".format(i, line_count()))
                f.write("- lam({0},{1}) ".format(i, j))
                count += 1
        f.write("= 0\n")

    for i in Kb:  # 67
        count = 0
        for j in Kb:
            if i != j:
                if count == 0:
                    f.write("c{1}: piB{0} ".format(i, line_count()))
                f.write("- kap({1},{0}) ".format(i, j))
                count += 1
        f.write("= 0\n")

    for i in Kb:  # 69
        count = 0
        for j in Kb:
            if i != j:
                if count == 0:
                    f.write("c{1}: piA{0} ".format(i, line_count()))
                f.write("- kap({0},{1}) ".format(i, j))
                count += 1
        f.write("= 0\n")

    for i in range(len(Kb)):
        for j in range(len(Kb)):
            if i != j:
                j_n_i = int(int(JIG[i]) / 1000 - 1)
                j_n_j = int(int(JIG[j]) / 1000 - 1)
                for k in dic_jig[j_n_i]:
                    f.write(
                        "c{3}: E({0},{1},{2}) - u({0},{2}) - u({1},{2}) >= -1\n".format(Kb[i], Kb[j], k,
                                                                                        line_count()))  # 35
                    f.write(
                        "c{3}: 2 E({0},{1},{2}) - u({0},{2}) - u({1},{2}) <= 0\n".format(Kb[i], Kb[j], k,
                                                                                         line_count()))  # 36

    for i in range(len(Kb)):  # 39
        for j in range(len(Kb)):
            if i != j:
                j_n_i = int(int(JIG[i]) / 1000 - 1)
                f.write("c{2}: a({0},{1})".format(Kb[i], Kb[j], line_count()))
                for k in dic_jig[j_n_i]:
                    f.write(" - E({0},{1},{2})".format(Kb[i], Kb[j], k))
                f.write(" = 0\n")

    for i in Kb:  # 43
        for j in Kb:
            if i != j:
                f.write("c{2}: d({0},{1}) - xp({0},{1}) >= 0\n".format(i, j, line_count()))

    for i in Kb:  # 44
        for j in Kb:
            if i != j:
                f.write("c{2}: xp({0},{1}) - x({0},{1}) <= 0\n".format(i, j, line_count()))

    for i in Kb:  # 45
        for j in Kb:
            if i != j:
                f.write("c{4}: ts{1} - tf{0} - {2} xp({3},{1}) >= -{2}\n".format(i + 2, j, A, i, line_count()))

    for i in Kb:  # 46
        for j in Kb:
            if i != j:
                f.write("c{2}: xp({0},{1}) + xp({1},{0}) <= 1\n".format(i, j, line_count()))

    for i in Kb:  # 47
        count = 0
        for j in Kb:
            if i != j:
                if count == 0:
                    f.write("c{2}: xp({0},{1}) ".format(i, j, line_count()))
                elif count < len(Kb) - 1:
                    f.write("+ xp({0},{1}) ".format(i, j))
                if count == len(Kb) - 2:
                    f.write("<= 1\n")
                count += 1

    dKb = copy.copy(Kb)
    dKb.insert(0, 0)

    for i in Kb:  # 48
        count = 0
        for j in dKb:
            if i != j:
                if count == 0:
                    f.write("c{2}: xp({0},{1})".format(j, i, line_count()))
                elif count == len(dKb) - 2:
                    f.write(" + xp({0},{1}) = 1\n".format(j, i))
                else:
                    f.write(" + xp({0},{1})".format(j, i))
                count += 1

    count = 0

    for i in Kb:  # 49
        if count == 0:
            f.write("c{1}: xp(0,{0}) ".format(i, line_count()))
        elif count == len(Kb) - 1:
            f.write("+ xp(0,{0}) <= {1}\n".format(i, pallet))
        else:
            f.write("+ xp(0,{}) ".format(i))
        count += 1

    for i in Kb:  # 54
        count = 0
        for j in Kb:
            if i != j:
                if count == 0:
                    f.write("c{2}: xJ({0},{1}) ".format(i, j, line_count()))
                elif count < len(Kb) - 1:
                    f.write("+ xJ({0},{1}) ".format(i, j))
                if count == len(Kb) - 2:
                    f.write("<= 1\n")
                count += 1

    for i in Kb:  # 55
        count = 0
        for j in dKb:
            if i != j:
                if count == 0:
                    f.write("c{2}: xJ({0},{1})".format(j, i, line_count()))
                elif count == len(dKb) - 2:
                    f.write(" + xJ({0},{1}) = 1\n".format(j, i))
                else:
                    f.write(" + xJ({0},{1})".format(j, i))
                count += 1

    for i in range(jig_total):  # 71
        f.write("c{2}: {0} tau{1} ".format(A, i + 1, line_count()))
        for j in Kb:
            f.write("- u({0},{1}) ".format(j, i + 1))
        f.write(">= 0\n")

    for i in range(jig_total):  # 72
        f.write("c{1}: tau{0} ".format(i + 1, line_count()))
        for j in Kb:
            f.write("- u({0},{1}) ".format(j, i + 1))
        f.write(" <= 0\n")

    for i in Kb:
        f.write("c{1}: 2 phiB{0} - piB{0} - gB{0} >= 0\n".format(i, line_count()))  # 74
        f.write("c{1}: 2 phiA{0} - piA{0} - gA{0} >= 0\n".format(i, line_count()))  # 76

    count = 0
    f.write('c{}: '.format(line_count()))  # 77
    for i in Kb:
        f.write("xJ(0,{0}) ".format(i))
        if count < len(Kb) - 1:
            f.write("+ ")
        count += 1
    for i in range(jig_total):
        f.write("- tau{} ".format(i + 1))
    f.write("<= 0\n")

    # シータを定義する式
    for i in Kb:  # 79
        for j in Kb:
            if i != j:
                tmp = -2
                if hs[i] != hs[j]:
                    tmp += 1
                f.write("c{3}: eta({1},{0}) - xp({1},{0}) - a({1},{0}) >= {2}\n".format(j, i, tmp, line_count()))

    for i in Kb:  # 80
        for j in Kb:
            if i != j:
                tmp = 0
                if hs[i] != hs[j]:
                    tmp = 1
                f.write("c{3}: 3 eta({1},{0}) - xp({1},{0}) - a({1},{0}) <= {2}\n".format(j, i, tmp, line_count()))

    for i in Kb:  # 82
        count = 0
        for j in Kb:
            if i != j:
                if count == 0:
                    f.write("c{1}: sita{0} ".format(i, line_count()))
                f.write("- eta({1},{0}) ".format(i, j))
                count += 1
        f.write("= 0\n")

    ################################################################################################################
    ################################################################################################################
    f.write("binary\n")
    for i in range(M):
        for j in rMW[i]:
            for k in rMW[i]:
                if j != k:
                    f.write("x({0},{1})\n".format(j, k))

    for i in range(1, D + 1):
        for j in MW[0]:
            f.write("y({0},{1})\n".format(i, j))

    for i in Kb:
        for j in range(1, pallet + 1):
            f.write("v({0},{1})\n".format(i, j))

    for i in Kb:
        for j in range(1, jig_total + 1):
            f.write("u({0},{1})\n".format(i, j))

    for i in Kb:
        f.write("xp(0,{})\n".format(i))
        f.write("xJ(0,{})\n".format(i))
        for j in Kb:
            if i != j:
                f.write("a({0},{1})\n".format(i, j))
                f.write("aR({0},{1})\n".format(i, j))
                f.write("xp({0},{1})\n".format(i, j))
                f.write("d({0},{1})\n".format(i, j))
                f.write("dR({0},{1})\n".format(i, j))
                f.write("xJ({0},{1})\n".format(i, j))
                f.write('lam({0},{1})\n'.format(i, j))
                f.write('kap({0},{1})\n'.format(i, j))
                f.write('eta({0},{1})\n'.format(i, j))
                for k in range(1, pallet + 1):
                    f.write("rho({0},{1},{2})\n".format(i, j, k))

    for i in range(len(Kb)):  # 19''-3
        for j in range(len(Kb)):
            if i != j:
                j_n_i = int(int(JIG[i]) / 1000 - 1)
                for k in dic_jig[j_n_i]:
                    f.write("E({0},{1},{2})\n".format(Kb[i], Kb[j], k))

    for i in Kb:
        f.write("gA{0}\n".format(i))
        f.write("gB{0}\n".format(i))
        f.write("piA{0}\n".format(i))
        f.write("piB{0}\n".format(i))
        f.write("phiA{0}\n".format(i))
        f.write("phiB{0}\n".format(i))
        f.write("sita{0}\n".format(i))

    for i in range(jig_total):
        f.write("tau{}\n".format(i + 1))

    f.write("end")

    f.close()


if __name__ == '__main__':
    write_lp(None, "prob_test.lp", "work_test.txt", "jig_origin.csv")
