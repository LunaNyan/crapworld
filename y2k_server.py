from system.engine import server, mgmt
from os import getcwd, listdir
mgmt.ROOT_DIR = getcwd()

from system import appinfo
from system.engine.log_manager import logger as log
from system.tool.etc import dir_delimiter
from system.engine.settings import site_settings
import conf

log.info("y2k.erpin.club")
log.info(f"ver : {appinfo.VERSION}")

# 페이지 루트를 로드한다.
route_d = listdir(f"system{dir_delimiter}route")
log.info(f"{len(route_d)} files exists on route")

for i in sorted(route_d):
    if not i.endswith(".py"):
        continue
    log.info(f"loading route {i.replace('.py', '')}")
    exec(f"import system.route.{i.replace('.py', '')}")

log.info(f"Using theme {site_settings['theme']}")

if __name__ == '__main__':
    log.warning("y2k_server.py를 직접 실행하였습니다.")
    log.warning("서버를 prod로 실행할 때는 'python3 -m flask run'을 사용하십시오.")
    log.info("Starting Server")
    server.app.run(host=conf.listen_host, port=conf.listen_port, debug=conf.debug)


def create_site():
    return server.app
