from system.engine.server import app
from system.engine.settings import site_settings
from system.tool import renderer
from system.tool.etc import cnv_path
from flask import abort
import yaml


class Photo:
    def __init__(self, path: str, description: str):
        self.path = path
        self.description = description


class PhotoCategory:
    def __init__(self, display_name: str, unlisted: bool, photos: list[Photo]):
        self.display_name = display_name
        self.unlisted = unlisted
        self.photos = photos


def get_list():
    # noinspection PyTypeChecker
    dl: dict[PhotoCategory] = {}
    # load photo.yaml
    with open(cnv_path("data/photo.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
    # parse
    for i in d:
        # photos
        photos = []
        for ii in i["photos"]:
            photos.append(Photo(ii["path"], ii["description"]))
        # category metadata
        dl[i["name"]] = PhotoCategory(i["display_name"], i["unlisted"], photos)
    return dl


def render_list(category_list: dict[PhotoCategory], current=None):
    html_delimiter = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_delimiter.html")
    html_delimiter_end = renderer.get_html_file(f"theme/{site_settings['theme']}/html/diary_delimiter_end.html")
    html_list_item = renderer.get_html_file(f"theme/{site_settings['theme']}/html/photo_list_item.html")
    html_list_item_cur = renderer.get_html_file(f"theme/{site_settings['theme']}/html/photo_list_item_current.html")
    ht = html_delimiter.replace("{group_title}", "카테고리")
    for name, cat in category_list.items():
        # 지금 보고있는 엔트리인가?
        if name == current:
            ht2 = html_list_item_cur.replace('{title}', cat.display_name)
        else:
            ht2 = html_list_item.replace('{title}', cat.display_name)
            ht2 = ht2.replace('{filename}', name)
        ht += ht2
    ht += html_delimiter_end
    return ht


@app.route('/photo')
def photo_main():
    if not site_settings["use_profile"]:
        return abort(404)
    placeholder_info = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/photo_content_placeholder.html')
    placeholder_no_entry = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/photo_content_no_entry.html')
    diary_main = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_main.html')

    category_list = get_list()

    arg = {"{entry_list}": render_list(category_list),
           "{entry_content}": placeholder_no_entry if len(category_list) == 0 else placeholder_info}
    diary_main = renderer.fill_args(diary_main, arg)

    return renderer.render_mainpage(diary_main, "photo", "photo")


@app.route('/photo/<category>')
def photo_category(category):
    if not site_settings["use_photo"]:
        return abort(404)
    if ".." in category:
        return abort(404)

    diary_main = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/diary_main.html')

    # ===== Content =====
    main_content = ""
    photo_content = renderer.get_html_file(f'theme/{site_settings["theme"]}/html/photo_entry.html')

    # load data
    d = get_list()
    try:
        for photos in d[category].photos:
            print(photos.path)
            print(photos.description)
            arg = {"{img_path}": photos.path, "{description}": photos.description}
            main_content += renderer.fill_args(photo_content, arg)
    except KeyError:
        return abort(404)

    # ===== Diary List =====
    profile_list = get_list()
    arg = {"{entry_list}": render_list(profile_list, category),
           "{entry_content}": main_content}
    diary_main = renderer.fill_args(diary_main, arg)

    # ===== make main html =====
    return renderer.render_mainpage(diary_main, "photo", "photo")
