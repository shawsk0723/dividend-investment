"""
UsaDivStockAnalyzer

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import os
import time
import traceback
from tkinter import *            # tkinter 라이브러리에 모든 함수를 사용
from StockAnalyzer import StockAnalyzer

import Config
import logging
from UsaDivStockLib import *

def LOG(msg):
    logging.debug(msg)


class UsaDivStockAnalyzer(StockAnalyzer):
    def __init__(self, root, tickerList):
        self.root = root
        self.tickerList = tickerList
        self.analysisResult = {}

        if Config.__APP_GRADE__ == Config.FREE:
            self.delay = 10
        else:
            self.delay = 2

    def execute(self):
        LOG('StockAnalyzer Start...')

        # GUI 업데이트
        self.root.startButton['state'] = DISABLED
        self.root.progressbar.start(10)
        self.root.statusText.delete(1.0, END)

        div_yields = []
        payout_ratios = []
        roes = []
        buy_scores = []

        self.root.__updateStatusText__(f'분석을 시작합니다.')
        self.root.__updateStatusText__('*'*50)

        totalStockNum = len(self.tickerList)
        for idx, ticker in enumerate(self.tickerList):
            try:
                self.root.__updateStatusText__(f'{ticker}')

                # collect fundamental data
                self.root.__updateStatusText__(f'펀더멘탈 데이터를 수집합니다.')

                stockBasicInfo = StockBasicInfo(ticker)
                self.cur_div_yield  = stockBasicInfo.getDividendYield()
                div_yields.append(self.cur_div_yield)
                LOG(f'cur_div_yield = {self.cur_div_yield}')

                self.payout_ratio = stockBasicInfo.getPayoutRatio()
                payout_ratios.append(self.payout_ratio)
                LOG(f'payout_ratio = {self.payout_ratio}')

                self.roe = stockBasicInfo.getRoe()
                roes.append(self.roe)
                LOG(f'roe = {self.roe}')

                # collect dividend data
                self.root.__updateStatusText__(f'배당금 데이터를 수집합니다.')

                stockDivDataCollector = StockDivDataCollector()
                self.stock_div_data = stockDivDataCollector.collect(ticker)

                # estimate stock price
                self.root.__updateStatusText__(f'적정 가격을 분석합니다.')

                usaDivStockPricer = UsaDivStockPricer(self.stock_div_data)
                self.buy_score = usaDivStockPricer.getBuyScore(self.cur_div_yield)
                buy_scores.append(self.buy_score)
                LOG(f'buy_score = {self.buy_score}')

                index = str(idx+1).zfill(3)
                totalStockNum = str(totalStockNum).zfill(3)
                self.root.tickerAnalysisCb(ticker = ticker,
                                            cur_div_yield = self.cur_div_yield,
                                            stock_div_data = self.stock_div_data.copy())
                time.sleep(self.delay)    
                self.root.__updateStatusText__(f'[*****************100%*******************] {index}/{totalStockNum} 완료하였습니다.')

            except Exception as e:
                LOG(str(e))
                LOG(traceback.format_exc())
                time.sleep(self.delay)   

        self.analysisResult['Ticker'] = self.tickerList
        self.analysisResult['div yield'] = div_yields
        self.analysisResult['payout ratio'] = payout_ratios
        self.analysisResult['roe'] = roes
        self.analysisResult['buy score'] = buy_scores

        self.root.analysisCompleteCb(True)

        # GUI 업데이트
        self.root.startButton['state'] = NORMAL
        self.root.progressbar.stop()
        LOG('StockAnalyzer Stop...')

    def saveAnalysisChartImage(self, ticker, chartDir):
        # save price div chart by image file
        chartFilePath = os.path.join(chartDir, ticker)
        saveDivAnalysisChart(ticker, self.stock_div_data, self.cur_div_yield, chartFilePath)

        # To-Do: save analysis result to excel file

