from system.appinfo import VERSION
from system.engine.settings import site_settings, load_settings
from system.tool.etc import cnv_path
import conf


def get_html_file(filename, auto_br=False):
    ff = open(cnv_path(filename), 'r', encoding='utf-8')
    index_html = ff.read()
    if auto_br:
        index_html = index_html.replace("\\\\n", "&#5c;n")
        index_html = index_html.replace("\n", "<br>")
    ff.close()
    return index_html


def fill_args(orig: str, arg: dict):
    for key, val in arg.items():
        orig = orig.replace(key, val)
    return orig


def render_tab(link: str, tab_name: str, selected: bool):
    """
    탭 아이템을 렌더링하여 HTML로 리턴한다.

    link (str) : 탭을 눌렀을 때 향하는 링크
    tab_name (str) : 탭의 표시 이름
    selected (bool) : 탭을 선택되었다고 표시할 지의 여부
    """
    fill_arg = {
        "{link}": link,
        "{tab_name}": tab_name,
        "{class_type}": "tab_selected" if selected else "tab"
    }
    menu_item = get_html_file(f'theme/{site_settings["theme"]}/html/menu_tab.html')
    menu_item = fill_args(menu_item, fill_arg)
    return menu_item


def render_mainpage(content: str, tab_selected: str, extra_css: str, enable_dropdown=True):
    """
    메인 페이지를 렌더링하여 최종적으로 사용자가 보게 되는 HTML을 리턴한다.

    content (str) : 페이지에 삽입될 메인 컨텐츠 HTML
    tab_selected (str) : 선택되었다고 표시할 탭의 변수명
    """
    if conf.dynamically_reload_site_settings:
        load_settings()
    index_html = get_html_file(f'theme/{site_settings["theme"]}/html/index.html')

    # ===== 탭 만들기 =====
    tab_html = get_html_file(f'theme/{site_settings["theme"]}/html/menu.html')
    # 구현된 기능에 대한 탭
    tab_items = render_tab("/", site_settings["home_tab_name"], tab_selected == "home")
    if site_settings["use_diary"]:
        tab_items += render_tab("/diary", site_settings["diary_tab_name"], tab_selected == "diary")
    if site_settings["use_gallery"]:
        tab_items += render_tab("/gallery", site_settings["gallery_tab_name"], tab_selected == "gallery")
    # 이 밑으로는 사용자가 추가한 탭을 넣는다.
    for i in site_settings['link_tabs']:
        tab_items += render_tab(i["url"], i["name"], False)
    if conf.debug:
        tab_items += render_tab("/debug", "디버그", tab_selected == "debug")
    tab_html = tab_html.replace("{menu_items}", tab_items)

    # ===== 드롭다운 메뉴 만들기 =====
    if enable_dropdown and site_settings["use_dropdown"]:
        # 드롭다운 메뉴 제작에 필요한 HTML을 로드한다.
        drop_html = get_html_file(f'theme/{site_settings["theme"]}/html/dropdown.html')
        drop_items = get_html_file(f'theme/{site_settings["theme"]}/html/dropdown_name.html')
        drop_items = drop_items.replace("{name}", site_settings["dropdown_name"])
        drop_item_ind = get_html_file(f'theme/{site_settings["theme"]}/html/dropdown_item.html')
        # 드롭다운 아이템 제작
        for i in site_settings["dropdown_items"]:
            drop_arg = {
                "{url}": i["url"],
                "{name}": i["name"]
            }
            tmp = fill_args(drop_item_ind, drop_arg)
            drop_items += tmp
        # 드롭다운 메뉴 HTML에 넣는다.
        drop_html = drop_html.replace("{dropdown_menus}", drop_items)
    else:
        drop_html = get_html_file(f'theme/{site_settings["theme"]}/html/dropdown_placeholder.html')

    # ===== 하단 링크 만들기 =====
    footer_links = ""
    for i in site_settings["footer_links"]:
        footer_links += f'{site_settings["footer_delimiter"]}<a href="{i["url"]}">{i["name"]}</a>'

    # 최종적으로 args를 채워넣는다.
    fill_arg = {
        "{extra_css}": extra_css,
        "{site_title}": site_settings['site_title'],
        "{hompy_title}": site_settings['hompy_title'],
        "{site_url}": site_settings['site_url'],
        "{menu}": tab_html,
        "{dropdown}": drop_html,
        "{app_version}": VERSION,
        "{footer_links}": footer_links,
        "{content}": content
    }
    index_html = fill_args(index_html, fill_arg)
    return index_html
