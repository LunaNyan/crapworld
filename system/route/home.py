from idlelib.iomenu import encoding

from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer
from system.tool.etc import cnv_path
import yaml


@app.route('/')
def home():
    home_html = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/home.html')
    home_content = renderer.get_html_file('data/home_content.html')
    home_bio = renderer.get_html_file('data/bio.html')

    with open("data/todays_feeling.yaml", "r", encoding="utf-8") as j:
        feeling = yaml.load(j, yaml.FullLoader)
    todays_feeling = feeling["feeling"]

    arg = {
        "{todays_feeling_name}": site_settings["todays_feeling_name"],
        "{todays_feeling}": todays_feeling,
        "{home_content}": home_content,
        "{bio}": home_bio
    }
    home_html = renderer.fill_args(home_html, arg)

    return renderer.render_mainpage(home_html, "home", "main")
