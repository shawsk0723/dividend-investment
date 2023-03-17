import os
from datetime import datetime
import Version


"""
App Grade
"""
FREE = 'Free'
PAID = 'Premium'

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

APP_EXPIRE_DATE = datetime(2023,6,1)
#APP_EXPIRE_DATE = datetime(2023,2,1)

EXPIRED_MESSAGE = '사용 기간이 만료되었습니다!'
EXPIRED_FAKE_MESSAGE = '업데이트가 필요합니다!'

"""
App Config
"""
APP_NAME = '안티똥손'

WIN_SIZE = "800x550"
WIN_FONT_SETTING = "맑은고딕 9"

WIN_TITLE = f'{APP_NAME} {COUNTRY}판 {Version.getVersion()} {__BUILD_TYPE__} ({__APP_GRADE__})'

TITLE_LABEL = '똥손탈출 프로젝트'
SUBTITLE_LABEL_1 = '인간은 원래 똥손으로 태어났다.'
SUBTITLE_LABEL_2 = '나도 똥손, 친구도 똥손, 전문가도 똥손이다.'
SUBTITLE_LABEL_LIST = [SUBTITLE_LABEL_1, SUBTITLE_LABEL_2]

START_BUTTON_LABEL = '데이터로 투자하라!'
DATA_DIR = os.path.join(os.getcwd(), 'data')
OUT_DIR = os.path.join(os.getcwd(), 'output')

"""
Stock Config
"""

STOCK_LIST_FILE_PATH = './data/stocklist.csv'

START_DATE = '20150501'
DEFAULT_STOCK_CODE = '010130'