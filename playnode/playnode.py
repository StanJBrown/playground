#!/usr/bin/env python
import sys
import json

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

# GLOBAL VARS
app = Flask(__name__)
playnode_type = None


class PlayNodeType(object):
    EVALUATOR = "EVALUATOR"
    GRAND_CENTRAL = "GRAND_CENTRAL"


class PlayNodeMessage(object):
    STATE = "STATE"
    OK = "OK"
    SHUTDOWN = "SHUTDOWN"
    SLEEP = "SLEEP"
    UNDEFINED = "UNDEFINED"


@app.route('/')
def index():
    return render_template('index.html', title="home")


@app.route('/message', methods=["POST"])
def message():
    raw_data = request.data
    incomming_data = json.loads(raw_data)
    response_data = {}

    if incomming_data["message"] == PlayNodeMessage.SHUTDOWN:
        response_data["message"] = PlayNodeMessage.OK
        shutdown()
    else:
        response_data["message"] = PlayNodeMessage.UNDEFINED

    response = jsonify(response_data)
    return response


@app.route('/evaluate')
def evaluate():
    return render_template('evaluate.html', title="evaluate")


@app.route('/shutdown')
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_func()
    return render_template('shutdown.html', title="shutdown")


if __name__ == '__main__':
    if len(sys.argv) == 4:
        host = sys.argv[1]
        port = int(sys.argv[2])
        playnode_type = sys.argv[3]

        app.run(debug=True, host=host, port=port)

    else:
        print "Not enough arguments"
