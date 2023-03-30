"""
StockBasicInfo
"""

import traceback
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
from yahoo_fin import stock_info
import time
import numpy as np

class StockBasicInfo:
    def __init__(self, ticker):
        self.stock_stats = stock_info.get_stats(ticker)

        stock = yf.Ticker(ticker)
        self.stock_info = stock.history(period='1d')

    def getRoe(self):
        return self.__getValueByAttribute('Return on Equity (ttm)')

    def getPayoutRatio(self):
        return self.__getValueByAttribute('Payout Ratio 4')

    def getDividendDate(self):
        return self.__getStrValueByAttribute('Dividend Date 3')

    def getExDividendDate(self):
        return self.__getStrValueByAttribute('Ex-Dividend Date 4')    
 
    def getDividend(self):
        return self.__getValueByAttribute('Forward Annual Dividend Rate 4')

    def getDividendYield(self):
        return self.__getValueByAttribute('Forward Annual Dividend Yield 4')
    
    def getCurrentPrice(self):
        return round(self.stock_info.Close, 2)
    
    def __getValueByAttribute(self, attribute):
        try:
            stock_stats = self.stock_stats
            value = stock_stats['Value'][stock_stats['Attribute'] == attribute].values[0]
            print(f'{attribute} = {value}')
            if value is np.nan:
                return 'N/A'
            value = value.replace('%', '')
            return float(value)
        except Exception as e:
            traceback.format_exc(e)
            return 'N/A'
        
    def __getStrValueByAttribute(self, attribute):
        try:
            stock_stats = self.stock_stats
            value = stock_stats['Value'][stock_stats['Attribute'] == attribute].values[0]
            print(f'{attribute} = {value}')
            return value
        except Exception as e:
            traceback.format_exc(e)
            return 'N/A'
        
        
def get_percentage(input, min, max):
    return round((input - min) / (max - min) * 100)

def calculate_buy_score(current_div_yield, div_min, div_max):
    buy_score = get_percentage(current_div_yield, div_min, div_max)
    return buy_score

def getBuyScore(ticker, periods=7):
    try:
        print(f'ticker = {ticker}')
        stock_basic_info = yf.Ticker(ticker).info
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - relativedelta(years=periods)).strftime("%Y-%m-%d")
        dividends = stock_info.get_dividends(ticker, start_date=start_date, end_date=end_date)
        result = dividends.drop('ticker', axis=1)
        stock_data = yf.download(ticker, start_date, end_date)
        df_close_price = stock_data.loc[dividends.index]['Close']
        result['close'] = df_close_price
        div_freq = round(len(result.index)/periods)
        result['div yield'] = round(result['dividend']*div_freq / result['close'] * 100, 2)
        div_min = min(result['div yield'])
        div_max = max(result['div yield'])
        buy_price = result['dividend'][-1] * div_freq * 100 / div_min
        sell_price = result['dividend'][-1] * div_freq * 100 / div_max
        current_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        current_price = stock_data.iloc[-1]['Close']
        last_dividend = result.iloc[-1]['dividend']
        current_dividend = last_dividend * div_freq
        current_div_yield = round(current_dividend/current_price*100, 2)
        buy_score = calculate_buy_score(current_div_yield, div_min, div_max)
        return current_dividend, current_div_yield, buy_score
    except Exception as e:
        traceback.format_exc(e)        
        return 'N/A'
