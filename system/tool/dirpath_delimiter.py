from platform import system
from system.engine.mgmt import ROOT_DIR
import logging as log

# OS를 확인한다.
if system() == "Windows":
    log.warning("Windows에서 구동 중입니다. 추후 지원되지 않을 가능성이 높습니다.")
    dir_delimiter = "\\"
else:
    dir_delimiter = "/"


def cnv_path(path):
    t = path.replace("/", dir_delimiter)
    t = f"{ROOT_DIR}{dir_delimiter}{t}"
    return t
