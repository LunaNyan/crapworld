from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.renderer import load_html_shard, render_mainpage, fill_args
from system.tool.auth import is_admin
from system.object.diary import render_list, get_entry, get_list
from datetime import datetime
from flask import abort, request


@app.route('/diary')
def diary_home():
    if not site_settings()["use_diary"]:
        return abort(404)
    placeholder_info = load_html_shard('diary/content_placeholder')
    placeholder_no_entry = load_html_shard('diary/content_no_entry')
    diary_main = load_html_shard('diary/main')

    diary_list = get_list()

    arg = {"{entry_list}": render_list(diary_list),
           "{entry_content}": placeholder_no_entry if len(diary_list) == 0 else placeholder_info}
    diary_main = fill_args(diary_main, arg)

    return render_mainpage(diary_main, "diary", "diary")


@app.route('/diary/<entry>')
def diary_entry(entry):
    if not site_settings()["use_diary"]:
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
    diary_content = load_html_shard('diary/content')

    # written_at
    dt = datetime.fromtimestamp(d.written_at).strftime('%x(%a) %X')
    # escape surrogate
    dt = dt.encode('utf8', 'surrogateescape').decode('utf8', 'surrogateescape')

    # ===== Content =====
    arg = {
        "{title}": d.title,
        "{written_at}": dt + ('<br>미공개' if d.unlisted else ''),
        "{entry_content}": d.content
    }
    diary_content = fill_args(diary_content, arg)

    # ===== Admin Context =====
    if is_admin(request)[0]:
        manage = load_html_shard('diary/manage')
        manage = manage.replace("{filename}", entry)
        diary_content += manage

    # ===== Diary List =====
    diary_list = get_list()
    arg = {"{entry_list}": render_list(diary_list, entry),
           "{entry_content}": diary_content}
    diary_main = fill_args(diary_main, arg)

    # ===== make main html =====
    return render_mainpage(diary_main, "diary", "diary")
