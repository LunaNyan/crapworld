from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.renderer import load_html_shard, render_mainpage, fill_args
from system.tool.auth import is_admin
from system.object.diary import (
    DiaryEntry, render_list, get_entry, get_list, remove_entry, add_entry)
from flask import abort, request, redirect
from datetime import datetime
from uuid import uuid4


# 프로필 추가 요청 POST에 대한 처리
@app.route('/diary/post', methods=['POST'])
def diary_post():
    if not is_admin(request)[0]:  # use_admin이 false이거나 사용 가능한 IP가 아닌 경우
        return abort(404)
    if not site_settings()["use_diary"]:  # use_profile이 false인 경우
        return abort(404)

    title = request.form['title']
    filename = request.form['filename']

    if filename == "":
        filename = str(uuid4())

    content = request.form['content']
    is_unlisted = request.form.get('unlisted')
    is_auto_wrap = request.form.get('auto_wrap')

    entry = DiaryEntry(
            filename=filename,
            title=title,
            written_at=datetime.now().timestamp(),
            auto_wrap=True if is_auto_wrap is not None else False,
            unlisted=True if is_unlisted is not None else False,
            content=content
    )

    add_entry(entry)
    return redirect(location=f"/diary/{filename}")


# 수정하기
@app.route('/diary/<entry>/edit')
def diary_edit(entry):
    if not is_admin(request)[0]:  # use_admin이 false이거나 사용 가능한 IP가 아닌 경우
        return abort(404)
    if not site_settings()["use_diary"]:  # use_profile이 false인 경우
        return abort(404)

    diary_main = load_html_shard('diary/main')
    profile_content = load_html_shard('diary/editor')

    curr_entry = get_entry(entry)

    args = {
        "{page_title}": "수정하기",
        "{title}": curr_entry.title,
        "{filename}": curr_entry.filename,
        "{content}": curr_entry.content,
        "{auto_wrap_is_checked}": " checked" if curr_entry.auto_wrap else "",
        "{unlisted_is_checked}": " checked" if curr_entry.unlisted else ""
    }
    profile_content = fill_args(profile_content, args)

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, "add_item"),
           "{entry_content}": profile_content}
    diary_main = fill_args(diary_main, arg)

    # ===== make main html =====
    return render_mainpage(diary_main, "profile", "diary")


# 새로 만들기
@app.route('/diary/add_item')
def diary_add():
    if not is_admin(request)[0]:  # use_admin이 false이거나 사용 가능한 IP가 아닌 경우
        return abort(404)
    if not site_settings()["use_diary"]:  # use_profile이 false인 경우
        return abort(404)

    diary_main = load_html_shard('diary/main')
    profile_content = load_html_shard('diary/editor')

    args = {
        "{page_title}": "새로 만들기",
        "{title}": "",
        "{filename}": "",
        "{content}": "",
        "{auto_wrap_is_checked}": "",
        "{unlisted_is_checked}": ""
    }
    profile_content = fill_args(profile_content, args)

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, "add_item"),
           "{entry_content}": profile_content}
    diary_main = fill_args(diary_main, arg)

    # ===== make main html =====
    return render_mainpage(diary_main, "diary", "diary")


# 프로필 삭제하기 전 질문
@app.route('/diary/<entry>/remove')
def diary_confirm_remove(entry):
    if not is_admin(request)[0]:  # use_admin이 false이거나 사용 가능한 IP가 아닌 경우
        return abort(404)
    if not site_settings()["use_diary"]:  # use_profile이 false인 경우
        return abort(404)

    # load yaml
    try:
        if ".." in entry:
            return abort(404)
        d = get_entry(entry)
    except FileNotFoundError:
        return abort(404)

    diary_main = load_html_shard('diary/main')
    profile_content = load_html_shard('diary/confirm_remove')

    # ===== Content =====
    args = {
        "{title}": d.title,
        "{filename}": d.filename
    }
    content = fill_args(profile_content, args)

    # ===== Admin Context =====
    if is_admin(request)[0]:
        manage = load_html_shard('diary/manage')
        manage = manage.replace("{filename}", entry)
        profile_content += manage

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, entry),
           "{entry_content}": content}
    diary_main = fill_args(diary_main, arg)

    # ===== make main html =====
    return render_mainpage(diary_main, "diary", "diary")


# 삭제
@app.route('/diary/<entry>/confirm_remove')
def diary_remove(entry):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_diary"]:
        return abort(404)
    remove_entry(entry)
    return redirect(location="/diary")
