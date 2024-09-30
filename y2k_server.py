# 우선 작업
from os.path import exists, isdir, join, basename
from tabnanny import check

from system.engine.log_manager import logger as log
import shutil

# data가 있는지 확인한 뒤, 없으면 skel에서 가져온다.
def copy_func(src, dst):
    if isdir(dst):
        dst = join(dst, basename(src))
    if exists(dst):
        # 이미 존재하는 파일은 덮어쓰지 않는다.
        pass
    shutil.copy2(src, dst)


if not exists("data/site_settings.yaml"):
    log.info("data를 초기화합니다.")
    shutil.copytree("system/skel", "data", dirs_exist_ok=True, copy_function=copy_func)

from system.engine import server, mgmt
from system.tool.upgrader import check_upgrade
from os import getcwd, listdir, cpu_count

mgmt.ROOT_DIR = getcwd()

# Check upgrade
log.info("Checking fmt_ver")
check_upgrade()

# 남은 모듈들을 마저 import한다.
from system import appinfo
from system.tool.etc import dir_delimiter
from system.engine.settings import site_settings
from sys import exit
import signal
import waitress
import conf

log.info(f"ver : {appinfo.VERSION}")

# 페이지 루트를 로드한다.
route_d = listdir(f"system{dir_delimiter}route")
log.info(f"{len(route_d)} files exists on route")

for i in sorted(route_d):
    if not i.endswith(".py"):
        continue
    log.info(f"loading route {i.replace('.py', '')}")
    exec(f"import system.route.{i.replace('.py', '')}")

log.info(f"Using theme {site_settings()['theme']}")


def signal_handler(signal, frame):
    exit(0)


signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    # 서버를 동작시킨다.
    log.info("server ON")
    cpu_threads = conf.cpu_threads if conf.cpu_threads != 0 else cpu_count()
    if conf.debug:
        server.app.run(host=conf.listen_host, port=conf.listen_port, debug=conf.debug)
    else:
        waitress.serve(server.app,
                       host=conf.listen_host,
                       port=conf.listen_port,
                       clear_untrusted_proxy_headers=True,
                       threads=cpu_threads)
