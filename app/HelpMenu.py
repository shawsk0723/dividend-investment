"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

from tkinter import messagebox
import Config
from ExpiryChecker import *

def showAbout():
    aboutMsg = f"{Config.WIN_TITLE}\n\n"
    aboutMsg += "제작자: 코드장인\n\n"
    aboutMsg += f"유효 기간: {HardExpiryChecker().getExiryDate()}"
    messagebox.showinfo(message=aboutMsg)