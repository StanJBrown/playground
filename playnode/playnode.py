#!/usr/bin/env python
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

import playground.gp_tree.tree_evaluation as tree_evaluation
from playground.gp_tree.tree_generator import TreeGenerator
from playground.functions import FunctionRegistry

# GLOBAL VARS
app = Flask(__name__)
playnode_type = None
evaluate = tree_evaluation.evaluate
functions = FunctionRegistry()


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
    response_data = {}
    incomming_data = json.loads(request.data)

    if incomming_data["message"] == PlayNodeMessage.SHUTDOWN:
        response_data["message"] = PlayNodeMessage.OK
        shutdown()
    else:
        response_data["message"] = PlayNodeMessage.UNDEFINED

    response = jsonify(response_data)
    return response


@app.route('/evaluate', methods=["POST"])
def evaluate():
    results = []
    response_data = {"results": []}

    # parse incomming data
    incomming_data = json.loads(request.data)
    config = incomming_data["config"]
    individuals = incomming_data["individuals"]

    # convert dict to trees
    tree_parser = TreeGenerator(config)
    for individual in list(individuals):
        tree = tree_parser.generate_tree_from_dict(individual)
        individuals.append(tree)
        individuals.remove(individual)

    # evaluate individuals and create response
    tree_evaluation.evaluate(individuals, functions, config, results)
    for individual in results:
        result = {"id": individual.tree_id, "score": individual.score}
        response_data["results"].append(result)

    response = jsonify(response_data)
    return response


@app.route('/shutdown')
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_func()
    return render_template('shutdown.html', title="shutdown")


if __name__ == '__main__':
    if len(sys.argv) == 4:
        # parse command line arguments
        host = sys.argv[1]
        port = int(sys.argv[2])
        playnode_type = sys.argv[3]

        # run app
        app.run(debug=True, host=host, port=port)

    else:
        print "Not enough arguments"
