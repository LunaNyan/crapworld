from system.tool.etc import cnv_path
from system.tool.ip_filter import if_admin
from system.tool import renderer
from system.engine.settings import site_settings
from flask import request
from os import listdir, remove
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


def add_entry(entry: ProfileEntry):
    with open(cnv_path(f"data/profile/{entry.filename}.yaml"), "w", encoding="utf-8") as f:
        yaml_data = {
            "title": entry.title,
            "auto_wrap": entry.auto_wrap,
            "unlisted": entry.unlisted,
            "content": entry.content
        }
        yaml.dump(yaml_data, f)


def remove_entry(fname):
    try:
        remove(cnv_path(f"data/profile/{fname}.yaml"))
    except FileNotFoundError:
        pass


def render_list(profile_list: list[ProfileEntry], current=None):
    html_delimiter = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/diary_delimiter.html")
    html_delimiter_end = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/diary_delimiter_end.html")
    html_list_item = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/profile_list_item.html")
    html_list_item_cur = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/profile_list_item_current.html")
    ht = html_delimiter.replace("{group_title}", site_settings()["profile_header_name"])
    for i in profile_list:
        # 지금 보고있는 엔트리인가?
        if i.filename == current:
            ht2 = html_list_item_cur.replace('{title}', i.title)
        else:
            ht2 = html_list_item.replace('{title}', i.title)
            ht2 = ht2.replace('{filename}', i.filename)
        ht += ht2
    # admin인 경우 새로 만들 수 있음
    if if_admin(request):
        if current == "add_item":
            ht2 = html_list_item_cur.replace('{title}', "<b>새로 만들기</b>")
            ht2 = ht2.replace('{filename}', 'add_item')
        else:
            ht2 = html_list_item.replace('{title}', "<b>새로 만들기</b>")
            ht2 = ht2.replace('{filename}', 'add_item')
        ht += ht2
    ht += html_delimiter_end
    return ht
