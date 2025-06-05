from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.auth import is_admin
from system.tool.renderer import load_html_shard, render_mainpage, fill_args
from system.object.photo import render_list, get_list, get_entry, add_category, upload_pic, add_entry, remove_entry
from flask import abort, request, redirect
from uuid import uuid4


@app.route('/photo/add_category', methods=['POST'])
def photo_add_category_post():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_photo"]:
        return abort(404)

    url = request.form['name']
    title = request.form['display_name']
    is_unlisted = request.form.get('unlisted')

    add_category(url, title, True if is_unlisted is not None else False)

    return redirect(location=f"/photo/{url}")


@app.route('/photo/add_category', methods=['GET'])
def photo_add_category():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_photo"]:
        return abort(404)

    form = load_html_shard('photo/add_category')
    diary_main = load_html_shard('diary/main')

    category_list = get_list()

    arg = {"{entry_list}": render_list(category_list, "add_item"),
           "{entry_content}": form}
    diary_main = fill_args(diary_main, arg)

    return render_mainpage(diary_main, "photo", "diary")


@app.route('/photo/<category>/add_item', methods=['POST'])
def photo_add_item_post(category):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_photo"]:
        return abort(404)

    slug = request.form.get('name')
    if slug == "":
        slug = str(uuid4())
    description = request.form.get('description')

    upload_pic(request, slug)
    add_entry(category, slug, description)

    return redirect(location=f"/photo/{category}/{slug}")


@app.route('/photo/<category>/add_item', methods=['GET'])
def photo_add_item(category):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_photo"]:
        return abort(404)

    form = load_html_shard('photo/add_item')
    diary_main = load_html_shard('diary/main')

    category_list = get_list()

    arg = {"{entry_list}": render_list(category_list, category),
           "{entry_content}": form,
           "{category}": category}
    diary_main = fill_args(diary_main, arg)

    return render_mainpage(diary_main, "photo", "diary")


@app.route('/photo/<category>/<photo_name>/confirm_remove')
def photo_remove_confirm(category, photo_name):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_photo"]:
        return abort(404)

    remove_entry(category, photo_name)

    return redirect(location=f"/photo/{category}")


@app.route('/photo/<category>/<photo_name>/remove')
def photo_remove(category, photo_name):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_photo"]:
        return abort(404)

    form = load_html_shard('photo/confirm_remove')
    diary_main = load_html_shard('diary/main')

    category_list = get_list()

    arg = {"{entry_list}": render_list(category_list, category),
           "{entry_content}": form,
           "{category}": category,
           "{name}": photo_name,
           "{photo_path}": get_entry(category, photo_name).path}
    diary_main = fill_args(diary_main, arg)

    return render_mainpage(diary_main, "photo", "diary")
