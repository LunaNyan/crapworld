from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer
from system.tool.etc import cnv_path
from os import listdir
from flask import abort
import yaml


class ProfileEntry:
    def __init__(self, filename, title, auto_wrap, unlisted, content=None):
        self.filename = filename
        self.title = title
        self.auto_wrap = auto_wrap
        self.unlisted = unlisted
        self.content = content


def get_list():
    dir_list = sorted(listdir(cnv_path("data/profile")))
    dl: list[ProfileEntry] = []
    for i in dir_list:
        if not i.endswith('.yaml'):
            continue
        with open(cnv_path(f"data/profile/{i}"), "r", encoding="utf-8") as f:
            d = yaml.load(f, yaml.FullLoader)
            if d['unlisted']:
                continue
            dl.append(ProfileEntry(
                    filename=i.replace(".yaml", ""),
                    title=d['title'],
                    auto_wrap=d['auto_wrap'],
                    unlisted=d['unlisted']
            ))
    return dl


def get_entry(fname):
    with open(cnv_path(f"data/profile/{fname}.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
        res = ProfileEntry(
                filename=fname,
                title=d['title'],
                auto_wrap=d['auto_wrap'],
                unlisted=d['unlisted'],
                content=d['content']
        )
    return res


def render_list(profile_list: list[ProfileEntry], current=None):
    html_delimiter = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_delimiter.html")
    html_delimiter_end = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_delimiter_end.html")
    html_list_item = renderer.get_html_file(f"theme/{site_settings['theme']}/html/profile_list_item.html")
    html_list_item_cur = renderer.get_html_file(f"theme/{site_settings['theme']}/html/profile_list_item_current.html")
    ht = html_delimiter.replace("{group_title}", site_settings["profile_header_name"])
    for i in profile_list:
        # 지금 보고있는 엔트리인가?
        if i.filename == current:
            ht2 = html_list_item_cur.replace('{title}', i.title)
        else:
            ht2 = html_list_item.replace('{title}', i.title)
            ht2 = ht2.replace('{filename}', i.filename)
        ht += ht2
    ht += html_delimiter_end
    return ht


@app.route('/profile')
def profile_home():
    if not site_settings["use_profile"]:
        return abort(404)
    placeholder_info = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/profile_content_placeholder.html')
    placeholder_no_entry = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/profile_content_no_entry.html')
    diary_main = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_main.html')

    diary_list = get_list()

    arg = {"{entry_list}": render_list(diary_list),
           "{entry_content}": placeholder_no_entry if len(diary_list) == 0 else placeholder_info}
    diary_main = renderer.fill_args(diary_main, arg)

    return renderer.render_mainpage(diary_main, "profile", "diary")


@app.route('/profile/<entry>')
def profile_entry(entry):
    if not site_settings["use_profile"]:
        return abort(404)
    # load yaml
    try:
        if ".." in entry:
            return abort(404)
        d = get_entry(entry)
        if d.auto_wrap:
            d.content = d.content.replace("\n", "<br>")
    except FileNotFoundError:
        return abort(404)

    diary_main = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_main.html')
    profile_content = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/profile_content.html')

    # ===== Content =====
    profile_content = renderer.fill_args(profile_content, {"{entry_content}": d.content})

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, entry),
           "{entry_content}": profile_content}
    diary_main = renderer.fill_args(diary_main, arg)

    # ===== make main html =====
    return renderer.render_mainpage(diary_main, "profile", "diary")
