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
# the only reason this is an exception is because it's in core
@app.route("/core/apiversion")
def return_api_version():
    return flask.Response(str(apiversion), content_type="text/plain")