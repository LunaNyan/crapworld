from os import listdir
from system.tool.etc import cnv_path
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
