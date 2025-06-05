from system.tool.etc import cnv_path
from system.tool.auth import is_admin
from system.tool.renderer import load_html_shard
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
            if d['unlisted'] and not is_admin(request):
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
    html_delimiter = load_html_shard("diary/delimiter")
    html_delimiter_end = load_html_shard("diary/delimiter_end")
    html_list_item = load_html_shard("profile/list_item")
    html_list_item_cur = load_html_shard("profile/list_item_current")
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
    if is_admin(request)[0]:
        if current == "add_item":
            ht2 = html_list_item_cur.replace('{title}', "<b>새로 만들기</b>")
            ht2 = ht2.replace('{filename}', 'add_item')
        else:
            ht2 = html_list_item.replace('{title}', "<b>새로 만들기</b>")
            ht2 = ht2.replace('{filename}', 'add_item')
        ht += ht2
    ht += html_delimiter_end
    return ht
