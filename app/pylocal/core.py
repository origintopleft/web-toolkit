import logging
import os

import flask

app = flask.Flask(__name__, template_folder="../templates")
apiversion = 1

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

# ALL OTHER COMMANDS SHOULD USE @core.app.route
# the only reason these are an exception is because it's in core
@app.route("/core/apiversion")
def return_api_version():
    return flask.Response(str(apiversion), content_type="text/plain")

# static file handling
@app.route("/static/<path:filepath>")
def return_static_file():
    return flask.send_from_directory("static", filepath)