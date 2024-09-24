from system.engine.server import app
from system.tool import main_renderer
from system.tool.dirpath_delimiter import cnv_path
from os import listdir
from datetime import datetime
import yaml


class DiaryEntry:
    def __init__(self, filename, title, written_at, content=None):
        self.filename = filename
        self.title = title
        self.written_at = written_at
        self.content = content


def get_list():
    dir_list = sorted(listdir(cnv_path("data/diary")))
    dl: list[DiaryEntry] = []
    for i in dir_list:
        if not i.endswith('.yaml'):
            continue
        with open(cnv_path(f"data/diary/{i}")) as f:
            d = yaml.load(f, yaml.FullLoader)
            dl.append(DiaryEntry(
                    filename=i,
                    title=d['title'],
                    written_at=d['written_at']
            ))
    return dl


def get_entry(fname):
    with open(cnv_path(f"data/diary/{fname}")) as f:
        d = yaml.load(f, yaml.FullLoader)
        res = DiaryEntry(
                filename=fname,
                title=d['title'],
                written_at=d['written_at'],
                content=d['content']
        )
    return res


def render_list(current=None):
    html_delimiter = main_renderer.get_html_file(cnv_path("assets/html/diary_delimiter.html"))
    html_delimiter_end = main_renderer.get_html_file(cnv_path("assets/html/diary_delimiter_end.html"))
    html_list_item = main_renderer.get_html_file(cnv_path("assets/html/diary_list_item.html"))
    html_list_item_cur = main_renderer.get_html_file(cnv_path("assets/html/diary_list_item_current.html"))
    prev_month = 0
    # data load
    dd = get_list()
    ht = ""
    for i in dd:
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
        ht += ht2
    ht += html_delimiter_end
    return ht


@app.route('/diary')
def diary_home():
    html = main_renderer.basepage(menu_mode=2)
    html = html.replace('{content}',
                        main_renderer.get_html_file(cnv_path('assets/html/diary_main.html')))
    html = html.replace('{extra_css}', 'diary')
    html = html.replace('{entry_list}', render_list())
    return html


@app.route('/diary/<entry>')
def diary_entry(entry):
    # load yaml
    d = get_entry(entry)
    cnt = d.content.replace("\n", "<br>")
    html = main_renderer.basepage(menu_mode=2)
    html = html.replace('{content}',
                        main_renderer.get_html_file(cnv_path('assets/html/diary_main.html')))
    html = html.replace('{extra_css}', 'diary')
    html = html.replace('{entry_list}', render_list())
    html = html.replace('{entry_content}',
                        main_renderer.get_html_file(cnv_path('assets/html/diary_content.html')))
    html = html.replace('{title}', d.title)
    html = html.replace('{written_at}', datetime.fromtimestamp(d.written_at).isoformat())
    html = html.replace('{entry_content}', cnt)
    return html
