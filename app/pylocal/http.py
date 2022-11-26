import flask

from . import core

@core.app.route("/http/user_agent")
def user_agent():
    """Returns the user agent of the requester."""
    return flask.Response(flask.request.user_agent.string)