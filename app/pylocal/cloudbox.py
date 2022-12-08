import json
import random
import string

import flask

from . import core

allocated_ids = {}

@core.app.route("/cbx/allocate")
def allocate_id():
    global allocated_ids

    id = "{0}{1}{2}-{3}".format(
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.ascii_uppercase),

        ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(3))
    )

    allocated_ids[id] = {
        "addr": flask.request.remote_addr
    }

    result_data = {}
    result_data["id"] = id

    return flask.Response(json.dumps(result_data), content_type="application/json")

@core.app.route("/cbx/release/<id>")
def release_id(id):
    global allocated_ids

    if flask.request.remote_addr == allocated_ids[id]["addr"]:
        del allocated_ids[id]
        return flask.Response("ok", content_type="text/plain")
    else:
        flask.abort(503)