from system.engine.server import app
from system.tool import main_renderer
from system.tool.dirpath_delimiter import cnv_path
import json


def render_list(current=None):
    html_delimiter = main_renderer.get_html_file(cnv_path("assets/html/diary_delimiter.html"))
    html_list_item = main_renderer.get_html_file(cnv_path("assets/html/diary_list_item.html"))
    html_list_item_cur = main_renderer.get_html_file(cnv_path("assets/html/diary_list_item_current.html"))
    # list.json open
    with open(cnv_path("data/diary/list.json"), "r", encoding="utf-8") as f:
        d = json.loads(f.read())
    h = ""
    for i in d:
        ht = html_delimiter.replace("{group_title}", i['title'])
        for ii in i['items']:
            if ii['filename'] == current:
                ht2 = html_list_item_cur.replace('{title}', ii['title'])
            else:
                ht2 = html_list_item.replace('{title}', ii['title'])
                ht2 = ht2.replace('{filename}', '/diary/' + ii['filename'])
            ht += ht2
        h += ht
    return h


@app.route('/diary')
def diary_home():
    html = main_renderer.basepage(menu_mode=2)
    html = html.replace('{content}',
                        main_renderer.get_html_file(cnv_path('assets/html/diary_main.html')))
    html = html.replace('{extra_css}', 'diary')
    html = html.replace('{entry_list}', render_list())
    return html
