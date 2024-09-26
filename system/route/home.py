from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer


@app.route('/')
def home():
    home_html = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/home.html')
    home_content = renderer.get_html_file('data/home_content.html')
    home_bio = renderer.get_html_file('data/bio.html')

    arg = {
        "{home_content}": home_content,
        "{bio}": home_bio
    }
    home_html = renderer.fill_args(home_html, arg)

    return renderer.render_mainpage(home_html, "home", "main")
