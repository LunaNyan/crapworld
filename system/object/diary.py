from system.tool.auth import is_admin
from system.tool.renderer import load_html_shard
from system.tool.etc import cnv_path
from os import listdir, remove
from datetime import datetime
from flask import request
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
            if d['unlisted'] and not is_admin(request):
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


def add_entry(entry: DiaryEntry):
    with open(cnv_path(f"data/diary/{entry.filename}.yaml"), "w", encoding="utf-8") as f:
        yaml_data = {
            "title": entry.title,
            "written_at": datetime.now().timestamp(),
            "auto_wrap": entry.auto_wrap,
            "unlisted": entry.unlisted,
            "content": entry.content
        }
        yaml.dump(yaml_data, f)


def remove_entry(fname):
    try:
        remove(cnv_path(f"data/diary/{fname}.yaml"))
    except FileNotFoundError:
        pass


def render_list(diary_list: list[DiaryEntry], current=None):
    html_delimiter = load_html_shard("diary/delimiter")
    html_delimiter_end = load_html_shard("diary/delimiter_end")
    html_list_item = load_html_shard("diary/list_item")
    html_list_item_cur = load_html_shard("diary/list_item_current")
    prev_month = 0
    ht = ""
    # admin인 경우 새로 만들 수 있음
    if is_admin(request)[0]:
        ht += html_delimiter.replace("{group_title}", "")
        if current == "add_item":
            ht2 = html_list_item_cur.replace('{day} | <b>{title}</b>', "<b>새로 만들기</b>")
            ht2 = ht2.replace('{filename}', 'add_item')
        else:
            ht2 = html_list_item.replace('{day} | {title}', "<b>새로 만들기</b>")
            ht2 = ht2.replace('{filename}', 'add_item')
        ht += ht2
        ht += html_delimiter_end
    for i in diary_list:
        dt = datetime.fromtimestamp(i.written_at)
        # 월자가 바뀐 경우 delimiter를 넣는다.
        if dt.month != prev_month:
            if not prev_month == 0:
                ht += html_delimiter_end
            ht += html_delimiter.replace("{group_title}", f"{dt.year}년 {dt.month}월")
        # 지금 보고있는 엔트리인가?
        if i.filename == current:
            ht2 = html_list_item_cur.replace('{title}', i.title)
        else:
            ht2 = html_list_item.replace('{title}', i.title)
            ht2 = ht2.replace('{filename}', i.filename)
        ht += ht2.replace('{day}', str(dt.day))
        prev_month = dt.month
    ht += html_delimiter_end
    return ht
