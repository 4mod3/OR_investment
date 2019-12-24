import numpy as np
import os
import pandas as pd


class Stock(object):

    stock_name_list = [0]*50
    stock_dir_list = [0]*50
    daily_SD = [0]*50
    expect_RE = [0]*50
    cost = [0]*50

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
            #print(raw_data['Adj Close'][-1])
            self.daily_SD[i] = raw_data['Adj Close'].std()
            self.expect_RE[i] = (raw_data['Adj Close'][-1] - raw_data['Adj Close'][0])/*100
            self.cost[i] = raw_data['Adj Close'][-1]*100
        print(self.expect_RE)
        print(self.daily_SD)


ss = Stock()
ss.load()