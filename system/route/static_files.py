from system.engine.server import app
from system.engine.mgmt import ROOT_DIR
from flask import send_file, abort
from os.path import exists
from system.tool.dirpath_delimiter import dir_delimiter


@app.route('/static/<path>')
def static_send(path):
    if exists(f'{ROOT_DIR}{dir_delimiter}static{dir_delimiter}{path}'):
        return send_file(f"{ROOT_DIR}{dir_delimiter}static{dir_delimiter}{path}")
    else:
        # Not Found를 리턴한다.
        return abort(404)
