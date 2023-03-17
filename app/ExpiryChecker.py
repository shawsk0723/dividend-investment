"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""
import os
from hashlib import blake2b
import tempfile
from datetime import datetime
from datetime import timedelta
import Config

def LOG(msg):
    #print(msg)
    pass

class HardExpiryChecker:
    def isExpired(self):
        expire_date = Config.APP_EXPIRE_DATE
        return datetime.today() > expire_date

    def getExiryDate(self):
        exiryDate = (Config.APP_EXPIRE_DATE - timedelta(days=1)).strftime("%Y-%m-%d")
        return exiryDate

class ExpiryChecker:
    def __init__(self, expiration_day = Config.EXPIRATION_DAY):
        m = blake2b(digest_size=17)
        m.update(Config.WIN_TITLE.encode('utf-8'))
        expiryfilename = m.hexdigest() + '.bin'
        self.expiry_file_path = os.path.join(tempfile.gettempdir(), expiryfilename) 
        self.expiration_day = expiration_day
        self.remained_day = 0

        self.current_date = datetime.now()
        LOG(f'expiry_file_path = {self.expiry_file_path}')
        if os.path.isfile(self.expiry_file_path):
            with open(self.expiry_file_path, 'r') as f:
                install_date =f.read()
                install_date = datetime.strptime(install_date, "%Y%m%d")
                LOG(f'install_date = {install_date}')
                LOG(f'current_date = {self.current_date}')
                self.elapsed_day = self.current_date - install_date
                self.remained_day = self.expiration_day - self.elapsed_day.days
        else:
            with open(self.expiry_file_path, 'w') as f:
                f.write(f'{self.current_date.strftime("%Y%m%d")}')
                self.elapsed_day = timedelta(0)
                self.remained_day = self.expiration_day

    def isExpired(self):
        return self.elapsed_day > timedelta(self.expiration_day)

    def getRemainedDay(self):
        return self.remained_day

"""
TEST
"""
if __name__ == '__main__':
    expiryChecker = ExpiryChecker()
    expired = expiryChecker.isExpired()
    print(f'expired = {expired}')
    print(f'remained day = {expiryChecker.getRemainedDay()}')