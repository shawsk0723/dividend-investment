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

def calculate_buysell_score(current_div_yield, div_min, div_max):
    buy_score = get_percentage(current_div_yield, div_min, div_max)
    sell_score = 100 - buy_score
    return buy_score, sell_score


class UsaStockDividendAnalyzer:
    def __init__(self, ticker, period):
        self.ticker = ticker
        self.period = period

    def fit(self):
        try:
            ticker = self.ticker
            period = self.period

            print(f'ticker = {ticker}')
            stock_basic_info = yf.Ticker(ticker).info
            end_date = datetime.now().strftime("%Y-%m-%d")
            #print("start date: " , end_date)
            start_date = (datetime.now() - relativedelta(years=period)).strftime("%Y-%m-%d")
            #print("end date: ", start_date)

            dividends = stock_info.get_dividends(ticker, start_date=start_date, end_date=end_date)

            stock_data = yf.download(ticker, start_date, end_date)

            df_close_price = stock_data.loc[dividends.index]['Close']

            dividends['close'] = df_close_price

            dividends = dividends.drop('ticker', axis=1)

            div_freq = round(len(dividends.index)/period)

            dividends['div yield'] = round(dividends['dividend']*div_freq / dividends['close'] * 100, 2)

            div_min = min(dividends['div yield'])
            div_max = max(dividends['div yield'])

            buy_price = dividends['dividend'][-1] * div_freq * 100 / div_min
            sell_price = dividends['dividend'][-1] * div_freq * 100 / div_max

            current_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            current_price = stock_data.iloc[-1]['Close']

            last_dividend = dividends.iloc[-1]['dividend']
            self.current_dividend = last_dividend * div_freq
            self.current_div_yield = round(self.current_dividend/current_price*100, 2)

            self.buy_score, self.sell_score = calculate_buysell_score(self.current_div_yield, div_min, div_max)
            #print(f'buy score = {buy_score}\nsell score = {sell_score}')
        except Exception as e:
            raise(e)
        
    def getBuyScore(self):
        return self.buy_score

    def getSellScore(self):
        return self.sell_score
    
    def getCurrentDividend(self):
        return self.current_dividend
    
    def getCurrentDividendYield(self):
        return self.current_div_yield