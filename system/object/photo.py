from system.engine.settings import site_settings
from system.tool.etc import cnv_path
from PIL import Image
import uuid
import yaml


class Photo:
    def __init__(self, path: str, thumbnail_path: str, description: str):
        self.path = path
        self.thumbnail_path = thumbnail_path
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
            photos.append(Photo(ii["path"], thumbnail, ii["description"]))
        # category metadata
        dl[i["name"]] = PhotoCategory(i["display_name"], i["unlisted"], photos)
    return dl


def make_thumbnail(fpath, ysize):
    img = Image.open(cnv_path("data/" + fpath))
    hsize = int(img.size[0] * (ysize / img.size[1]))
    img = img.resize((hsize, ysize))
    u = str(uuid.uuid4()) + "." + fpath.split(".")[-1]
    print(u)
    img.save(cnv_path("cache/image_thumbnail/" + u))
    return u
