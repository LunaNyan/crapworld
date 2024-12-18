from system.tool.etc import cnv_path
from os import listdir
import yaml
import operator
import locale


locale.setlocale(locale.LC_TIME, "ko_KR.UTF-8")


class DiaryEntry:
    def __init__(self, filename, title, written_at, auto_wrap, unlisted, content=None):
        self.filename = filename
        self.title = title
        self.written_at = written_at
        self.auto_wrap = auto_wrap
        self.unlisted = unlisted
        self.content = content


def get_list():
    dir_list = listdir(cnv_path("data/diary"))
    dl: list[DiaryEntry] = []
    for i in dir_list:
        if not i.endswith('.yaml'):
            continue
        with open(cnv_path(f"data/diary/{i}"), "r", encoding="utf-8") as f:
            d = yaml.load(f, yaml.FullLoader)
            if d['unlisted']:
                continue
            dl.append(DiaryEntry(
                    filename=i.replace(".yaml", ""),
                    title=d['title'],
                    written_at=d['written_at'],
                    auto_wrap=d['auto_wrap'],
                    unlisted=d['unlisted']
            ))
    # written_at을 대조하여 최근 - 과거 순으로 정렬한다.
    dl = sorted(dl, key=operator.attrgetter('written_at'), reverse=True)
    return dl


def get_entry(fname):
    with open(cnv_path(f"data/diary/{fname}.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
        res = DiaryEntry(
                filename=fname,
                title=d['title'],
                written_at=d['written_at'],
                auto_wrap=d['auto_wrap'],
                unlisted=d['unlisted'],
                content=d['content']
        )
    return res