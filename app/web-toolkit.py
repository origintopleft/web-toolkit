#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    print("please don't run me directly, i'm a flask app")
    sys.exit(0)

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>It works!</h1>"