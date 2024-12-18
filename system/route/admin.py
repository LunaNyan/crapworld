from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer
from flask import request
import yaml


@app.route('/admin')
def admin_home():
    home_html = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/diary_main.html')
    home_content = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/admin_main_content.html')

    arg = {
        "{entry_content}": home_content,
        "{ip}": request.remote_addr
    }
    home_html = renderer.fill_args(home_html, arg)

    return renderer.admin_render_mainpage(home_html, "admin", "diary")
