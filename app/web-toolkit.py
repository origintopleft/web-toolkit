#!/usr/bin/env python3

# preload step
import gevent.monkey

gevent.monkey.patch_all()

# std lib
import logging
import sys

# third party
import flask
from gevent.pywsgi import WSGIServer

# local
from pylocal import core, http, weather

logging.basicConfig(format="%(asctime)s [%(levelname)s][%(module)s] %(message)s", level=logging.INFO)
logging.info("web-toolkit preparing to spin up")

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

if __name__ == "__main__":
    #core.app.run("0.0.0.0", 1337)
    http_server = WSGIServer(('', 1337), core.app, log=logging.getLogger(name="gevent"))
    http_server.serve_forever()