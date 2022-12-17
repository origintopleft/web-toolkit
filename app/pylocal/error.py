import json
import random
import string
import subprocess

import flask

from . import core

str_guestcheck_token_characters = string.ascii_uppercase + string.digits

def generate_ticket_item():
    rantout = subprocess.run(["rant", "/app/rant/order.rant"], capture_output=True)
    result = rantout.stdout.decode("utf8")
    result = result.rstrip()

    return result

def init_error():
    # stub
    return ''.join([random.choice(str_guestcheck_token_characters) for i in range(30)])

@core.app.route("/error/dummy")
def render_dummy_error():
    if "render" in flask.request.args and flask.request.args["render"] == "testcheck":
        return flask.render_template("guestcheck.j2", **{
            "page_title": "test",
            "order_items": [generate_ticket_item() for int in range(random.randint(1, 4))]
        })
    else:
        return flask.Response(generate_ticket_item(), content_type="text/plain")