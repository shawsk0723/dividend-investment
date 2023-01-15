from yahoo_fin import stock_info


class StockBasicInfo:
    def __init__(self, ticker):
        try:
            self.ticker = ticker
            self.stock_stats = stock_info.get_stats(ticker)
        except Exception as e:
            raise(e)
            
    def getRoe(self):
        try:
            stock_stats = self.stock_stats
            roe = stock_stats['Value'][stock_stats['Attribute'] == 'Return on Equity (ttm)'].values[0]
            return roe
        except Exception as e:
            print(e)
            return 'N/A'
        
    def getPayoutRatio(self):
        try:
            stock_stats = self.stock_stats
            payout_ratio = stock_stats['Value'][stock_stats['Attribute'] == 'Payout Ratio 4'].values[0]
            return payout_ratio
        except Exception as e:
            print(e)
            return 'N/A'
