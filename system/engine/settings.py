import logging
import yaml

log = logging.getLogger(__name__)
site_settings = None


def load_settings():
    global site_settings
    with open("data/site_settings.yaml", "r", encoding="utf-8") as j:
        site_settings = yaml.load(j, yaml.FullLoader)


load_settings()
log.info("site settings loaded")
