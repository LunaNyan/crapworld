from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.ip_filter import is_admin
from system.tool import renderer
from system.object.photo import render_list, get_list, add_category, upload_pic, add_entry
from flask import abort, request, redirect


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

    form = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/photo_add_category.html')
    diary_main = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')

    category_list = get_list()

    arg = {"{entry_list}": render_list(category_list, "add_item"),
           "{entry_content}": form}
    diary_main = renderer.fill_args(diary_main, arg)

    return renderer.render_mainpage(diary_main, "photo", "diary")


@app.route('/photo/<category>/add_item', methods=['POST'])
def photo_add_item_post(category):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_photo"]:
        return abort(404)

    slug = request.form.get('name')
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

    form = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/photo_add_item.html')
    diary_main = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')

    category_list = get_list()

    arg = {"{entry_list}": render_list(category_list, category),
           "{entry_content}": form,
           "{category}": category}
    diary_main = renderer.fill_args(diary_main, arg)

    return renderer.render_mainpage(diary_main, "photo", "diary")
