from flask import url_for, redirect, render_template, request
from . import fiction
from app.models import Fiction, Fiction_Lst, Fiction_Content
from app.xiaoshuo.spider import (download_fiction_lst, download_fiction_content, 
    search, get_fiction_lst, save_fiction_lst)

def returnFiction(fic_id, chapter, fiction_content):
    first_chapter_id = Fiction_Lst.query.filter_by(fic_id=fic_id).order_by(Fiction_Lst.id).first().id 
    last_chapter_id = Fiction_Lst.query.filter_by(fic_id=fic_id).order_by(Fiction_Lst.id.desc()).first().id
    chapter_id = chapter.id
    if (chapter_id != first_chapter_id) and (chapter_id != last_chapter_id):
        chapter_pre = Fiction_Lst.query.filter_by(id=chapter_id-1).first().chapter_id  
        chapter_next = Fiction_Lst.query.filter_by(id=chapter_id+1).first().chapter_id
    elif chapter_id == first_chapter_id:
        chapter_pre = None 
        chapter_next = Fiction_Lst.query.filter_by(id=chapter_id+1).first().chapter_id
    elif chapter_id == last_chapter_id:
        chapter_pre = Fiction_Lst.query.filter_by(id=chapter_id-1).first().chapter_id  
        chapter_next = None 
    chapter_content = fiction_content.chapter_content
    chapter_name = chapter.chapter_name
    return fic_id, chapter_pre, chapter_next, chapter_name, chapter_content

@fiction.route('/')
def book_index():
    fictions = Fiction.query.all()
    return render_template('fiction_index.html', fictions=fictions)

@fiction.route('/list/<fic_id>')
def book_lst(fic_id):
    fictions = Fiction.query.all()
    fiction = Fiction.query.filter_by(fic_id=fic_id).first()
    if fiction is None:
        return render_template('fiction_error.html', message='抱歉！您搜索的小说ID不存在。')
    fiction_lst = Fiction_Lst.query.filter_by(fic_id=fic_id).all()
    if fiction_lst is None:
        download_fiction_lst(fiction.fic_source_url)
        fiction_lst = Fiction_Lst.query.filter_by(fic_id=fic_id).all()
        if fiction_lst is None:
            return render_template('fiction_error.html', message='抱歉！小说章节为空。')
    return render_template('fiction_lst.html', fictions=fictions,
        fiction=fiction, fiction_lst=fiction_lst)

@fiction.route('/fiction/')
def fiction_content():
    fic_id = request.args.get('fic_id')
    chapter_id = request.args.get('chapter_id')

    # 首先判断fiction表是否存在此小说
    fiction = Fiction.query.filter_by(fic_id=fic_id).first()
    if fiction is None:
        return render_template('fiction_error.html', message="抱歉！您搜索的小说ID不存在。")

    # 如果fiction表存在，检查fiction_lst表有没有该章节，如果没有，下载整个章节列表
    else:
        chapter = Fiction_Lst.query.filter_by(fic_id=fic_id, chapter_id=chapter_id).first()
        if chapter is None:
            fic_name = fiction.fic_name
            download_fiction_lst(fiction.fic_source_url)
            print("下载《{}》列表完成！".format(fic_name))
            chapter = Fiction_Lst.query.filter_by(fic_id=fic_id, chapter_id=chapter_id).first()
            
            if chapter is None:
                return render_template('fiction_error.html', message="抱歉！您搜索的章节不存在。")
            else:
                chapter_source_url = chapter.chapter_source_url
                download_fiction_content(chapter_source_url)
                fiction_content = Fiction_Content.query.filter_by(fic_id=fic_id, chapter_id=chapter_id).first()
                if fiction_content is not None:
                    fic_id, chapter_pre, chapter_next, chapter_name, chapter_content = returnFiction(fic_id, chapter, fiction_content)
                    return render_template('fiction.html', 
                        fic_id=fic_id,
                        chapter_pre=chapter_pre,
                        chapter_next=chapter_next,
                        chapter_name=chapter_name,
                        chapter_content=chapter_content)
                else:
                    return render_template('fiction_error.html', message="抱歉！您搜索的章节不存在。")
        # fiction_lst已经有该章节，判断fiction_content有没有内容，没有就下载                
        else:
            fiction_content = Fiction_Content.query.filter_by(fic_id=fic_id, chapter_id=chapter_id).first()
            if fiction_content is None: 
                chapter_source_url = chapter.chapter_source_url
                download_fiction_content(chapter_source_url)
                fiction_content = Fiction_Content.query.filter_by(fic_id=fic_id, chapter_id=chapter_id).first()
                if fiction_content is None:
                    return render_template('fiction_error.html', message="抱歉！您搜索的章节不存在。")
                else:
                    fic_id, chapter_pre, chapter_next, chapter_name, chapter_content = returnFiction(fic_id, chapter, fiction_content)
                    return render_template('fiction.html', 
                        fic_id=fic_id,
                        chapter_pre=chapter_pre,
                        chapter_next=chapter_next,
                        chapter_name=chapter_name,
                        chapter_content=chapter_content)
            else:
                fic_id, chapter_pre, chapter_next, chapter_name, chapter_content = returnFiction(fic_id, chapter, fiction_content)
                return render_template('fiction.html', 
                    fic_id=fic_id,
                    chapter_pre=chapter_pre,
                    chapter_next=chapter_next,
                    chapter_name=chapter_name,
                    chapter_content=chapter_content)


@fiction.route('/search/')
def fiction_search():
    fic_name = request.args.get('fic_name')
    fiction = Fiction.query.filter_by(fic_name=fic_name).first()
    if fiction is None:
        search(fic_name)
        fiction = Fiction.query.filter_by(fic_name=fic_name).first()
        if fiction is None:
            return render_template('fiction_error.html', message="抱歉!您搜索的小说不存在。")
    fic_id = fiction.fic_id
    fiction_lst = Fiction_Lst.query.filter_by(fic_id=fic_id).all()
    fictions = Fiction.query.all()
    return render_template('fiction_lst.html', fiction=fiction, fictions=fictions, fiction_lst=fiction_lst)


@fiction.route('/update/')
def update():
    fic_name = request.args.get('fic_name')
    fic_id = Fiction.query.filter_by(fic_name=fic_name).first().fic_id
    fic_source_url = request.args.get('f_url')
    lst_on_db = Fiction_Lst.query.filter_by(fic_id=fic_id).all()
    len_on_db = len(lst_on_db)
    lst_of_source = get_fiction_lst(fic_source_url)
    len_of_source = len(lst_of_source)
    if len_of_source > len_on_db:
        save_fiction_lst(lst_of_source)
        lst_on_db = Fiction_Lst.query.filter_by(fic_id=fic_id).all()
        print("更新小说《{}》目录完成".format(fic_name))
    else:
        print("小说《{}》目录已是最新".format(fic_name))

    fiction = Fiction.query.filter_by(fic_id=fic_id).first()
    fictions = Fiction.query.all()
    return render_template('fiction_lst.html', fiction=fiction, fictions=fictions, fiction_lst=lst_on_db)

