"""
UsaDivStockAnalyzer

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import os
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

        for ticker in self.tickerList:
            try:
                self.ticker = ticker
                self.root.__updateStatusText__('*****************')
                self.root.__updateStatusText__(f'{ticker}')
                self.root.__updateStatusText__(f'분석을 시작합니다.')

                # collect fundamental data
                self.root.__updateStatusText__(f'펀더멘탈 데이터를 수집합니다.')

                stockBasicInfo = StockBasicInfo(ticker)
                self.cur_div_yield  = stockBasicInfo.getDividendYield()
                div_yields.append(self.cur_div_yield)
                print(f'cur_div_yield = {self.cur_div_yield}')

                payout_ratios.append(stockBasicInfo.getPayoutRatio())
                roes.append(stockBasicInfo.getRoe())

                # collect dividend data
                self.root.__updateStatusText__(f'배당금 데이터를 수집합니다.')

                stockDivDataCollector = StockDivDataCollector()
                self.stock_div_data = stockDivDataCollector.collect(ticker)

                # estimate stock price
                self.root.__updateStatusText__(f'적정 가격을 분석합니다.')

                usaDivStockPricer = UsaDivStockPricer(self.stock_div_data)
                buy_score = usaDivStockPricer.getBuyScore(self.cur_div_yield)
                buy_scores.append(buy_score)
                print(f'buy_score = {buy_score}')

                self.root.tickerAnalysisCb(self.ticker, True)

                time.sleep(2)    

            except Exception as e:
                LOG(str(e))

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

    def saveAnalysisChartImage(self, chartDir):
        # save price div chart by image file
        chartFilePath = os.path.join(chartDir, self.ticker)
        saveDivAnalysisChart(self.ticker, self.stock_div_data, self.cur_div_yield, chartFilePath)

        # To-Do: save analysis result to excel file

