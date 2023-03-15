import os
from datetime import datetime
import Version


"""
App Grade
"""
FREE = '무료'
PAID = '유료'

__APP_GRADE__ = FREE


"""
Country
"""
USA = '미국'
KOR = '한국'
COUNTRY = USA

"""
Build Type
"""
RELEASE = 'Release'
DEBUG = 'Debug'

__BUILD_TYPE__ = RELEASE

def isRelease():
    return __BUILD_TYPE__ == RELEASE


"""
앱 유효 기간
"""

EXPIRATION_DAY = 30

APP_EXPIRE_DATE = datetime(2023,5,1)
#APP_EXPIRE_DATE = datetime(2023,2,1)

EXPIRED_MESSAGE = '데이터 유효 기간이 만료되었습니다!'

"""
App Config
"""
WIN_SIZE = "800x500"
WIN_FONT_SETTING = "맑은고딕 9"

WIN_TITLE = f'안티똥손 {COUNTRY}판 {Version.getVersion()} {__BUILD_TYPE__} ({__APP_GRADE__})'

INPUT_GUIDE_LABEL = '주식 코드를 입력하세요~'
START_BUTTON_LABEL = '분석해 주세요~'
DATA_DIR = os.path.join(os.getcwd(), 'data')
OUT_DIR = os.path.join(os.getcwd(), 'output')

"""
Stock Config
"""

STOCK_LIST_FILE_PATH = './data/stocklist.csv'

START_DATE = '20150501'
DEFAULT_STOCK_CODE = '010130'