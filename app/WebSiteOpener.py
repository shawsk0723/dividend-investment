"""
YoutubeMP3ExtractorApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""


import webbrowser

def openMyBlog():
    try:
        url = "https://blog.naver.com/shawgibal"
        webbrowser.open(url,new=1)
    except Exception as e:
        print(f'exception happens while opening url = {url}')
        print(e)


def openKmongEbook():
    try:
        url = "https://kmong.com/self-marketing/430900/oPS99d32DU"
        webbrowser.open(url,new=1)
    except Exception as e:
        print(f'exception happens while opening url = {url}')
        print(e)
