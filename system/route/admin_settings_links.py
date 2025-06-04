from system.engine.server import app
from system.engine.settings import site_settings, save_settings
from system.tool import renderer, ip_filter
from system.route.admin import render_list
from flask import request, abort, redirect
from os import listdir
from os.path import isdir


@app.route('/admin/content/links/post', methods=['POST'])
def admin_settings_dropdown_post():
    if not ip_filter.is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    settings_to_save = site_settings()
    settings_to_save["dropdown_items"] = []

    link_t = request.form.get('dropdown_content')
    print(link_t)
    for i in link_t.split("\n"):
        if len(i.split("|")) != 2:
            continue
        elif i == "":
            continue
        ii = i.split("|")
        settings_to_save["dropdown_items"].append({'name': ii[0], 'url': ii[1]})

    save_settings(settings_to_save)
    return redirect(location=f"/admin/content/links")


@app.route('/admin/content/links')
def admin_settings_links():
    if not ip_filter.is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    admin_html = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    admin_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/admin_settings_links.html')

    # themes list
    themes = ""
    for i in listdir("theme"):
        if isdir(f"theme/{i}"):
            if i == site_settings()["theme"]:
                themes += f"<option value=\"{i}\" selected>{i}</option>\n"
            else:
                themes += f"<option value=\"{i}\">{i}</option>\n"

    links_t = ""
    for i in site_settings()["dropdown_items"]:
        links_t += f"{i['name']}|{i['url']}\n"

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("links"),
        # 기본 설정
        "{dropdown_content}": links_t
    }
    admin_html = renderer.fill_args(admin_html, arg)

    return renderer.render_mainpage(admin_html, "admin", "diary")
