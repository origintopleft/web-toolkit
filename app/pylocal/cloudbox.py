import json
import logging
import random
import regex as re
import string

import flask

from . import core

allocated_ids = {}

def generate_id():
    return "{0}{1}{2}-{3}".format(
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.ascii_uppercase),

        ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(3))
    )

@core.app.route("/cbx/allocate")
def allocate_id():
    global allocated_ids

    id = generate_id()
    remote_addr = flask.request.remote_addr

    allocated_ids[id] = {
        "addr": remote_addr
    }
    logging.info("allocated id {0} to {1}".format(id, remote_addr))

    if "token" in flask.request.args:
        allocated_ids[id]["token"] = flask.request.args["token"]

    result_data = {}
    result_data["id"] = id

    return flask.Response(json.dumps(result_data), content_type="application/json")

@core.app.route("/cbx/release/<id>")
def release_id(id):
    global allocated_ids

    rgx_id_validation = re.compile(r"^[A-Z]\d[A-Z]-[A-Z0-9]{3}$")
    if not rgx_id_validation.fullmatch(id):
        flask.abort(400)

    if not id in allocated_ids:
        logging.info("denying release of non-existent ID {0}")
        # return 503 instead of 404 to prevent enumerations
        flask.abort(503)

    if "token" in flask.request.args and flask.request.args["token"] == allocated_ids[id]["token"]:
        del allocated_ids[id]
        return flask.Response("ok", content_type="text/plain")
    elif flask.request.remote_addr == allocated_ids[id]["addr"]:
        del allocated_ids[id]
        return flask.Response("ok", content_type="text/plain")
    else:
        logging.info("denying release of {0} from mismatched addr {1}".format(id, flask.request.remote_addr))
        flask.abort(503)