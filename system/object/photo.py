from system.engine.settings import site_settings
from system.tool import renderer
from system.tool.ip_filter import is_admin
from system.tool.etc import cnv_path
from flask import request
from datetime import datetime
from PIL import Image
import uuid
import yaml
import os


class Photo:
    def __init__(self, name: str, path: str, thumbnail_path: str, description: str, uploaded_at: int):
        self.name = name
        self.path = path
        self.thumbnail_path = thumbnail_path
        self.description = description
        self.uploaded_at = uploaded_at


class PhotoCategory:
    def __init__(self, display_name: str, unlisted: bool, photos: list[Photo]):
        self.display_name = display_name
        self.unlisted = unlisted
        self.photos = photos


def add_category(name, display_name, unlisted=False):
    # load photo.yaml
    with open(cnv_path("data/photo.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)

    d.append({"name": name, "display_name": display_name, "unlisted": unlisted, "photos": []})

    # save
    with open("data/photo.yaml", "w", encoding="utf-8") as j:
        yaml.dump(d, j, allow_unicode=True)


def upload_pic(request, filename):
    file = request.files['file']
    file.save("cache/profile_pic")

    im = Image.open("cache/profile_pic")
    im.save(f'data/img/{filename}.png')

    os.remove("cache/profile_pic")


def add_entry(category, name, description):
    # load photo.yaml
    with open(cnv_path("data/photo.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)

    cat = None
    catn = 0
    for n, i in enumerate(d):
        if i["name"] == category:
            cat = i
            catn = n
    if cat is None:
        raise KeyError

    cat["photos"].append({
        "description": description,
        "name": name,
        "path": f"/img/{name}.png",
        "uploaded_at": datetime.now().timestamp()
    })

    d[catn]["photos"] = cat["photos"]

    # save
    with open("data/photo.yaml", "w", encoding="utf-8") as j:
        yaml.dump(d, j, allow_unicode=True)


def get_entry(category, img_name):
    # load photo.yaml
    with open(cnv_path("data/photo.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
    # load cache
    with open(cnv_path("cache/image_thumbnail/entry.yaml"), "r", encoding="utf-8") as f:
        dtn = yaml.load(f, yaml.FullLoader)

    # Find data
    opn = None
    for i in d:
        if i["name"] == category:
            opn = i
    if opn is None:  # category not found handler
        raise KeyError

    opn2 = None
    for i in opn["photos"]:
        if i["name"] == img_name:
            opn2 = i
    if opn2 is None:
        raise KeyError

    try:
        # 썸네일을 찾는다.
        thumbnail = dtn[opn2['path'].replace("/img/", "")]
    except KeyError:
        # 썸네일이 없다. 만든다.
        thumbnail = make_thumbnail(opn2['path'], site_settings()["photo_thumbnail_size"])
        dtn[opn2['path'].replace("/img/", "")] = thumbnail
        # cache save
        with open(cnv_path("cache/image_thumbnail/entry.yaml"), "w", encoding="utf-8") as f:
            yaml.dump(dtn, f)

    return Photo(opn2["name"], opn2["path"], thumbnail, opn2["description"], opn2["uploaded_at"])


def get_list():
    # noinspection PyTypeChecker
    dl: dict[PhotoCategory] = {}
    # load photo.yaml
    with open(cnv_path("data/photo.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
    # load cache
    with open(cnv_path("cache/image_thumbnail/entry.yaml"), "r", encoding="utf-8") as f:
        dtn = yaml.load(f, yaml.FullLoader)
    # parse
    for i in d:
        # photos
        photos = []
        for ii in i["photos"]:
            # cache
            if site_settings()['photo_use_thumbnail']:
                try:
                    # 썸네일을 찾는다.
                    thumbnail = dtn[ii['path'].replace("/img/", "")]
                except KeyError:
                    # 썸네일이 없다. 만든다.
                    thumbnail = make_thumbnail(ii['path'], site_settings()["photo_thumbnail_size"])
                    dtn[ii['path'].replace("/img/", "")] = thumbnail
                    # cache save
                    with open(cnv_path("cache/image_thumbnail/entry.yaml"), "w", encoding="utf-8") as f:
                        yaml.dump(dtn, f)
            else:
                thumbnail = ii["path"]
            photos.append(Photo(ii["name"], ii["path"], thumbnail, ii["description"], ii["uploaded_at"]))
        # category metadata
        dl[i["name"]] = PhotoCategory(i["display_name"], i["unlisted"], photos)
    return dl


def make_thumbnail(fpath, ysize):
    img = Image.open(cnv_path("data/" + fpath))
    hsize = int(img.size[0] * (ysize / img.size[1]))
    img = img.resize((hsize, ysize))
    u = str(uuid.uuid4()) + "." + fpath.split(".")[-1]
    img.save(cnv_path("cache/image_thumbnail/" + u))
    return u


def render_list(category_list: dict[PhotoCategory], current=None):
    html_delimiter = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/diary_delimiter.html")
    html_delimiter_end = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/diary_delimiter_end.html")
    html_list_item = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/photo_list_item.html")
    html_list_item_cur = renderer.get_html_file(f"theme/{site_settings()['theme']}/html/photo_list_item_current.html")
    ht = html_delimiter.replace("{group_title}", "카테고리")
    for name, cat in category_list.items():
        # 지금 보고있는 엔트리인가?
        if name == current:
            ht2 = html_list_item_cur.replace('{title}', cat.display_name)
        else:
            ht2 = html_list_item.replace('{title}', cat.display_name)
            ht2 = ht2.replace('{filename}', name)
        ht += ht2
    # admin인 경우 새로 만들 수 있음
    if is_admin(request)[0]:
        if current == "add_item":
            ht2 = html_list_item_cur.replace('{title}', "<b>새로 만들기</b>")
            ht2 = ht2.replace('{filename}', 'add_category')
        else:
            ht2 = html_list_item.replace('{title}', "<b>새로 만들기</b>")
            ht2 = ht2.replace('{filename}', 'add_category')
        ht += ht2
    ht += html_delimiter_end
    return ht
