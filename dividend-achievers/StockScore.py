import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings('ignore')

def _get_percentage_(input, min, max):
    return round((input - min) / (max - min) * 100)

def _calculate_buy_score_(current_div_yield, div_min, div_max):
    buy_score = _get_percentage_(current_div_yield, div_min, div_max)
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
        buy_score = _calculate_buy_score_(current_div_yield, div_min, div_max)
        return current_dividend, current_div_yield, buy_score
    except Exception as e:
        raise(e)