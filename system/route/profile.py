from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.renderer import load_html_shard, render_mainpage, fill_args
from system.tool.auth import is_admin
from system.object.profile import render_list, get_entry, get_list
from flask import abort, request


@app.route('/profile')
def profile_home():
    if not site_settings()["use_profile"]:
        return abort(404)
    placeholder_info = load_html_shard('profile/content_placeholder')
    placeholder_no_entry = load_html_shard('profile/content_no_entry')
    diary_main = load_html_shard('diary/main')

    diary_list = get_list()

    arg = {"{entry_list}": render_list(diary_list),
           "{entry_content}": placeholder_no_entry if len(diary_list) == 0 else placeholder_info}
    diary_main = fill_args(diary_main, arg)

    return render_mainpage(diary_main, "profile", "diary")


# 프로필 보기
@app.route('/profile/<entry>')
def profile_entry(entry):
    if not site_settings()["use_profile"]:
        return abort(404)
    # load yaml
    try:
        if ".." in entry:
            return abort(404)
        d = get_entry(entry)
        if d.auto_wrap:
            d.content = d.content.replace("\n", "<br>")
    except FileNotFoundError:
        return abort(404)

    diary_main = load_html_shard('diary/main')
    profile_content = load_html_shard('profile/content')

    # ===== Content =====
    profile_content = fill_args(profile_content, {"{entry_content}": d.content})

    # ===== Admin Context =====
    if is_admin(request)[0]:
        manage = load_html_shard('profile/manage')
        manage = manage.replace("{filename}", entry)
        profile_content += manage

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, entry),
           "{entry_content}": profile_content}
    diary_main = fill_args(diary_main, arg)

    # ===== make main html =====
    return render_mainpage(diary_main, "profile", "diary")
