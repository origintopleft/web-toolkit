#!/usr/bin/env python3

import sys

import flask

from pylocal import *

@core.app.route("/")
def index():
    return "<h1>It works!</h1>"

# apache2
application = core.app

if __name__ == "__main__":
    core.app.run("0.0.0.0", 1337)