from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer, ip_filter
from system.object.profile import get_list as get_profile_list
from flask import request, abort


def render_list(current=None):
    cms_lst = [
        ["프로필", "profile"],
        ["다이어리", "diary"],
        ["사진첩", "photo"],
        ["동영상", "video"]
    ]
    html_delimiter = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/diary_delimiter.html")
    html_delimiter_end = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/diary_delimiter_end.html")
    html_list_item = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/admin_content_list_item.html")
    html_list_item_cur = renderer.get_html_file(
            f"theme/{site_settings()['theme']}/html/admin_content_list_item_selected.html")
    ht = ""

    ht += html_delimiter_end
    ht += html_delimiter.replace("{group_title}", f"컨텐츠 관리")
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


@app.route('/admin/content')
def admin_content_main():
    if not ip_filter.if_local(request):
        return abort(404)
    admin_html = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    admin_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/admin_content_placeholder.html')

    arg = {
        "{entry_content}": admin_content,
        "{entry_list}": render_list()
    }
    admin_html = renderer.fill_args(admin_html, arg)

    return renderer.admin_render_mainpage(admin_html, "admin_content", "diary")


# ===== 프로필(우측) =====
@app.route('/admin/content/profile')
def admin_content_profile():
    if not ip_filter.if_local(request):
        return abort(404)
    admin_html = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    admin_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/admin_content_profile.html')

    # 프로필 리스트 제작
    ht = ""
    for i in get_profile_list():
        ht += f"<li><a href=\"/admin/content/profile/edit/{i.filename}\">{i.title}</a></li>"

    arg = {
        "{entry_content}": admin_content,
        "{contents}": ht,
        "{entry_list}": render_list(current="profile")
    }
    admin_html = renderer.fill_args(admin_html, arg)

    return renderer.admin_render_mainpage(admin_html, "admin_content", "diary")
