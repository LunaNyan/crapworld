from system.appinfo import VERSION
import logging
import yaml

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
    with open("data/site_settings.yaml", "r", encoding="utf-8") as j:
        site_settings = yaml.load(j, yaml.FullLoader)
    return site_settings


def make_menu_tab(settings, link: str, tab_name: str, selected: bool):
    menu_tab = get_html_file(cnv_path(f'theme/{settings["theme"]}/html/menu_tab.html'))
    menu_tab = menu_tab.replace("{link}", link)
    menu_tab = menu_tab.replace("{tab_name}", tab_name)
    if selected:
        menu_tab = menu_tab.replace("{class_type}", "tab_selected")
    else:
        menu_tab = menu_tab.replace("{class_type}", "tab")
    return menu_tab


def basepage(menu_mode):
    settings = get_settings()
    index_html = get_html_file(cnv_path(f'theme/{settings["theme"]}/html/index.html'))
    site_settings = get_settings()
    # 파라미터 수정 개시
    index_html = index_html.replace('{site_title}', site_settings['site_title'])
    index_html = index_html.replace('{hompy_title}', site_settings['hompy_title'])
    index_html = index_html.replace('{site_url}', site_settings['site_url'])
    index_html = index_html.replace('{app_version}', VERSION)
    # 드롭다운
    drop_html = get_html_file(cnv_path(
        f'theme/{settings["theme"]}/html/dropdown_name.html')).replace("{name}", site_settings['dropdown_name'])
    drop_item = get_html_file(cnv_path(f'theme/{settings["theme"]}/html/dropdown_item.html'))
    for i in site_settings['dropdown_items']:
        tmp = drop_item.replace('{url}', i['url'])
        tmp = tmp.replace('{name}', i['name'])
        drop_html += tmp
    index_html = index_html.replace('{dropdown_menus}', drop_html)
    # 메뉴
    menu_html = get_html_file(cnv_path(f'theme/{settings["theme"]}/html/menu.html'))
    # 메뉴 탭
    menu_items = make_menu_tab(settings, "/", settings["home_tab_name"], menu_mode == "home")
    menu_items += make_menu_tab(settings, "/diary", settings["diary_tab_name"], menu_mode == "diary")
    # 커스텀 가능 탭
    for i in site_settings['link_tabs']:
        menu_items += make_menu_tab(settings, i["url"], i["name"], False)
    menu_html = menu_html.replace("{menu_items}", menu_items)
    # 메뉴 삽입
    index_html = index_html.replace('{menu}', menu_html)
    # footer
    footer_links = ""
    for i in site_settings['footer_links']:
        footer_links += f' | <a href="{i["url"]}">{i["name"]}</a>'
    index_html = index_html.replace('{footer_links}', footer_links)
    return index_html
