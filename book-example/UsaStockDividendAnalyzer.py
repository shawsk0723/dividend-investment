"""
UsaStockDividendAnalyzer

    date: 20221218
    author: 코드장인
"""

import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_percentage(input, min, max):
    return round((input - min) / (max - min) * 100)

def calculate_buy_score(current_div_yield, div_min, div_max):
    buy_score = get_percentage(current_div_yield, div_min, div_max)
    return buy_score

class UsaStockDividendAnalyzer:
    def __init__(self, ticker, period):
        self.ticker = ticker
        self.period = period
        self.result = pd.DataFrame()

    def fit(self):
        try:
            ticker = self.ticker
            period = self.period

            print(f'ticker = {ticker}')
            stock_basic_info = yf.Ticker(ticker).info
            end_date = datetime.now().strftime("%Y-%m-%d")
            #print("end date: " , end_date)
            start_date = (datetime.now() - relativedelta(years=period)).strftime("%Y-%m-%d")
            #print("start date: ", start_date)

            dividends = stock_info.get_dividends(ticker, start_date=start_date, end_date=end_date)

            self.result = dividends.drop('ticker', axis=1)

            stock_data = yf.download(ticker, start_date, end_date)

            df_close_price = stock_data.loc[dividends.index]['Close']

            self.result['close'] = df_close_price

            div_freq = round(len(self.result.index)/period)

            self.result['div yield'] = round(self.result['dividend']*div_freq / self.result['close'] * 100, 2)

            div_min = min(self.result['div yield'])
            div_max = max(self.result['div yield'])

            buy_price = self.result['dividend'][-1] * div_freq * 100 / div_min
            sell_price = self.result['dividend'][-1] * div_freq * 100 / div_max

            current_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            current_price = stock_data.iloc[-1]['Close']

            last_dividend = self.result.iloc[-1]['dividend']
            self.current_dividend = last_dividend * div_freq
            self.current_div_yield = round(self.current_dividend/current_price*100, 2)

            self.buy_score = calculate_buy_score(self.current_div_yield, div_min, div_max)
            #print(f'buy score = {buy_score}\nsell score = {sell_score}')
        except Exception as e:
            raise(e)

    def getBuyScore(self):
        return self.buy_score

    def getCurrentDividend(self):
        return self.current_dividend

    def getCurrentDividendYield(self):
        return self.current_div_yield

    def getResult(self):
        return self.result

    def getTicker(self):
        return self.ticker


if __name__ == '__main__':
    usaStockDividendAnalyzer = UsaStockDividendAnalyzer('O', 7)
    usaStockDividendAnalyzer.fit()
    buyScore = usaStockDividendAnalyzer.getBuyScore()
    print(f'buyScore = {buyScore}')