from system.engine.settings import site_settings
from system.engine.log_manager import logger as log
from system.appinfo import FMT_VER
import conf
import sys

# ===== Upgrade =====


def do_upgrade_100_to_102():
    site_settings_append = """
# ===== r1p2-beta =====
# 사진첩 썸네일을 사용할지의 여부
photo_use_thumbnail: true
# 썸네일 최대 크기(세로)
photo_thumbnail_size: 300
"""
    log.info("automatically editing site_settings.yaml")

    fr = open("data/site_settings.yaml", "r", encoding="utf-8")
    f = fr.read() + "\n" + site_settings_append
    fr.close()
    f.replace("fmt_ver: 100", "fmt_ver: 102")

    fw = open("data/site_settings.yaml", "w", encoding="utf-8")
    fw.write(f)
    fw.close()

    log.info("upgrade fmt_ver 100 to 102 complete.")


upgrade_steps = {100: do_upgrade_100_to_102}

# ===================


def check_upgrade():
    cur = site_settings()["fmt_ver"]
    if cur == FMT_VER:
        log.info("data format version is up to date")
    if cur < FMT_VER:
        # 포맷 업그레이드가 필요하다.
        log.info(f"current data format version is {cur}, which is older than current version {FMT_VER}")
        for cver, stp in upgrade_steps.items():
            if cur < cver:
                log.info(f"running upgrade {stp.__name__}")
                stp()
        log.info("done")
        if not conf.dynamically_reload_site_settings:
            log.info("dynamically_reload_site_settings is off. you need to restart app manually.")
            sys.exit(0)
