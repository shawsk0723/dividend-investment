"""
DivAchievers

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import pandas as pd

class DivAchievers:
    def __init__(self):
        self.df = pd.read_csv('./data/dividend_achievers.csv')

    def getFiveYearDivGrowthRate(self, ticker):
        if not self.isTickerAvailable(ticker):
            raise Exception('ticker is not available~')

        fiveYearDivGrowthRate = self.df['5-Year Dividend Growth (Annualized)'][self.df['Ticker'] == ticker].values[0]
        return fiveYearDivGrowthRate

    def getCurDivYield(self, ticker):
        if not self.isTickerAvailable(ticker):
            raise Exception('ticker is not available~')

        curDivYield = self.df['Dividend Yield'][self.df['Ticker'] == ticker].values[0]
        return curDivYield    
    
    def isTickerAvailable(self, ticker):
        return ticker in self.df['Ticker'].values
    

def getFutureDividend(capital, cur_div_yield, interest_rate, years):
    futureDividends = []
    #utureDividends.append(round(capital * cur_div_yield))
    for year in range(1, years+1):
        futureDividend = capital * cur_div_yield * ((1+ interest_rate)**year)
        futureDividends.append(round(futureDividend))
    return futureDividends   