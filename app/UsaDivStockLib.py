import os
import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import time

def makeDirIfNotExist(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except Exception as e:
        LOG(str(e))

class StockBasicInfo:
    def __init__(self, ticker):
        self.stock_stats = stock_info.get_stats(ticker)

    def getRoe(self):
        return self.__getValueByAttribute('Return on Equity (ttm)')

    def getPayoutRatio(self):
        return self.__getValueByAttribute('Payout Ratio 4')

    def getDividendYield(self):
        return self.__getValueByAttribute('Forward Annual Dividend Yield 4')

    def __getValueByAttribute(self, attribute):
        try:
            stock_stats = self.stock_stats
            value = stock_stats['Value'][stock_stats['Attribute'] == attribute].values[0]
            value = value.replace('%', '')
            return float(value)
        except Exception as e:
            print(e)
            return 'N/A'

class StockDivDataCollector:
    def __init__(self):
        pass
        #self.ticker = ticker
        #self.periods = periods

    def collect(self, ticker, periods=7):
        end_date = datetime.now().strftime("%Y-%m-%d")
        print("end date: " , end_date)
        start_date = (datetime.now() - relativedelta(years=periods)).strftime("%Y-%m-%d")
        print("start date: ", start_date)

        stock_div_data = stock_info.get_dividends(ticker, start_date=start_date, end_date=end_date)
        stock_div_data.drop(['ticker'], axis=1, inplace=True)

        # Get stock price data
        stock_price_data = yf.download(ticker, start_date, end_date)
        df_close_price = stock_price_data.loc[stock_div_data.index]['Close']
        stock_div_data['close'] = df_close_price

        div_freq = round(len(stock_div_data.index)/periods)
        div_yield = stock_div_data['dividend']*div_freq / stock_div_data['close'] * 100
        div_yield = round(div_yield, 2)
        stock_div_data['div yield'] = div_yield
        self.stock_div_data = stock_div_data
        return self.stock_div_data

class UsaDivStockPricer:
    def __init__(self, stockDivData):
        self.stockDivData = stockDivData

    def getBuyScore(self, current_div_yield):
        div_min = min(self.stockDivData['div yield'])
        div_max = max(self.stockDivData['div yield'])
        self.buyScore = self.__calculate_buy_score(current_div_yield, div_min, div_max)
        return self.buyScore
        
    def __get_percentage(self, input, min, max):
        return round((input - min) / (max - min) * 100)

    def __calculate_buy_score(self, current_div_yield, div_min, div_max):
        buy_score = self.__get_percentage(current_div_yield, div_min, div_max)
        return buy_score

def saveDivAnalysisChart(ticker, dividends, current_div_yield, img_file_path_to_save):
    div_min = min(dividends['div yield'])
    div_max = max(dividends['div yield'])
    
    plt.plot(dividends['div yield'],  color='b', label = 'dividend history')
    plt.axhline(y=div_min, color='y', linestyle='--', label='min div yield')
    plt.axhline(y=div_max, color='r', linestyle='--', label='max div yield')
    plt.axhline(y=current_div_yield, color='g', linestyle='--', label='current div yield')
    plt.title(f'{ticker} dividend analysis')
    plt.xlabel('year')
    plt.ylabel('dividend yield')
    plt.legend()
    plt.savefig(img_file_path_to_save)
    plt.close()