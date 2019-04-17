from app.models import Fiction, Fiction_Lst, Fiction_Content
import requests
from random import choice, randint
from time import sleep
from app import db

headers = {}
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
headers['Connection'] = 'keep-alive'
headers['Upgrade-Insecure-Requests'] = '1'

agents = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
]

def get_one_page(url, sflag=1):
    while True:
        try:
            headers['User-Agent'] = choice(agents)
            if sflag ==1:
                sleep(randint(1,3))
            page = requests.get(url, timeout=5, headers=headers)
        except Exception as e:
            print("下载页面失败,errorInfo:", e)
            continue
        else:
            if page.status_code == 200:
                page.encoding = page.apparent_encoding
                return page.text
            else:
                continue

def insert_Fiction(author, fic_name, fic_id, fic_img, fic_comment, fic_source_url, new_content, new_url, update_time):
    fiction = Fiction(author=author,
                      fic_name=fic_name,
                      fic_id=fic_id,
                      fic_img=fic_img,
                      fic_comment=fic_comment,
                      fic_source_url=fic_source_url,
                      new_content=new_content,
                      new_url=new_url,
                      update_time=update_time
        )
    db.session.add(fiction)
    db.session.commit()

def insert_Fiction_Lst(fic_id, chapter_id, chapter_name, chapter_source_url):
    fiction_lst = Fiction_Lst(fic_id=fic_id,
                              chapter_id=chapter_id,
                              chapter_name=chapter_name,
                              chapter_source_url=chapter_source_url
        )
    db.session.add(fiction_lst)
    db.session.commit()

def insert_Fiction_Content(fic_id, chapter_id, chapter_content):
    fiction_content = Fiction_Content(fic_id=fic_id,
                              chapter_id=chapter_id,
                              chapter_content=chapter_content
        )
    db.session.add(fiction_content)
    db.session.commit()


