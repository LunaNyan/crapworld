from system.appinfo import VERSION
import logging
import json

log = logging.getLogger(__name__)


def get_html_file(filename):
    ff = open(filename, 'r', encoding='utf-8')
    index_html = ff.read()
    ff.close()
    return index_html


def get_settings():
    # 설정 읽어들이기
    with open("data/site_settings.json", "r", encoding="utf-8") as j:
        site_settings = json.loads(j.read())
    return site_settings


def basepage(menu_mode=1):
    index_html = get_html_file('assets/html/index.html')
    site_settings = get_settings()
    # 파라미터 수정 개시
    index_html = index_html.replace('{site_title}', site_settings['site_title'])
    index_html = index_html.replace('{hompy_title}', site_settings['hompy_title'])
    index_html = index_html.replace('{app_version}', VERSION)
    # 메뉴
    index_html = index_html.replace('{menu}', get_html_file('assets/html/menu.html'))
    index_html = index_html.replace(f'<img src="/static/m0{menu_mode}_0.png"><br>',
                                    f'<img src="/static/m0{menu_mode}_1.png"><br>',)
    return index_html
