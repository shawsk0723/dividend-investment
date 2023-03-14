"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import pandas as pd


class StockLister:
    def __init__(self, filePath, stockCodeKey):
        self.filePath = filePath
        self.stockCodeKey = stockCodeKey

    def getFirstStockCode(self):
        try:
            df = pd.read_csv(self.filePath)
            stockCodeKey = self.stockCodeKey
            return df[stockCodeKey].to_list()[0]
        except Exception as e:
            print(str(e))
            return ""

    def getStockCodeList(self):
        try:
            df = pd.read_csv(self.filePath)
            stockCodeKey = self.stockCodeKey
            return df[stockCodeKey].to_list()
        except Exception as e:
            print(str(e))
            return []


def getDefaultStockCode():
    try:
        df = pd.read_csv('./data/stocklist.csv')
        return df.Ticker.to_list()[0]
    except Exception as e:
        print(str(e))
        return ""

def getStockCodeList():
    try:
        df = pd.read_csv('./data/stocklist.csv')
        return df.Ticker.to_list()
    except Exception as e:
        print(str(e))
        return ""


if __name__ == '__main__':
    stockLister = StockLister('./data/stocklist.csv', 'Ticker')
    defaultStockCode = stockLister.getFirstStockCode()
    print(f'defaultStockCode = {defaultStockCode}')
    stockCodeList = stockLister.getStockCodeList()
    print(f'stockCodeList = {stockCodeList}')

    """
    defaultStockCode = getDefaultStockCode()
    print(f'defaultStockCode = {defaultStockCode}')
    stockCodeList = getStockCodeList()
    print(f'stockCodeList = {stockCodeList}')
    """