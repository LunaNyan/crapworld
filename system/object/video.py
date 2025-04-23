from system.tool.etc import cnv_path
import yaml


class VideoEntry:
    def __init__(self, path: str, name: str, youtube_path: str, description: str):
        self.path = path
        self.name = name
        self.youtube_path = youtube_path
        self.description = description


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
            v.append(VideoEntry(ii["id"], ii["name"], ii["youtube_path"], ii["description"]))
        dl.append(VideoCategory(i["category_name"], v))
    return dl


def get_entry(video_id):
    with open(cnv_path(f"data/videos.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
    for i in d:
        for ii in i["videos"]:
            if ii["id"] == video_id:
                return ii["name"], ii["youtube_path"], ii["description"]
    # 여기로 진입했다 == 못찾았다
    raise IndexError


def create_category(category_name: str):
    # read
    with open(cnv_path(f"data/videos.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
    # write
    with open(cnv_path(f"data/videos.yaml"), "w", encoding="utf-8") as f:
        d = d + {"category_name": category_name}
        yaml.dump(d, f)


def create_video(category_name: str, entry_id: str, video_name: str, video_id: str, description: str):
    # read
    with open(cnv_path(f"data/videos.yaml"), "r", encoding="utf-8") as f:
        d = yaml.load(f, yaml.FullLoader)
    # find category
    target = None
    cnt = 0
    for i in d:
        if i["category_name"] == category_name:
            target = i
        cnt += 1
    if not target:
        # 여기까지 도달했는데 target이 None임 == 못찾음
        raise IndexError
    # target category를 임시로 제거
    d.pop(cnt)
    # add entry
    target["videos"].append(
        {"id": entry_id,
         "name": video_name,
         "youtube_path": video_id,
         "description": description}
    )
    d.insert(cnt, target)
    # write
    with open(cnv_path(f"data/videos.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(d, f)
