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

def generate_price():
    price = 0.0
    price = price + random.randint(7, 29)
    price = price + random.choice([0.99, 0.49])
    return price

def init_error():
    # stub
    return ''.join([random.choice(str_guestcheck_token_characters) for i in range(30)])

@core.app.route("/error/dummy")
def render_dummy_error():
    if "render" in flask.request.args and flask.request.args["render"] == "testcheck":
        order_items = []
        for _ in range(random.randint(1, 4)):
            order_items.append((generate_ticket_item(), generate_price()))
        return flask.render_template("guestcheck.j2", **{
            "page_title": "test",
            "order_items": order_items
        })
    else:
        return flask.Response(generate_ticket_item(), content_type="text/plain")