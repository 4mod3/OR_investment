#!/usr/bin/python
import os
import numpy as np
import pandas as pd



class Stock(object):

    # 初始化变量
    stock_num = 20
    stock_name_list = [0]*50
    stock_dir_list = [0]*50
    adj_close = pd.DataFrame()
    adj_close_10 = pd.DataFrame()
    expect_RE_50 = [0]*50
    daily_SD_10 = [0] * stock_num
    daily_SD_50 = [0] * 50
    expect_RE_10 = [0] * stock_num
    cost_10 = [0] * stock_num
    stock_name_10 = [0]*stock_num
    cov_10 = pd.DataFrame()
    cov_50 = pd.DataFrame()

    def __init__(self):
        pass

    def load(self, path='./StockDir'):
        if not os.path.exists(path):
            raise ValueError

        self.stock_dir_list = os.listdir(path)
        for i, stock_name in enumerate(self.stock_dir_list):
            self.stock_name_list[i] = (stock_name.split('.ss')[0])

        for i, stock_dir in enumerate(self.stock_dir_list):
            raw_data = pd.read_csv('./StockDir/{}'.format(stock_dir), index_col='Date')
            self.adj_close[i] = raw_data['Adj Close']
            self.expect_RE_50[i] = (raw_data['Adj Close'][-1] - raw_data['Adj Close'][0])/raw_data['Adj Close'][0]

    def pick_10(self):
        arr_index = np.argsort(self.expect_RE_50)
        for i in range(self.stock_num):
            self.adj_close_10[i] = self.adj_close[arr_index[-i - 1]]
            self.daily_SD_10[i] = self.adj_close[arr_index[-i - 1]].std()
            self.expect_RE_10[i] = self.expect_RE_50[arr_index[-i-1]]
            self.cost_10[i] = self.adj_close[arr_index[-i - 1]][-1]*100
            self.stock_name_10[i] = self.stock_name_list[arr_index[-i-1]]
        self.cov_10 = self.adj_close_10.cov()

    def cal_all(self):
        self.cov_50 = self.adj_close.cov()
        print(self.cov_50)
        self.daily_SD_50 = self.adj_close.std()
