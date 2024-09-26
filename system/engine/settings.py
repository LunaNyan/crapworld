import logging
import yaml


log = logging.getLogger(__name__)


def get_settings():
    # 설정 읽어들이기
    with open("data/site_settings.yaml", "r", encoding="utf-8") as j:
        site_settings = yaml.load(j, yaml.FullLoader)
    return site_settings


site_settings = get_settings()
log.info("site settings loaded")
