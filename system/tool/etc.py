from system.engine.mgmt import ROOT_DIR
from platform import system
import math

# OS를 확인한다.
if system() == "Windows":
    dir_delimiter = "\\"
else:
    dir_delimiter = "/"


class Paginated:
    def __init__(self, current_page: int, total_pages: int, content: list):
        self.current_page = current_page
        self.total_pages = total_pages
        self.content = content


def paginate(data: list, page=1, amount_per_page=10):
    pages = math.ceil(len(data) / amount_per_page)
    if page > pages or page < 1:
        raise IndexError("Invalid Page Number")
    c = (page - 1) * amount_per_page
    liw = data[c:c+amount_per_page]
    return Paginated(page, pages, liw)


def cnv_path(path):
    t = path.replace("/", dir_delimiter)
    t = f"{ROOT_DIR}{dir_delimiter}{t}"
    return t


def check_trait(text, mode=False):
    """
    한글 문장을 검사하여 적절한 조사를 str로 리턴한다.
    text (str) : 조사 판단에 사용될 문장
    mode (bool) : 어떤 형태의 조사를 리턴할지 정한다. 기본값은 False이다.
      - True : 을 / 를
      - False : 이 / 가
    """
    if int((ord(text[-1:]) - 0xAC00) % 28) != 0:
        res = "을" if mode else "이"
    else:
        res = "를" if mode else "가"
    return res
