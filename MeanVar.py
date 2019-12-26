#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from cvxopt import matrix, solvers

from Stock import Stock

# stock_num = 10
# expect_ret = 0.4


def min_val(stock_num, expect_ret, covs, rets, stock_name):

    assert np.array(covs).shape == (stock_num, stock_num)
    print(np.linalg.eigvals(np.array(covs)))
    assert np.all(np.linalg.eigvals(np.array(covs)) >= 0), '保证正定矩阵'
    P = matrix(np.array(covs) * 2)
    print(P)
    q = matrix(np.zeros(stock_num))
    G = matrix(np.insert(np.identity(stock_num), 0, values=np.array(rets), axis=0) * (-1))

    A = matrix(np.ones(stock_num), (1, stock_num))
    b = matrix(np.ones(1))

    h = matrix(np.insert(np.zeros(stock_num), 0, values=-1*expect_ret, axis=0))
    result = solvers.qp(P, q, G, h, A, b)
    weight = np.array(result['x'])
    max_list = weight.transpose().argsort()
    print(weight)
    print("最高权重股票：", stock_name[max_list[0][-1]])
    print("股票权重：", weight[max_list[0][-1]])
    print("期望收益率：", rets[max_list[0][-1]])
    return weight


def cal_var(weight, covs):
    return np.dot(np.matmul(np.transpose(weight), covs), weight).squeeze().squeeze()


def cal_ret(weight, rets):
    return np.dot(rets, weight).squeeze().squeeze()


if __name__ == "__main__":

    ss = Stock()
    ss.load()
    ss.pick_10()

    # # 高收益型投资方案
    # # 期望收益率下限为30%
    # w = min_val(20, 0.3, ss.cov_10, ss.expect_RE_10, ss.stock_name_10)
    # w = np.where(w > 1e-7, w, 0)
    # print(w)
    # print(cal_var(w, np.array(ss.cov_10)))
    # print(cal_ret(w, np.array(ss.expect_RE_10)))
    # print(ss.stock_name_10)
    # print(ss.cost_10)

    # 稳健型投资方案
    w_old = min_val(20, 0.25, ss.cov_10, ss.expect_RE_10, ss.stock_name_10)
    w = np.where(w_old > 1e-6, w_old, 0)
    print(w)
    print('股票名称      ', '投资金额(单位/万元)', '投资比例')
    for i in range(20):
        print(ss.stock_name_10[i], str(w[i] * 10000).ljust(16), w[i])
    print('-------------------')
    print('预期收益：0.25')
    print('投资风险：', cal_var(w, np.array(ss.cov_10)))
    print('投资收益率：', cal_ret(w, np.array(ss.expect_RE_10)))

    # # 中等型投资方案
    # w = min_val(20, 0.22, ss.cov_10, ss.expect_RE_10, ss.stock_name_10)
    # w = np.where(w > 1e-6, w, 0)
    # print(w)
    # print(cal_var(w, np.array(ss.cov_10)))
    # print(cal_ret(w, np.array(ss.expect_RE_10)))
    # print(ss.stock_name_10)
    # print(ss.cost_10)

    # 画图部分
    # var_list = []
    # ret_list = []
    # for k in np.arange(0, 0.32, 0.02):
    #     w = min_val(10, k, ss.cov_10, ss.expect_RE_10, ss.stock_name_10)
    #     var_list.append(cal_var(w, np.array(ss.cov_10)))
    #     ret_list.append(cal_ret(w, np.array(ss.expect_RE_10)))
    # print(ss.stock_name_10)
    #
    # sim_var_list = []
    # sim_ret_list = []
    # sim_weight = np.random.uniform(0, 1, (100000, 10))
    # sim_weight = np.apply_along_axis(lambda x: x / sum(x), 1, sim_weight)
    # print(sim_weight)
    # for tmp_w in sim_weight:
    #     sim_var_list.append(cal_var(tmp_w, np.array(ss.cov_10)))
    #     sim_ret_list.append(cal_ret(tmp_w, np.array(ss.expect_RE_10)))
    #
    # plt.figure(figsize=(8, 5))
    # plt.plot(var_list, ret_list, 'ro')
    # plt.plot(sim_var_list, sim_ret_list, 'b.')
    # plt.grid(True)
    # plt.xlabel('var')
    # plt.ylabel('returns')
    # plt.show()