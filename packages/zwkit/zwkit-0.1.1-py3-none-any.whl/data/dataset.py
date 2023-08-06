import pandas as pd
import pywencai as wc
import tushare as ts
import os
from kit import numkit

'''
数据函数
'''


class dataset_loader:
    """
    数据加载器
    通过问财获得股票列表
    通过tushare获得股票数据
    """
    def __init__(self, question, start, end, token):
        self.question = question
        self.start = start
        self.end = end
        self.token = token
        self.symbols_list = None  # 股票列表
        self.symbol_index = dict()  # 股票时间索引
        self.filter_symbols = set()
        self.data = pd.DataFrame()
        pass

    def __daily_data(self, symbol, start, end):
        """
        获取日线数据
        :param symbol:
        :param start:
        :param end:
        :return:
        """
        api = ts.pro_api(self.token)
        df = ts.pro_bar(
            ts_code=symbol,
            api=api,
            start_date=start + "0101",
            end_date=end + "1231",
            asset="E",
            freq="D",
            adj="hfq",
        )
        return df[::-1]

    def __daily(self, start_date, end_date, symbols=[]):
        """
        获取日线数据
        :param start_date:
        :param end_date:
        :param symbols:
        :return:
        """
        result = pd.DataFrame()
        if len(symbols) == 0:
            return pd.DataFrame()
        for symbol in symbols:
            df = self.__daily_data(symbol, start_date, end_date)
            result = pd.concat([result, df])
        return result

    def filter_symbols(self, symbols: list):
        """
        过滤数据列表
        :param symbols: 以列表的形式填入股票代码
        :return:
        """
        symbols = set(symbols)
        self.filter_symbols.add(symbols)

    def __get_symbols_by_wc(self, question, columns=[]):
        """
        股票列表
        通过问财获得股票列表
        """
        result = pd.DataFrame()
        for i in range(self.start, self.end):
            question = question % (i, i - 1)
            data = wc.get(question=question, loop=True)
            data = data[columns]
            data = data[~data['股票代码'].isin(self.filter_symbols)]
            data['trade_date'] = i
            result = pd.concat([result, data])
        self.symbols_list = result
        return result

    def get_data(self, data_path='data/data.csv'):
        """
        获取总数据集
        优先在本地读取，如果本地没有从互联网获取
        :param data_path: 默认的数据集路径
        :return:
        """
        if os.path.exists(data_path):
            self.data = pd.read_csv(data_path)
        else:
            symbols_list = self.__get_symbols_by_wc(self.question, columns=['股票代码'])
            for symbol in symbols_list['股票代码'].unique():
                # 获取股票代码的符合的年数据
                symbol_data = symbols_list[symbols_list['股票代码'] == symbol]
                # 获取股票代码的年数据的时间集合
                self.symbol_index.update({symbol: numkit.date_split(symbol_data)})
                pd.concat([self.data, self.__daily_data(symbol, self.start, self.end)])
        return self.data

    def observe(self):
        """
        观察数据集
        :return:
        """
        pass