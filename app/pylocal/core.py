import logging
import os

import flask

app = flask.Flask(__name__, template_folder="../templates")

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self