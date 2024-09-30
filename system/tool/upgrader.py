from system.engine.settings import site_settings
from system.engine.log_manager import logger as log
from system.appinfo import FMT_VER

upgrade_steps = {}


def check_upgrade():
    cur = site_settings()["fmt_ver"]
    if cur == FMT_VER:
        log.info("data format version is up to date")
    if cur < FMT_VER:
        # 포맷 업그레이드가 필요하다.
        log.info(f"current data format version is {cur}, which is older than current version {FMT_VER}")
