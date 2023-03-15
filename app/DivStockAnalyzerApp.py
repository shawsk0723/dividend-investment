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
from ExpiryChecker import ExpiryChecker
from AppLogger import LOG
from BlogOpener import openBlog
from KorDivStockAnalyzer import KorDivStockAnalyzer
from UsaDivStockAnalyzer import UsaDivStockAnalyzer
from WorkerThread import WorkerThread
from StockAnalyzerEvent import *
from ResultDisplayWindow import ResultDisplayWindow
import AnalysisResultSaver
import UserSettings
import HelpMenu


"""
App config
"""

WIN_SIZE = Config.WIN_SIZE
WIN_TITLE = Config.WIN_TITLE
WIN_FONT = "*Font"
WIN_FONT_SETTING = "맑은고딕 15"
PADY = 5

DEFAULT_FONT = ("맑은고딕",9)
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

        self.analysisResultChecker = self.root.after(200, self.checkAnalysisResult)

    def onClosing(self):
        LOG('onClosing()')
        try:
            self.root.after_cancel(self.analysisResultChecker)
            self.root.destroy()
        except Exception as e:
            LOG(str(e))

    def start(self):

        if Config.__APP_GRADE__ == Config.FREE:
            expiryChecker = ExpiryChecker()
            if expiryChecker.isExpired():
                msg_box = messagebox.showerror('Error', Config.EXPIRED_MESSAGE)
                if msg_box == 'ok':
                    self.root.destroy()
                    return
            else:
                remainedDay = expiryChecker.getRemainedDay()
                LOG(f'remained day = {remainedDay}')
                self.expiryLabel = Label(root,
                                         text = f'사용 기간이 {remainedDay}일 남았습니다.',
                                         font = DEFAULT_FONT, fg ="blue",
                                         height=1)
                self.expiryLabel.pack(pady=PADY)

        # Start Button 콜백 함수
        def startButtonCb():
            try:
                LOG('Start Button Clicked ~')
                #self.stockCode = self.codeEntry.get()
                #if self.stockCode == "":
                #    messagebox.showerror('Error', '코드를 입력하세요!')
                #    return
                # 결과 텍스트 위젯 리셋
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

        self.messageLabel = Label(frame1, 
                                  text = f"주식 리스트 파일 : {Config.STOCK_LIST_FILE_PATH}", 
                                  font = BIG_FONT,
                                  height=1)
        self.messageLabel.pack(pady=PADY)

        #self.codeEntry = Entry(frame1, width=50)           # root라는 창에 입력창 생성
        #self.codeEntry.insert(0, UserSettings.getStockCodeList()[0])
        #self.codeEntry.pack(pady=PADY)                               # 입력창 배치

        self.startButton = Button(frame1,
                                  font = BIG_FONT,
                                  height=5)
        self.startButton.config(text= Config.START_BUTTON_LABEL)               # 버튼 내용 
        self.startButton.config(width=20)                      # 버튼 크기
        self.startButton.config(command=startButtonCb)               # 버튼 기능 (btnpree() 함수 호출)
        self.startButton.pack(pady=PADY*2)                                 # 버튼 배치

        self.progressbar=tkinter.ttk.Progressbar(frame1, maximum=100, mode="indeterminate")
        self.progressbar.pack(pady=PADY)

        self.statusLabel = Label(frame1, text = f'진행 상태',
                                 font = BIG_FONT)
        self.statusLabel.pack(pady=PADY*2)

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
                                text = "코드장인의 블로그 바로가기",
                                font = BIG_FONT,
                                command=openBlog)
        openBlogButton.pack(side=BOTTOM, pady=20)

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

    def tickerAnalysisCb(self, ticker, success):
        LOG(f'tickerAnalysisCb, ticker = {ticker}, success = {success}')
        if success:
            stockAnalyzerEvent = StockAnalyzerEvent(STOCK_ANALYSIS_OK_EVENT, ticker)
        else:
            stockAnalyzerEvent = StockAnalyzerEvent(STOCK_ANALYSIS_FAIL_EVENT, ticker)

        self.eventQueue.put_nowait(stockAnalyzerEvent)

    def analysisCompleteCb(self, success):
        LOG('analysisCompleteCb ~')
        stockAnalyzerEvent = StockAnalyzerEvent(ANALYZER_FINISH_EVENT, "")
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
                ticker = stockAnalyzerEvent.getMessage()
                LOG(f'{ticker} analysis ok !')
                self.stockAnalyzer.saveAnalysisChartImage(ticker, self.chart_dir)
            elif event == ANALYZER_FINISH_EVENT:
                LOG('analysis complete !')
                analysisResult = self.stockAnalyzer.getAnalysisResult()
                LOG(analysisResult)
                csvFileName = os.path.basename(Config.STOCK_LIST_FILE_PATH)
                csvFileName = csvFileName.replace('.csv', '_result.csv')
                resultCsvFilePath = os.path.join(self.out_dir, csvFileName)
                AnalysisResultSaver.saveAnalsisResultToCsv(analysisResult, resultCsvFilePath)
                self.__updateStatusText__('*'*30)
                self.__updateStatusText__('주식 리스트 분석을 모두 완료하였습니다.')
                self.__updateStatusText__('*'*30)
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