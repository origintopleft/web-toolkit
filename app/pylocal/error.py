import json
import random
import string

import flask

from . import core

str_guestcheck_token_characters = string.ascii_uppercase + string.digits

def generate_ticket_item():
    return "{{ adjectives.food | random }} {{ nouns.food | random }}"

def init_error():
    # stub
    return ''.join([random.choice(str_guestcheck_token_characters) for i in range(30)])

@core.app.route("/error/dummy")
def render_dummy_error():
    return flask.render_template_string(generate_ticket_item(), **core.wordlist)