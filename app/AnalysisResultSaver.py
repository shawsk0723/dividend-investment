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

    df_cleaned = df.loc[df['buy score'] != "N/A" ]
    df_sorted = df_cleaned.sort_values('buy score', ascending=False)
    df_sorted.to_csv(outFilePath.replace('.csv', '_sorted_buyscore.csv'), index=False)