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
    def __init__(self, event, message):
          self.event = event
          self.message = message

    def getEvent(self):
         return self.event
    
    def getMessage(self):
         return self.message