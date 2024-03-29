"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import os
from tkinter import *
from tkinter import messagebox
import tkinter.ttk
import queue
import traceback

import Config
import AppUtil
from ExpiryChecker import *
from AppLogger import LOG
import WebSiteOpener
from KorDivStockAnalyzer import KorDivStockAnalyzer
from UsaDivStockAnalyzer import UsaDivStockAnalyzer
from WorkerThread import WorkerThread
from StockAnalyzerEvent import *
from ResultDisplayWindow import ResultDisplayWindow
import AnalysisResultSaver
import UserSettings
import HelpMenu

import UsaDivStockLib

"""
App config
"""

WIN_SIZE = Config.WIN_SIZE
WIN_TITLE = Config.WIN_TITLE
WIN_FONT = "*Font"
WIN_FONT_SETTING = "맑은고딕 15"
PADY = 5

SMALL_FONT = ("맑은고딕",8)
NORMAL_FONT = ("맑은고딕",9)
BIG_FONT = ("맑은고딕",10)


"""
GUI Class
"""
class GUI:

    def __init__(self, root):
        self.root = root
        root.geometry(WIN_SIZE)                 # 창 크기설정
        root.title(WIN_TITLE)           # 창 제목설정
        root.option_add(WIN_FONT, WIN_FONT_SETTING)    # 폰트설정
        root.resizable(False, False)             # x, y 창 크기 변경 불가
        root.protocol("WM_DELETE_WINDOW", self.onClosing)
        root.iconbitmap('./resource/warrenbuffett.ico')
        self.stockCode = ""
        self.stockAnalyzer = None
        self.workerThread = None

        self.eventQueue = queue.Queue()
        self.tickerAnalysisEvent = False
        self.analysisFinishEvent = False
        self.analysisResult = False

        # output 폴더가 없다면 새로 생성
        self.out_dir = Config.OUT_DIR
        AppUtil.makeDirIfNotExist(self.out_dir)
        self.chart_dir = os.path.join(self.out_dir, 'chart')
        AppUtil.makeDirIfNotExist(self.chart_dir)

        self.expiryChecker = ExpiryChecker()
        self.hardExpiryChecker = HardExpiryChecker()

        self.analysisResultChecker = self.root.after(200, self.checkAnalysisResult)

    def onClosing(self):
        LOG('onClosing()')
        try:
            self.root.after_cancel(self.analysisResultChecker)
            self.root.destroy()
        except Exception as e:
            LOG(str(e))

    def start(self):

        # Start Button 콜백 함수
        def startButtonCb():
            if Config.__APP_GRADE__ == Config.FREE:

                #if self.expiryChecker.isExpired() or self.hardExpiryChecker.isExpired():
                if self.expiryChecker.isExpired():
                    msg_box = messagebox.showerror('Error', Config.EXPIRED_FAKE_MESSAGE)
                    if msg_box == 'ok':
                        return

            try:
                LOG('Start Button Clicked ~')
                self.statusText.delete(1.0,END)
                self.statusText.insert(END, '분석을 시작합니다.')

                # 분석 쓰레드 실행
                stockLister = UserSettings.StockLister()
                self.stockAnalyzer = UsaDivStockAnalyzer(self,
                                                stockLister.getStockCodeList())
                self.workerThread = WorkerThread(self.stockAnalyzer)
                self.workerThread.start()
            except Exception as e:
                traceback.format_exc()
                print(e)

        """
        제어 프레임
        """
        frame1 = Frame(root)
        frame1.pack()

        self.titleLabel = Label(frame1, 
                                  text = Config.TITLE_LABEL, 
                                  font = BIG_FONT, fg ="blue",
                                  borderwidth=1, relief="solid",
                                  width=40,
                                  height=2)
        self.titleLabel.pack(pady=10)

        for SUBTITLE_LABEL in Config.SUBTITLE_LABEL_LIST:
            self.subtitleLabel1 = Label(frame1,
                                    text = SUBTITLE_LABEL, 
                                    font = NORMAL_FONT,
                                    height=2)
            self.subtitleLabel1.pack(pady=0)
    
        self.startButton = Button(frame1,
                                  font = BIG_FONT,
                                  height=3)
        self.startButton.config(text= Config.START_BUTTON_LABEL)
        self.startButton.config(width=30)
        self.startButton.config(command=startButtonCb)
        self.startButton.pack(pady=PADY*2)

        self.messageLabel = Label(frame1, 
                                  text = f"주식 리스트 파일 : {Config.STOCK_LIST_FILE_PATH}", 
                                  font = BIG_FONT,
                                  height=1)
        self.messageLabel.pack(pady=PADY)

        self.statusLabel = Label(frame1, text = f'진행 상태',
                                 font = BIG_FONT)
        self.statusLabel.pack(pady=PADY*2)

        self.progressbar=tkinter.ttk.Progressbar(frame1, maximum=250, mode="indeterminate", length=350)
        self.progressbar.pack(pady=PADY)

        """
        진행 상황 프레임
        """
        frame2 = Frame(root)
        frame2.pack()

        # add a vertical scrollbar
        scrollbar = Scrollbar(frame2, orient='vertical')
        scrollbar.pack(side=RIGHT, fill='both')

        self.statusText = Text(frame2, height=10, width=70,
                               yscrollcommand=scrollbar.set, 
                               font = BIG_FONT)
        #self.statusText.insert(END, '')
        self.statusText.pack(pady=PADY*2)

        # Attach the scrollbar with the text widget
        scrollbar.config(command=self.statusText.yview)


        """
        기타 정보 프레임
        """
        frame3 = Frame(root)
        frame3.pack()
        openBlogButton = Button(frame3, 
                                text = "데이터로 투자하라\n\n전자책 바로가기",
                                width = 20,
                                height= 5,
                                font = BIG_FONT,
                                command = WebSiteOpener.openKmongEbook)
        openBlogButton.pack(side=LEFT, pady=20)

        openBlogButton = Button(frame3, 
                                text = "코드장인\n\n블로그 바로가기",
                                width = 20,
                                height= 5,
                                font = BIG_FONT,
                                command = WebSiteOpener.openMyBlog)
        openBlogButton.pack(side=RIGHT, padx=20, pady=20)

        """
        메뉴
        """
        self.menu = Menu(self.root)

        file_menu = Menu(self.menu, tearoff=0)
        file_menu.add_command(label="열기",
                              command=None
                              )
        file_menu.entryconfig(1, state=DISABLED)
        self.menu.add_cascade(label='파일', menu=file_menu)

        help_menu = Menu(self.menu, tearoff=0)
        help_menu.add_command(label="안티똥손",
                              command=HelpMenu.showAbout
                              )
        self.menu.add_cascade(label='도움말', menu=help_menu)
        self.root.config(menu=self.menu)

    def tickerAnalysisCb(self, **kargs):
        stockAnalyzerEvent = StockAnalyzerEvent(STOCK_ANALYSIS_OK_EVENT, kargs)
        self.eventQueue.put_nowait(stockAnalyzerEvent)

    def analysisCompleteCb(self, success):
        LOG('analysisCompleteCb ~')
        stockAnalyzerEvent = StockAnalyzerEvent(ANALYZER_FINISH_EVENT, {})
        self.eventQueue.put_nowait(stockAnalyzerEvent)

    def checkAnalysisResult(self):
        try:
            stockAnalyzerEvent = self.eventQueue.get_nowait()
            self.__handleEvent__(stockAnalyzerEvent)
        except Exception as e:
            #LOG(str(e))
            pass

        self.analysisResultChecker = self.root.after(200, self.checkAnalysisResult)

    def __handleEvent__(self, stockAnalyzerEvent):
        try:
            event = stockAnalyzerEvent.getEvent()
            LOG(f'event from analyzer = {event}')
            if event == STOCK_ANALYSIS_OK_EVENT:
                data = stockAnalyzerEvent.getData()
                ticker = data['ticker']
                cur_div_yield = data['cur_div_yield']
                stock_div_data = data['stock_div_data']
                chartFilePath = os.path.join(self.chart_dir, f'{ticker}.png')
                UsaDivStockLib.saveDivAnalysisChart(ticker,
                                                stock_div_data,
                                                cur_div_yield,
                                                chartFilePath)
                LOG(f'analysis ok')
            elif event == ANALYZER_FINISH_EVENT:
                LOG('analysis complete !')
                analysisResult = self.stockAnalyzer.getAnalysisResult()
                LOG(analysisResult)
                csvFileName = os.path.basename(Config.STOCK_LIST_FILE_PATH)
                csvFileName = csvFileName.replace('.csv', '_result.csv')
                resultCsvFilePath = os.path.join(self.out_dir, csvFileName)
                AnalysisResultSaver.saveAnalsisResultToCsv(analysisResult, resultCsvFilePath)
            else:
                LOG('invalid event !')
        except Exception as e:
            LOG(str(e))

    def __updateStatusText__(self, message):
        self.statusText.insert(END, message + '\n')
        self.statusText.see(END)        

if __name__ == "__main__":
    root = Tk()
    GUI(root).start()
    root.mainloop()    