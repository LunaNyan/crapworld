from system.engine.server import app
from flask import send_file, abort
from os.path import exists
from system.tool.etc import cnv_path
from system.engine.settings import site_settings


# static
@app.route('/static/<path>')
def static_send(path):
    fpath = cnv_path(f'theme/{site_settings()["theme"]}/static/{path}')
    if exists(fpath):
        return send_file(fpath)
    else:
        # Not Found를 리턴한다.
        return abort(404)


# css
@app.route('/css/<path>')
def css_send(path):
    fpath = cnv_path(f'theme/{site_settings()["theme"]}/css/{path}')
    if exists(fpath):
        return send_file(fpath)
    else:
        # Not Found를 리턴한다.
        return abort(404)


# data/img
@app.route('/img/<path>')
def static_send_img(path):
    fpath = cnv_path(f'data/img/{path}')
    if exists(fpath):
        return send_file(fpath)
    else:
        # Not Found를 리턴한다.
        return abort(404)
