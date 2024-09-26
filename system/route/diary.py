from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer
from system.tool.etc import cnv_path
from os import listdir
from datetime import datetime
from flask import abort
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


def render_list(diary_list: list[DiaryEntry], current=None):
    html_delimiter = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_delimiter.html")
    html_delimiter_end = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_delimiter_end.html")
    html_list_item = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_list_item.html")
    html_list_item_cur = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_list_item_current.html")
    prev_month = 0
    ht = ""
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


@app.route('/diary')
def diary_home():
    if not site_settings["use_diary"]:
        return abort(404)
    placeholder_info = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_content_placeholder.html')
    placeholder_no_entry = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_content_no_entry.html')
    diary_main = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_main.html')

    diary_list = get_list()

    arg = {"{entry_list}": render_list(diary_list),
           "{entry_content}": placeholder_no_entry if len(diary_list) == 0 else placeholder_info}
    diary_main = renderer.fill_args(diary_main, arg)

    return renderer.render_mainpage(diary_main, "diary", "diary")


@app.route('/diary/<entry>')
def diary_entry(entry):
    if not site_settings["use_diary"]:
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
    diary_content = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_content.html')

    # written_at
    dt = datetime.fromtimestamp(d.written_at).strftime('%x(%a) %X')
    # escape surrogate
    dt = dt.encode('utf8', 'surrogateescape').decode('utf8', 'surrogateescape')

    # ===== Content =====
    arg = {
        "{title}": d.title,
        "{written_at}": dt + ('<br>미공개' if d.unlisted else ''),
        "{entry_content}": d.content
    }
    diary_content = renderer.fill_args(diary_content, arg)

    # ===== Diary List =====
    diary_list = get_list()
    arg = {"{entry_list}": render_list(diary_list, entry),
           "{entry_content}": diary_content}
    diary_main = renderer.fill_args(diary_main, arg)

    # ===== make main html =====
    return renderer.render_mainpage(diary_main, "diary", "diary")
