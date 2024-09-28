from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer
from system.tool.etc import cnv_path
from flask import abort
import yaml


class VideoEntry:
    def __init__(self, path: str, name: str, youtube_path: str):
        self.path = path
        self.name = name
        self.youtube_path = youtube_path


class VideoCategory:
    def __init__(self, name: str, videos: list[VideoEntry]):
        self.name = name
        self.videos = videos


def get_list():
    dl = []
    with open(cnv_path(f"data/videos.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
    for i in d:
        # videos
        v = []
        for ii in i["videos"]:
            v.append(VideoEntry(ii["id"], ii["name"], ii["youtube_path"]))
        dl.append(VideoCategory(i["category_name"], v))
    return dl


def get_entry(video_id):
    with open(cnv_path(f"data/videos.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
    for i in d:
        for ii in i["videos"]:
            if ii["id"] == video_id:
                return ii["name"], ii["youtube_path"]
    # 여기로 진입했다 == 못찾았다
    raise IndexError


def render_list(current=None):
    html_delimiter = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_delimiter.html")
    html_delimiter_end = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_delimiter_end.html")
    html_list_item = renderer.get_html_file(f"theme/{site_settings['theme']}/html/video_list_item.html")
    html_list_item_cur = renderer.get_html_file(f"theme/{site_settings['theme']}/html/video_list_item_current.html")
    ht = ""
    video_category = get_list()
    for n, i in enumerate(video_category):
        # delimiter end
        if n != 0:
            ht += html_delimiter_end
        # delimiter start
        ht += html_delimiter.replace("{group_title}", i.name)
        # videos
        for ii in i.videos:
            # 지금 보고있는 엔트리인가?
            if ii.path == current:
                ht2 = html_list_item_cur.replace('{title}', ii.name)
            else:
                ht2 = html_list_item.replace('{title}', ii.name)
                ht2 = ht2.replace('{videoid}', ii.path)
            ht += ht2
    ht += html_delimiter_end
    return ht


@app.route('/video')
def video_home():
    if not site_settings["use_video"]:
        return abort(404)
    placeholder_info = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/video_content_placeholder.html')
    placeholder_no_entry = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/video_content_no_entry.html')
    diary_main = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_main.html')

    diary_list = get_list()

    arg = {"{entry_list}": render_list(diary_list),
           "{entry_content}": placeholder_no_entry if len(diary_list) == 0 else placeholder_info}
    diary_main = renderer.fill_args(diary_main, arg)

    return renderer.render_mainpage(diary_main, "video", "video")


@app.route('/video/<entry>')
def video_entry(entry):
    if not site_settings["use_video"]:
        return abort(404)
    if ".." in entry:
        return abort(404)
    # load video entry
    try:
        display_name, youtube_path = get_entry(entry)
    except IndexError:
        return abort(404)

    diary_main = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_main.html')
    video_content = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/video_entry.html')

    # ===== Content =====
    arg = {"{title}": display_name,
           "{youtube_path}": youtube_path}
    video_content = renderer.fill_args(video_content, arg)

    # ===== Diary List =====
    arg = {"{entry_list}": render_list(entry),
           "{entry_content}": video_content}
    diary_main = renderer.fill_args(diary_main, arg)

    # ===== make main html =====
    return renderer.render_mainpage(diary_main, "video", "video")
