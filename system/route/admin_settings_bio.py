from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer, ip_filter
from system.route.admin import render_list
from flask import request, abort, redirect
from PIL import Image
import os
import yaml


@app.route('/admin/content/bio/post_profile_pic', methods=['POST'])
def admin_content_bio_upload_pic():
    file = request.files['file']
    file.save("cache/profile_pic")

    im = Image.open("cache/profile_pic")
    im.save('data/img/icon.png')

    os.remove("cache/profile_pic")

    return redirect(location=f"/admin/content/bio")


@app.route('/admin/content/bio/post', methods=['POST'])
def admin_content_bio_post():
    # 오늘의 기분
    with open("data/todays_feeling.yaml", "w", encoding="utf-8") as j:
        yaml.dump({"feeling": request.form.get('todays_feeling')}, j, allow_unicode=True)
    # 바이오
    with open("data/bio.html", "w", encoding="utf-8") as b:
        b.write(request.form.get('bio'))

    return redirect(location=f"/admin/content/bio")


@app.route('/admin/content/bio')
def admin_settings_bio():
    if not ip_filter.is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)
    admin_html = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    admin_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/admin_settings_bio.html')

    with open("data/todays_feeling.yaml", "r", encoding="utf-8") as j:
        feeling = yaml.load(j, yaml.FullLoader)

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("bio"),
        "{todays_feeling}": feeling['feeling'],
        "{bio}": renderer.get_html_file('data/bio.html')
    }
    admin_html = renderer.fill_args(admin_html, arg)

    return renderer.render_mainpage(admin_html, "admin", "diary")
