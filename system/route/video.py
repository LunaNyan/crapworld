from system.engine.server import app
from system.engine.settings import site_settings
from system.tool.renderer import load_html_shard, render_mainpage, fill_args
from system.object.video import get_list, get_entry
from flask import abort


def render_list(current=None):
    html_delimiter = load_html_shard("diary/delimiter")
    html_delimiter_end = load_html_shard("diary/delimiter_end")
    html_list_item = load_html_shard("video/list_item")
    html_list_item_cur = load_html_shard("video/list_item_current")
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
    if not site_settings()["use_video"]:
        return abort(404)
    placeholder_info = load_html_shard('video/content_placeholder')
    placeholder_no_entry = load_html_shard('video/content_no_entry')
    diary_main = load_html_shard('diary/main')

    diary_list = get_list()

    arg = {"{entry_list}": render_list(diary_list),
           "{entry_content}": placeholder_no_entry if len(diary_list) == 0 else placeholder_info}
    diary_main = fill_args(diary_main, arg)

    return render_mainpage(diary_main, "video", "video")


@app.route('/video/<entry>')
def video_entry(entry):
    if not site_settings()["use_video"]:
        return abort(404)
    if ".." in entry:
        return abort(404)
    # load video entry
    try:
        display_name, youtube_path, description = get_entry(entry)
    except IndexError:
        return abort(404)

    diary_main = load_html_shard('diary/main')
    video_content = load_html_shard('video/entry')

    # ===== Content =====
    arg = {"{title}": display_name,
           "{youtube_path}": youtube_path,
           "{description}": description}
    video_content = fill_args(video_content, arg)

    # ===== Diary List =====
    arg = {"{entry_list}": render_list(entry),
           "{entry_content}": video_content}
    diary_main = fill_args(diary_main, arg)

    # ===== make main html =====
    return render_mainpage(diary_main, "video", "video")
