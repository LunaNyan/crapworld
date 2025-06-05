from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.auth import is_admin
from system.tool.renderer import load_html_shard, fill_args, render_mainpage
from system.object.photo import render_list, get_list, get_entry
from datetime import datetime
from flask import abort, request


@app.route('/photo')
def photo_main():
    if not site_settings()["use_profile"]:
        return abort(404)
    placeholder_info = load_html_shard('photo/content_placeholder')
    placeholder_no_entry = load_html_shard('photo/content_no_entry')
    diary_main = load_html_shard('diary/main')

    category_list = get_list()

    arg = {"{entry_list}": render_list(category_list),
           "{entry_content}": placeholder_no_entry if len(category_list) == 0 else placeholder_info}
    diary_main = fill_args(diary_main, arg)

    return render_mainpage(diary_main, "photo", "photo")


@app.route('/photo/<category>/<photo_name>')
def photo_detail(category, photo_name):
    if not site_settings()["use_photo"]:
        return abort(404)
    if ".." in category:
        return abort(404)

    diary_main = load_html_shard('diary/main')
    photo_content = load_html_shard('photo/detail')
    photo_manage = load_html_shard('photo/manage')

    # load data
    try:
        d = get_entry(category, photo_name)
    except KeyError:
        print("keyerror")
        return abort(404)

    # written_at
    dt = datetime.fromtimestamp(d.uploaded_at).strftime('%x(%a) %X')
    # escape surrogate
    dt = dt.encode('utf8', 'surrogateescape').decode('utf8', 'surrogateescape')

    # is admin?
    if is_admin(request)[0]:
        dt += "\n<br><br>\n" + photo_manage + "\n"

    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, category),
           "{entry_content}": photo_content,
           "{photo_path}": d.path,
           "{description}": d.description,
           "{uploaded_at}": dt,
           "{category}": category,
           "{filename}": photo_name}
    diary_main = fill_args(diary_main, arg)

    # ===== make main html =====
    return render_mainpage(diary_main, "photo", "diary")


@app.route('/photo/<category>')
def photo_category(category):
    if not site_settings()["use_photo"]:
        return abort(404)
    if ".." in category:
        return abort(404)

    diary_main = load_html_shard('diary/main')

    # ===== Content =====
    main_content = ""
    photo_content = load_html_shard('photo/entry')
    photo_new = load_html_shard('photo/new')

    # load data
    d = get_list()
    try:
        for photo in d[category].photos:
            arg = {"{img_path}": photo.path,
                   "{thumbnail_path}": "/thumbnail/" + photo.thumbnail_path,
                   "{img_name}": f"/photo/{category}/{photo.name}",
                   "{description}": photo.description}
            main_content += fill_args(photo_content, arg)
    except KeyError:
        return abort(404)

    if is_admin(request)[0]:
        arg = {"{category}": category}
        main_content += fill_args(photo_new, arg)

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, category),
           "{entry_content}": main_content}
    diary_main = fill_args(diary_main, arg)

    # ===== make main html =====
    return render_mainpage(diary_main, "photo", "photo")
