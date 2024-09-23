from conf import conf
from system.engine.server import app
import logging

log = logging.getLogger(__name__)


@app.route('/')
def hello_world():
    ff = open('html/index.html', 'r', encoding='utf-8')
    index_html = ff.read()
    ff.close()
    # 파라미터 수정 개시
    index_html = index_html.replace('{site_title}', conf.site_title)
    return index_html
