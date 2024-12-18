from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer, ip_filter
from flask import request, abort


@app.route('/admin')
def admin_home():
    if not ip_filter.if_local(request):
        return abort(404)
    admin_html = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    admin_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/admin_main_content.html')

    arg = {
        "{entry_content}": admin_content,
        "{entry_list}": "",
        "{ip}": request.remote_addr
    }
    admin_html = renderer.fill_args(admin_html, arg)

    return renderer.admin_render_mainpage(admin_html, "admin", "diary")
