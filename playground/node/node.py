#!/usr/bin/env python
import sys
# import json

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

# GLOBAL VARS
playnode = Flask(__name__)
playnode_type = None
playnode_state = None


class PlayNodeType(object):
    EVALUATOR = "EVALUATOR"
    GRAND_CENTRAL = "GRAND_CENTRAL"


class PlayNode(object):
    RUNNING = "RUNNING"
    SLEEP = "SLEEP"
    SHUTDOWN = "SHUTDOWN"
    STATE = "STATE"
    OK = "OK"


@playnode.route('/')
def index():
    return render_template('index.html', title="home")


@playnode.route('/message/<msg>')
def message(msg):
    print "MESSAGE: ", msg
    if msg == PlayNode.SHUTDOWN:
        shutdown()

    response = jsonify(message=msg)
    return response


@playnode.route('/state')
def state():
    response = jsonify(state=playnode_state)
    return response


@playnode.route('/evaluate')
def evaluate():
    return render_template('evaluate.html', title="evaluate")


@playnode.route('/shutdown')
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
        playnode_state = PlayNode.RUNNING

        playnode.run(debug=True, host=host, port=port)

    else:
        print "Not enough arguments"
