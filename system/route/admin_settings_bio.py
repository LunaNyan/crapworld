from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.renderer import load_html_shard, render_mainpage, fill_args, get_html_file
from system.tool.auth import is_admin
from system.route.admin import render_list
from flask import request, abort, redirect
from PIL import Image
import os
import yaml


@app.route('/admin/content/bio/post_profile_pic', methods=['POST'])
def admin_content_bio_upload_pic():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    file = request.files['file']
    file.save("cache/profile_pic")

    im = Image.open("cache/profile_pic")
    im.save('data/img/icon.png')

    os.remove("cache/profile_pic")

    return redirect(location=f"/admin/content/bio")


@app.route('/admin/content/bio/post', methods=['POST'])
def admin_content_bio_post():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    # 오늘의 기분
    with open("data/todays_feeling.yaml", "w", encoding="utf-8") as j:
        yaml.dump({"feeling": request.form.get('todays_feeling')}, j, allow_unicode=True)
    # 바이오
    with open("data/bio.html", "w", encoding="utf-8") as b:
        b.write(request.form.get('bio'))

    return redirect(location=f"/admin/content/bio")


@app.route('/admin/content/bio')
def admin_settings_bio():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    admin_html = load_html_shard('diary/main')
    admin_content = load_html_shard('admin/settings_bio')

    with open("data/todays_feeling.yaml", "r", encoding="utf-8") as j:
        feeling = yaml.load(j, yaml.FullLoader)

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("bio"),
        "{todays_feeling}": feeling['feeling'],
        "{bio}": get_html_file('data/bio.html')
    }
    admin_html = fill_args(admin_html, arg)

    return render_mainpage(admin_html, "admin", "diary")
