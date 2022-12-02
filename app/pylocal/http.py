import flask

from . import core

@core.app.route("/http/user_agent")
def user_agent():
    """Returns the user agent of the requester."""
    return flask.Response(flask.request.user_agent.string, content_type="text/plain")

@core.app.route("/http/ip_addr")
def ip_addr():
    return flask.Response(flask.request.remote_addr, content_type="text/plain")

@core.app.route("/http/dump_request")
def dump_request():
    str_response  = "method: {0}\n".format(flask.request.method)
    str_response += "headers: \n"
    for k, v in flask.request.headers.items():
        str_response += "    {0} := {1}\n".format(k, v)

    if flask.request.args:
        str_response += "request args: \n"
        for k, v in flask.request.args.items(multi=True):
            str_response += "    {0} := {1}\n".format(k, v)
    
    if flask.request.form:
        str_response = "request form data: \n"
        for k, v in flask.request.form.items(multi=True):
            str_response += "    {0} := {1}\n".format(k, v)
    
    if flask.request.files:
        str_response = "request files: \n"
        for k,v in flask.request.files.items(multi=True):
            str_response += "    {0} := {1}\n".format(k, v.filename)
    
    return flask.Response(str_response, content_type="text/plain")