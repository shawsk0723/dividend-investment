"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import pandas as pd
import Config

class StockLister:
    def __init__(self, filePath=Config.STOCK_LIST_FILE_PATH, stockCodeKey='Ticker'):
        self.filePath = filePath
        self.stockCodeKey = stockCodeKey

    def getStockFilePath(self):
        return self.filePath

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
        df = pd.read_csv(Config.STOCK_LIST_FILE_PATH)
        return df.Ticker.to_list()[0]
    except Exception as e:
        print(str(e))
        return ""

def getStockCodeList():
    try:
        df = pd.read_csv(Config.STOCK_LIST_FILE_PATH)
        return df.Ticker.to_list()
    except Exception as e:
        print(str(e))
        return ""


if __name__ == '__main__':
    stockLister = StockLister(Config.STOCK_LIST_FILE_PATH, 'Ticker')
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