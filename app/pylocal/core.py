import logging
import os

import flask

app = flask.Flask(__name__, template_folder="../templates")

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

wordlist = None

def load_wordlists(dir):
    result = AttrDict()
    logging.info("loading wordlists from {0}".format(dir))
    for item in os.listdir(dir):
        absitem = "{0}/{1}".format(dir, item)
        if os.path.isdir(absitem):
            # recurse into subdirs
            result[item] = load_wordlists(absitem)
        elif item[-4:] == ".txt":
            itemres = []
            logging.info("loading wordlist {0}".format(absitem))
            with open(absitem) as itemfile:
                for line in itemfile:
                    itemres.append(line.strip())
            result[item] = itemres

    return result

wordlist = load_wordlists("/lib/wordlist")