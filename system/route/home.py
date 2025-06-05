from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.renderer import load_html_shard, get_html_file, fill_args, render_mainpage
import yaml


@app.route('/')
def home():
    home_html = load_html_shard('common/home')
    home_content = get_html_file('data/home_content.html')
    home_bio = get_html_file('data/bio.html')

    with open("data/todays_feeling.yaml", "r", encoding="utf-8") as j:
        feeling = yaml.load(j, yaml.FullLoader)
    todays_feeling = feeling["feeling"]

    arg = {
        "{todays_feeling_name}": site_settings()["todays_feeling_name"],
        "{todays_feeling}": todays_feeling,
        "{home_content}": home_content,
        "{bio}": home_bio
    }
    home_html = fill_args(home_html, arg)

    return render_mainpage(home_html, "home", "main")
