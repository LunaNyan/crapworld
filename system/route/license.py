from system.engine.server import app
from flask import make_response

f = open("LICENSE", "r")
LICENSE_TEXT = f.read()
f.close()


# static
@app.route('/license')
def license_send():
    response = make_response(LICENSE_TEXT, 200)
    response.mimetype = "text/plain"
    return response
