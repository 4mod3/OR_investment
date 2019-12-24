#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cvxopt import matrix, solvers

from Stock import Stock

# stock_num = 10
# expect_ret = 0.4


def min_val(stock_num, expect_ret, covs, rets, stock_name):

    assert np.array(covs).shape == (stock_num, stock_num)
    assert np.all(np.linalg.eigvals(np.array(covs)) > 0), '保证正定矩阵'
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


if __name__ == "__main__":

    ss = Stock()
    ss.load()
    ss.pick_10()
    for k in np.arange(0, 1, 0.05):
        min_val(10, k, ss.cov_10, ss.expect_RE_10, ss.stock_name_10)
        print(k)
    print(ss.stock_name_10)
