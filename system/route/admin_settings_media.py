from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.renderer import load_html_shard, render_mainpage, fill_args
from system.tool.auth import is_admin
from system.tool.etc import paginate
from system.object.photo import upload_pic
from system.route.admin import render_list
from flask import request, abort, redirect
from os import listdir, remove
from uuid import uuid4


@app.route('/admin/content/media/<photo_name>/confirm_remove')
def media_confirm_remove(photo_name):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    remove("data/img/" + photo_name)

    return redirect("/admin/content/media")


@app.route('/admin/content/media/<photo_name>/remove')
def media_remove(photo_name):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    admin_html = load_html_shard('diary/main')
    admin_content = load_html_shard('admin/media_confirm_remove')

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("media"),
        "{filename}": "/img/" + photo_name,
        "{filename_actual}": photo_name
    }
    admin_html = fill_args(admin_html, arg)

    return render_mainpage(admin_html, "admin", "diary")

@app.route('/admin/content/media', methods=['POST'])
def admin_upload_media():
    upload_pic(request, str(uuid4()))
    return redirect("/admin/content/media")


@app.route('/admin/content/media', defaults={'page': 1})
@app.route('/admin/content/media/<page>')
def admin_settings_media(page):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    admin_html = load_html_shard('diary/main')
    admin_content = load_html_shard('admin/settings_media_manager')
    media_item = load_html_shard('admin/settings_media_item')
    media_options = load_html_shard('admin/settings_media_options')

    img_lst = paginate(listdir("data/img"), page)
    med_lst = ""

    for i in img_lst.content:
        med = media_item.replace("{img_path}", "/img/" + i)
        if i == "icon.png":
            med = med.replace("{desc}", "프로필 사진 파일")
        else:
            med = med.replace("{desc}", media_options)
            med = med.replace("{filename}", i)
        med_lst += med

    page_ht = ""
    for i in range(img_lst.total_pages):
        if i+1 == page:
            page_ht += f"<b>{i+1}</b> "
        else:
            page_ht += f"<a href='/admin/content/media/{i+1}'>{i+1}</a> "

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("media"),
        "{media_list}": med_lst,
        "{page}": page_ht
    }
    admin_html = fill_args(admin_html, arg)

    return render_mainpage(admin_html, "admin", "diary")
