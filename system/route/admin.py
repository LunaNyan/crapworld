from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer, ip_filter
from flask import request, abort


def render_list(current=None):
    cms_lst = [
        ["미디어 관리", "media"],
        ["기본 설정", "settings"],
        ["바이오", "bio"],
        ["하단 바", "footer"],
        ["파도타기", "links"],
        ["커스텀 탭", "custom_tab"],
        ["고급", "advanced"]
    ]
    html_delimiter = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/diary_delimiter.html")
    html_delimiter_end = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/diary_delimiter_end.html")
    html_list_item = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/admin_content_list_item.html")
    html_list_item_cur = renderer.get_html_file(
            f"theme/{site_settings()['theme']}/html/admin_content_list_item_selected.html")
    ht = ""

    ht += html_delimiter_end
    ht += html_delimiter.replace("{group_title}", f"관리자 메뉴")
    for i in cms_lst:
        if i[1] == current:
            ht2 = html_list_item_cur.replace('{title}', i[0])
            ht2 = ht2.replace('{cms}', i[1])
        else:
            ht2 = html_list_item.replace('{title}', i[0])
            ht2 = ht2.replace('{cms}', i[1])
        ht += ht2
    ht += html_delimiter_end
    return ht


@app.route('/admin')
def admin_home():
    if not ip_filter.is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)
    admin_html = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    admin_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/admin_main_content.html')

    arg = {
        "{entry_content}": admin_content,
        "{entry_list}": render_list(),
        "{ip}": request.remote_addr
    }
    admin_html = renderer.fill_args(admin_html, arg)

    return renderer.render_mainpage(admin_html, "admin", "diary")
