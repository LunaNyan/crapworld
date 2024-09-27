from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer
from flask import abort
import yaml


@app.route('/guestbook')
def guestbook():
    if not site_settings["use_guestbook"]:
        return abort(404)
    home_html = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/home.html')
    home_bio = renderer.get_html_file('data/bio.html')
    gallery_content = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/guestbook.html')
    gallery_content = renderer.fill_args(gallery_content,
                                         {"{guest_ap_id}": site_settings["guest_ap_id"]})

    with open("data/todays_feeling.yaml", "r", encoding="utf-8") as j:
        feeling = yaml.load(j, yaml.FullLoader)
    todays_feeling = feeling["feeling"]

    arg = {
        "{todays_feeling_name}": site_settings["todays_feeling_name"],
        "{todays_feeling}": todays_feeling,
        "{home_content}": gallery_content,
        "{bio}": home_bio
    }
    home_html = renderer.fill_args(home_html, arg)

    return renderer.render_mainpage(home_html, "guestbook", "gallery")
