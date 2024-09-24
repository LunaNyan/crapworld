from system.engine.server import app
from system.tool import main_renderer
from system.tool.dirpath_delimiter import cnv_path

settings = main_renderer.get_settings()


@app.route('/')
def home():
    html = main_renderer.basepage(menu_mode=1)
    site_settings = main_renderer.get_settings()
    html = html.replace('{content}', main_renderer.get_html_file(
            cnv_path(f'theme/{settings["theme"]}/html/home.html')))
    html = html.replace('{home_content}', main_renderer.get_html_file(
            cnv_path('data/home_content.html')))
    html = html.replace('{extra_css}', 'main')
    html = html.replace('{bio}', site_settings['bio'])
    return html
