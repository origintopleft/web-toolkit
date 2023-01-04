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

def generate_taxes_and_fees():
    def get_rate():
        return round(random.uniform(1.76, 9.55), 2)

    def get_flat_fee():
        return round(random.uniform(0.50, 9.99), 2)

    result = {"tax": get_rate()}
    fee_types = [
        "77th Rule Of Acquisition",
        "Delivery",
        "Gratuitous Surcharge",
        "Ratioed on Twitter",
        "DTB",
        "Unreal Engine Royalties",
        "Mileage",
        "Receipt Fee"
    ]
    
    random.shuffle(fee_types)
    result["fees"] = [(fee_types.pop(), random.choice([(True, get_rate()), (False, get_flat_fee())])) for i in range(random.randint(1,3))]

    return result

def init_error(nonsense=False):
    if nonsense:
        errcode = "NSNSE" + ''.join([random.choice(str_guestcheck_token_characters) for i in range(25)])
    else:
        errcode = ''.join([random.choice(str_guestcheck_token_characters) for i in range(30)])
        while errcode[:5] == "NSNSE":
            # prevent generating nonsense codes on real errors
            errcode = ''.join([random.choice(str_guestcheck_token_characters) for i in range(5)]) + errcode[5:]
    return errcode

@core.app.route("/error/dummy")
def render_dummy_error():
    if "render" in flask.request.args and flask.request.args["render"] == "testcheck":
        curhost = flask.request.host.split(":")[0]
        host_components = curhost.split(".")
        curdomain = ".".join(host_components[-2:])
        
        # all this wind up for...
        if curdomain == "otl-hga.net": # production
            stylesheet = "https://cdn.otl-hga.net/toolkit/css/guestcheck.css"
        else: # dev
            stylesheet = flask.url_for("static", filename="css/guestcheck.css")

        order_items = []
        for _ in range(random.randint(1, 4)):
            order_items.append((generate_ticket_item(), generate_price()))
        return flask.render_template("guestcheck.j2", **{
            "page_title": "test",
            "order_items": order_items,
            "styles": [stylesheet],
            "errcode": init_error(nonsense=True),
            "taxesfees": generate_taxes_and_fees()
        })
    else:
        return flask.Response(generate_ticket_item(), content_type="text/plain")