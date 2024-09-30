import logging
import yaml
import conf

log = logging.getLogger(__name__)


def load_settings():
    global settings
    log.debug("loading site settings")
    with open("data/site_settings.yaml", "r", encoding="utf-8") as j:
        settings = yaml.load(j, yaml.FullLoader)


def site_settings():
    global settings
    if conf.dynamically_reload_site_settings:
        with open("data/site_settings.yaml", "r", encoding="utf-8") as j:
            settings = yaml.load(j, yaml.FullLoader)
    return settings


with open("data/site_settings.yaml", "r", encoding="utf-8") as j:
    settings = yaml.load(j, yaml.FullLoader)

log.info("site settings loaded")
