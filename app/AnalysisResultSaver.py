"""
AnalysisResultSaver

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import pandas as pd

def saveAnalsisResultToCsv(result, outFilePath):
    df = pd.DataFrame(result)
    df.to_csv(outFilePath, index=False)