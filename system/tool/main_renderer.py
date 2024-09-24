from system.appinfo import VERSION
import logging
import json

from system.tool.dirpath_delimiter import cnv_path

log = logging.getLogger(__name__)


def get_html_file(filename, auto_br=False):
    ff = open(filename, 'r', encoding='utf-8')
    index_html = ff.read()
    if auto_br:
        index_html = index_html.replace("\\\\n", "&#5c;n")
        index_html = index_html.replace("\n", "<br>")
    ff.close()
    return index_html


def get_settings():
    # 설정 읽어들이기
    with open("data/site_settings.json", "r", encoding="utf-8") as j:
        site_settings = json.loads(j.read())
    return site_settings


def basepage(menu_mode=1):
    settings = get_settings()
    index_html = get_html_file(cnv_path(f'theme/{settings["theme"]}/html/index.html'))
    site_settings = get_settings()
    # 파라미터 수정 개시
    index_html = index_html.replace('{site_title}', site_settings['site_title'])
    index_html = index_html.replace('{hompy_title}', site_settings['hompy_title'])
    index_html = index_html.replace('{site_url}', site_settings['site_url'])
    index_html = index_html.replace('{app_version}', VERSION)
    # 메뉴
    index_html = index_html.replace('{menu}', get_html_file(
            cnv_path(f'theme/{settings["theme"]}/html/menu.html')))
    index_html = index_html.replace(f'<img src="/static/m0{menu_mode}_0.png"><br>',
                                    f'<img src="/static/m0{menu_mode}_1.png"><br>',)
    return index_html
