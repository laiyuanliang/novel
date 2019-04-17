from .spider_tools import get_one_page, insert_Fiction, insert_Fiction_Lst, insert_Fiction_Content
from flask import render_template
from bs4 import BeautifulSoup

def save_fiction_lst(fic_lst):
    for lst in fic_lst:
        fic_id =lst[0]
        chapter_id = lst[1]
        chapter_name = lst[2]
        chapter_source_url = lst[3]
        insert_Fiction_Lst(fic_id=fic_id, chapter_id=chapter_id, 
            chapter_name=chapter_name, chapter_source_url=chapter_source_url)

def search(fic_name):
    url = 'https://sou.xanbhx.com/search?siteid=qula&q={}'.format(fic_name)
    page = get_one_page(url)
    soup = BeautifulSoup(page, 'html5lib')
    if len(soup.find_all('li')) < 2:
        return render_template('fiction_error.html', message='抱歉!您搜索的小说不存在。')

    search_outcome = soup.find_all('li')[1]
    fic_source_url = search_outcome.find('a').get('href')
    fic_id = fic_source_url.split('/')[-2]
    
    fic_page = get_one_page(fic_source_url)
    fic_soup = BeautifulSoup(fic_page, 'html5lib')

    # information get from fiction list page
    fic_name = fic_soup.find('div', id='maininfo').find('h1').text
    author = fic_soup.find('div', id='maininfo').find('p').text.split('：')[-1]
    fic_comment = fic_soup.find('div',id='intro').text.strip()
    new_content = fic_soup.find('div', id='maininfo').find_all('a')[3].text
    new_url = fic_soup.find('div', id='maininfo').find_all('a')[3].get('href').split('.')[0]
    update_time = fic_soup.find('div', id='maininfo').find_all('p')[2].text.split('：')[1]
    fic_img = 'https://www.qu.la' + fic_soup.find('img').get('src')

    fic_lst = [] 
    raw_fic_lst = fic_soup.find_all('dd')[12:]
    for item in raw_fic_lst:
        chapter_source_url = 'https://www.qu.la' + item.find('a').get('href')
        chapter_id = chapter_source_url.split('/')[-1].split('.')[0]
        chapter_name = item.find('a').text
        fic_lst.append([fic_id, chapter_id, chapter_name, chapter_source_url]) 

    save_fiction_lst(fic_lst)

    insert_Fiction(author=author, 
                    fic_name=fic_name,
                    fic_id =fic_id,
                    fic_img=fic_img,
                    fic_comment=fic_comment,
                    fic_source_url=fic_source_url,
                    new_content=new_content,
                    new_url=new_url,
                    update_time=update_time)

def get_fiction_lst(fic_source_url):
    fic_lst = []
    fic_id = fic_source_url.split('/')[-2]
    fic_page = get_one_page(fic_source_url)
    fic_soup = BeautifulSoup(fic_page, 'html5lib')
    raw_fic_lst = fic_soup.find_all('dd')[12:]
    for item in raw_fic_lst:
        chapter_source_url = 'https://www.qu.la' + item.find('a').get('href')
        chapter_id = chapter_source_url.split('/')[-1].split('.')[0]
        chapter_name = item.find('a').text
        fic_lst.append([fic_id, chapter_id, chapter_name, chapter_source_url]) 

    return fic_lst

#fic_source_url = 'https://www.qu.la/book/72146/'
def download_fiction_lst(fic_source_url):
    fic_lst = get_fiction_lst(fic_source_url)
    save_fiction_lst(fic_lst)

def download_fiction_content(chapter_source_url):
    fic_id = chapter_source_url.split('/')[-2]
    chapter_id = chapter_source_url.split('/')[-1].split('.')[0]

    content_page = get_one_page(chapter_source_url)

    content_soup = BeautifulSoup(content_page, 'html5lib')
    chapter_content = content_soup.find('div', id='content').text
    insert_Fiction_Content(fic_id=fic_id, chapter_id=chapter_id, chapter_content=chapter_content)

