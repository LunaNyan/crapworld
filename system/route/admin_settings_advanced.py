from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.renderer import load_html_shard, render_mainpage, fill_args
from system.tool.auth import is_admin
from system.route.admin import render_list
from flask import request, abort, redirect
from os import listdir, remove


@app.route('/admin/content/advanced/clear_cache')
def admin_clear_cache():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    for i in listdir("cache/image_thumbnail"):
        if i.endswith(".png"):
            remove(f"cache/image_thumbnail/{i}")

    with open("cache/image_thumbnail/entry.yaml", "w", encoding="utf-8") as f:
        f.write("orig_path: thumbnail_path\n")

    return redirect("/admin/content/advanced")


@app.route('/admin/content/advanced')
def admin_settings_advanced():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    admin_html = load_html_shard('diary/main')
    admin_content = load_html_shard('admin/settings_advanced')

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("advanced")
    }
    admin_html = fill_args(admin_html, arg)

    return render_mainpage(admin_html, "admin", "diary")
