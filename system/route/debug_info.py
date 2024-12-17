from system.engine.server import app
from system.engine.log_manager import logger as log
from system.engine.mgmt import BOOT_AT
from system.engine.settings import site_settings
from system.tool import renderer
from system.appinfo import VERSION
from datetime import datetime
import flask
import platform
import conf
import git
import locale

try:
    repo = git.Repo(search_parent_directories=True)
    git_sha = repo.head.object.hexsha[-10:]
except git.exc.InvalidGitRepositoryError:
    if conf.debug:
        log.warn("Git Repository is invalid. Git SHA is unavailable on Debug Info")
    git_sha = "알 수 없음 (InvalidGitRepositoryError)"
except git.exc.NoSuchPathError:
    if conf.debug:
        log.warn("Git Path is invalid. Git SHA is unavailable on Debug Info")
    git_sha = "알 수 없음 (NoSuchPathError)"


@app.route('/debug')
def debug_info():
    if not conf.debug:
        return flask.abort(404)
    home_html = renderer.get_html_file(f'theme/{site_settings()["theme"]}/html/debug_info.html')
    home_content = f"""
    <b>conf.py의 debug가 True입니다.</b><br>
    프로덕션으로 구동할 경우 반드시 False로 변경해 주세요.<br><br>
    <b>Uptime</b> : {datetime.now() - BOOT_AT}<br>
    <b>Version</b> : {VERSION}<br>
    <b>Branch</b> : {repo.active_branch}<br>
    <b>Git SHA</b> : {git_sha}<br><br>
    <b>OS</b> : {platform.system()} {platform.release()} ({platform.machine()})<br>
    <b>Locale</b> : {locale.getlocale(locale.LC_CTYPE)}<br>
    <b>Python</b> : {platform.python_implementation()} {platform.python_version()} ({platform.python_revision()})<br>
    <b>Flask</b> : {flask.__version__}<br><br>
    <b>theme</b> : {site_settings()["theme"]}
    """

    arg = {
        "{home_content}": home_content,
        "{bio}": ""
    }
    home_html = renderer.fill_args(home_html, arg)

    return renderer.render_mainpage(home_html, "debug", "debug_info",
                                    enable_dropdown=False)
