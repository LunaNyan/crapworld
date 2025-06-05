from system.engine.server import app
from system.engine.settings import site_settings, save_settings
from system.tool.renderer import load_html_shard, render_mainpage, fill_args
from system.tool.auth import is_admin
from system.route.admin import render_list
from flask import request, abort, redirect
from os import listdir
from os.path import isdir


@app.route('/admin/content/settings/post', methods=['POST'])
def admin_settings_general_post():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)

    settings_to_save = site_settings()
    settings_to_save["theme"] = request.form.get('theme')
    settings_to_save["site_title"] = request.form.get('site_title')
    settings_to_save["hompy_title"] = request.form.get('hompy_title')
    settings_to_save["site_url"] = request.form.get('site_url')
    settings_to_save["todays_feeling_name"] = request.form.get('todays_feeling_name')
    settings_to_save["home_tab_name"] = request.form.get('home_tab_name')
    settings_to_save["profile_tab_name"] = request.form.get('profile_tab_name')
    settings_to_save["diary_tab_name"] = request.form.get('diary_tab_name')
    settings_to_save["photo_tab_name"] = request.form.get('photo_tab_name')
    settings_to_save["gallery_tab_name"] = request.form.get('gallery_tab_name')
    settings_to_save["guestbook_tab_name"] = request.form.get('guestbook_tab_name')
    settings_to_save["video_tab_name"] = request.form.get('video_tab_name')
    settings_to_save["use_profile"] = request.form.get('use_profile')
    settings_to_save["profile_header_name"] = request.form.get('profile_header_name')
    settings_to_save["use_diary"] = request.form.get('use_diary')
    settings_to_save["use_photo"] = request.form.get('use_photo')
    settings_to_save["use_gallery"] = request.form.get('use_gallery')
    settings_to_save["gallery_sns_type"] = request.form.get('gallery_sns_type')
    settings_to_save["gallery_sns_id"] = request.form.get('gallery_sns_id')
    settings_to_save["use_video"] = request.form.get('use_video')
    settings_to_save["use_guestbook"] = request.form.get('use_guestbook')
    settings_to_save["guest_ap_id"] = request.form.get('guest_ap_id')
    settings_to_save["photo_use_thumbnail"] = request.form.get('photo_use_thumbnail')
    settings_to_save["photo_thumbnail_size"] = int(request.form.get('photo_thumbnail_size'))
    settings_to_save["show_admin_tab"] = request.form.get('show_admin_tab')

    save_settings(settings_to_save)
    return redirect(location=f"/admin/content/settings")


@app.route('/admin/content/settings')
def admin_settings_general():
    if not is_admin(request)[0]:
        return abort(404)
    if not site_settings()["use_admin"]:
        return abort(404)
    admin_html = load_html_shard('diary/main')
    admin_content = load_html_shard('admin/settings_general')

    # themes list
    themes = ""
    for i in listdir("theme"):
        if isdir(f"theme/{i}"):
            if i == site_settings()["theme"]:
                themes += f"<option value=\"{i}\" selected>{i}</option>\n"
            else:
                themes += f"<option value=\"{i}\">{i}</option>\n"

    arg = {
        # 필수
        "{entry_content}": admin_content,
        "{entry_list}": render_list("settings"),
        # 기본 설정
        "{site_title}": site_settings()["site_title"],
        "{hompy_title}": site_settings()["hompy_title"],
        "{site_url}": site_settings()["site_url"],
        # UI - 탭 이름
        "{todays_feeling_name}": site_settings()["todays_feeling_name"],
        "{home_tab_name}": site_settings()["home_tab_name"],
        "{profile_tab_name}": site_settings()["profile_tab_name"],
        "{diary_tab_name}": site_settings()["diary_tab_name"],
        "{photo_tab_name}": site_settings()["photo_tab_name"],
        "{gallery_tab_name}": site_settings()["gallery_tab_name"],
        "{guestbook_tab_name}": site_settings()["guestbook_tab_name"],
        "{video_tab_name}": site_settings()["video_tab_name"],
        "{theme_options}": themes,
        # UI - 탭 사용 여부
        "{use_profile}": " checked" if site_settings()["use_profile"] else "",
        "{use_diary}": " checked" if site_settings()["use_diary"] else "",
        "{use_photo}": " checked" if site_settings()["use_photo"] else "",
        "{use_gallery}": " checked" if site_settings()["use_gallery"] else "",
        "{use_guestbook}": " checked" if site_settings()["use_guestbook"] else "",
        "{use_video}": " checked" if site_settings()["use_video"] else "",
        # 탭 관련 설정들
        "{profile_header_name}": site_settings()["profile_header_name"],
        "{photo_use_thumbnail}": " checked" if site_settings()["photo_use_thumbnail"] else "",
        "{photo_thumbnail_size}": str(site_settings()["photo_thumbnail_size"]),
        "{instagram}": " checked" if site_settings()["gallery_sns_type"] == "instagram" else "",
        "{twitter}": " checked" if site_settings()["gallery_sns_type"] == "twitter" else "",
        "{gallery_sns_id}": site_settings()["gallery_sns_id"],
        "{guest_ap_id}": site_settings()["guest_ap_id"],
        "{show_admin_tab}": " checked" if site_settings()["show_admin_tab"] else ""
    }
    admin_html = fill_args(admin_html, arg)

    return render_mainpage(admin_html, "admin", "diary")
