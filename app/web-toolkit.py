#!/usr/bin/env python3

import sys

import flask

from pylocal import *

@core.app.route("/")
def index():
    return "<h1>It works!</h1>"

# compatibility with some browser data requests
@core.app.route("/favicon.ico")
def favicon():
    return flask.redirect("https://cdn.otl-hga.net/toolkit-branding/favicon.ico")

@core.app.route("/site.webmanifest")
def sitemanifest():
    return flask.redirect("https://cdn.otl-hga.net/toolkit-branding/site.webmanifest")

# apache2
application = core.app

if __name__ == "__main__":
    core.app.run("0.0.0.0", 1337)