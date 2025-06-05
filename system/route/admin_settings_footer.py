from system.engine.server import app
from system.engine.settings import site_settings, save_settings
from system.tool.renderer import load_html_shard, render_mainpage, fill_args
from system.tool.auth import is_admin
from system.route.admin import render_list
from flask import request, abort, redirect
from os import listdir
from os.path import isdir


@app.route('/admin/content/footer/post', methods=['POST'])
def admin_settings_footer_post():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    settings_to_save = site_settings()
    settings_to_save["footer_links"] = []

    link_t = request.form.get('footer_content')
    print(link_t)
    for i in link_t.split("\n"):
        if len(i.split("|")) != 2:
            continue
        elif i == "":
            continue
        ii = i.split("|")
        settings_to_save["footer_links"].append({'name': ii[0], 'url': ii[1]})

    save_settings(settings_to_save)
    return redirect(location=f"/admin/content/footer")


@app.route('/admin/content/footer')
def admin_settings_footer():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    admin_html = load_html_shard('diary/main')
    admin_content = load_html_shard('admin/settings_footer')

    # themes list
    themes = ""
    for i in listdir("theme"):
        if isdir(f"theme/{i}"):
            if i == site_settings()["theme"]:
                themes += f"<option value=\"{i}\" selected>{i}</option>\n"
            else:
                themes += f"<option value=\"{i}\">{i}</option>\n"

    links_t = ""
    for i in site_settings()["footer_links"]:
        links_t += f"{i['name']}|{i['url']}\n"

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("footer"),
        # 기본 설정
        "{footer_content}": links_t
    }
    admin_html = fill_args(admin_html, arg)

    return render_mainpage(admin_html, "admin", "diary")
