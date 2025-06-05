from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.renderer import load_html_shard, get_html_file, fill_args, render_mainpage
from flask import abort
import yaml


@app.route('/gallery')
def gallery():
    if not site_settings()["use_gallery"]:
        return abort(404)
    home_html = load_html_shard('common/home')
    home_bio = get_html_file('data/bio.html')
    sns_type = site_settings()["gallery_sns_type"]
    gallery_content = load_html_shard(f'etc/gallery_{sns_type}')
    gallery_content = fill_args(gallery_content,
                                         {"{sns_id}": site_settings()["gallery_sns_id"]})

    with open("data/todays_feeling.yaml", "r", encoding="utf-8") as j:
        feeling = yaml.load(j, yaml.FullLoader)
    todays_feeling = feeling["feeling"]

    arg = {
        "{todays_feeling_name}": site_settings()["todays_feeling_name"],
        "{todays_feeling}": todays_feeling,
        "{home_content}": gallery_content,
        "{bio}": home_bio
    }
    home_html = fill_args(home_html, arg)

    return render_mainpage(home_html, "gallery", "gallery")
