"""
StockAnalyzerEvent

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""


STOCK_ANALYSIS_OK_EVENT = 1
STOCK_ANALYSIS_FAIL_EVENT = 2

ANALYZER_FINISH_EVENT = 10


class StockAnalyzerEvent:
    def __init__(self, event, data):
          self.event = event
          self.data = data

    def getEvent(self):
         return self.event
    
    def getData(self):
         return self.data