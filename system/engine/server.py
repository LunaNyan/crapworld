from flask import Flask
import conf

app = Flask(__name__)
if conf.debug:
    app.debug = True
else:
    app.debug = False
