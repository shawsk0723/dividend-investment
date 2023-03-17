"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

from tkinter import messagebox
from ExpiryChecker import *
import Config


CAFE_URL = 'https://cafe.naver.com/codegarage'
BLOG_URL = 'https://blog.naver.com/shawgibal'

def showAbout():
    aboutMsg = f"{Config.WIN_TITLE}\n\n"
    aboutMsg += "제작자: 코드장인\n\n"
    aboutMsg += f"카페: {CAFE_URL}\n\n"
    aboutMsg += f"블로그: {BLOG_URL}\n\n"
    #aboutMsg += f"유효 기간: {HardExpiryChecker().getExiryDate()}"
    messagebox.showinfo(title=Config.APP_NAME, message=aboutMsg)