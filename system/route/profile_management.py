from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer
from system.tool.ip_filter import is_admin
from system.object.profile import (
    ProfileEntry, render_list, get_entry, get_list, remove_entry, add_entry)
from flask import abort, request, redirect


# 프로필 추가 요청 POST에 대한 처리
@app.route('/profile/post', methods=['POST'])
def profile_post():
    if not is_admin(request)[0]:  # use_admin이 false이거나 사용 가능한 IP가 아닌 경우
        return abort(404)
    if not site_settings()["use_profile"]:  # use_profile이 false인 경우
        return abort(404)
    title = request.form['title']
    filename = request.form['filename']
    content = request.form['content']
    is_unlisted = request.form.get('unlisted')
    is_auto_wrap = request.form.get('auto_wrap')

    entry = ProfileEntry(
        filename=filename,
        title=title,
        auto_wrap=True if is_auto_wrap is not None else False,
        unlisted=True if is_unlisted is not None else False,
        content=content
    )

    add_entry(entry)
    return redirect(location=f"/profile/{filename}")


# 수정하기
@app.route('/profile/<entry>/edit')
def profile_edit(entry):
    if not is_admin(request)[0]:  # use_admin이 false이거나 사용 가능한 IP가 아닌 경우
        return abort(404)
    if not site_settings()["use_profile"]:  # use_profile이 false인 경우
        return abort(404)

    diary_main = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    profile_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/profile_editor.html')

    curr_entry = get_entry(entry)

    args = {
        "{page_title}": "수정하기",
        "{title}": curr_entry.title,
        "{filename}": curr_entry.filename,
        "{content}": curr_entry.content,
        "{auto_wrap_is_checked}": " checked" if curr_entry.auto_wrap else "",
        "{unlisted_is_checked}": " checked" if curr_entry.unlisted else ""
    }
    profile_content = renderer.fill_args(profile_content, args)

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, "add_item"),
           "{entry_content}": profile_content}
    diary_main = renderer.fill_args(diary_main, arg)

    # ===== make main html =====
    return renderer.render_mainpage(diary_main, "profile", "diary")


# 새로 만들기
@app.route('/profile/add_item')
def profile_add():
    if not is_admin(request)[0]:  # use_admin이 false이거나 사용 가능한 IP가 아닌 경우
        return abort(404)
    if not site_settings()["use_profile"]:  # use_profile이 false인 경우
        return abort(404)

    diary_main = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    profile_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/profile_editor.html')

    args = {
        "{page_title}": "새로 만들기",
        "{title}": "",
        "{filename}": "",
        "{content}": "",
        "{auto_wrap_is_checked}": "",
        "{unlisted_is_checked}": ""
    }
    profile_content = renderer.fill_args(profile_content, args)

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, "add_item"),
           "{entry_content}": profile_content}
    diary_main = renderer.fill_args(diary_main, arg)

    # ===== make main html =====
    return renderer.render_mainpage(diary_main, "profile", "diary")


# 프로필 삭제하기 전 질문
@app.route('/profile/<entry>/remove')
def profile_confirm_remove(entry):
    if not is_admin(request)[0]:  # use_admin이 false이거나 사용 가능한 IP가 아닌 경우
        return abort(404)
    if not site_settings()["use_profile"]:  # use_profile이 false인 경우
        return abort(404)

    # load yaml
    try:
        if ".." in entry:
            return abort(404)
        d = get_entry(entry)
    except FileNotFoundError:
        return abort(404)

    diary_main = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    profile_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/profile_confirm_remove.html')

    # ===== Content =====
    args = {
        "{title}": d.title,
        "{filename}": d.filename
    }
    profile_content = renderer.fill_args(profile_content, args)

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, entry),
           "{entry_content}": profile_content}
    diary_main = renderer.fill_args(diary_main, arg)

    # ===== make main html =====
    return renderer.render_mainpage(diary_main, "profile", "diary")


# 프로필 삭제
@app.route('/profile/<entry>/confirm_remove')
def profile_remove(entry):
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_profile"]:
        return abort(404)
    remove_entry(entry)
    return redirect(location="/profile")
