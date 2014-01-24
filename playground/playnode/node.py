#!/usr/bin/env python
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

from playground.gp_tree.tree_evaluation import evaluate
from playground.gp_tree.tree_generator import TreeGenerator
from playground.functions import FunctionRegistry

# GLOBAL VARS
app = Flask(__name__)
playnode_type = None
functions = FunctionRegistry()
evaluate = evaluate


class PlayNodeType(object):
    EVALUATOR = "EVALUATOR"


class PlayNodeMessage(object):
    OK = "OK"
    SHUTDOWN = "SHUTDOWN"
    UNDEFINED = "UNDEFINED"
    ERROR = "ERROR"


@app.route('/')
def index():
    return render_template('index.html', title="home")


@app.route('/message', methods=["POST"])
def message():
    response_data = {}
    # incomming_data = json.loads(request.data)

    response_data["message"] = PlayNodeMessage.OK

    response = jsonify(response_data)
    return response


@app.route('/evaluate_trees', methods=["POST"])
def evaluate_trees():
    results = []
    response_data = {}

    # parse incomming data
    if request.data is not None:
        incomming_data = json.loads(request.data)
        config = incomming_data["config"]
        individuals = incomming_data["individuals"]

        # convert dict to trees
        tree_parser = TreeGenerator(config)
        for individual in list(individuals):
            tree = tree_parser.generate_tree_from_dict(individual)
            individuals.append(tree)
            individuals.remove(individual)

        evaluate(individuals, functions, config, results)

        # jsonify results
        response_data["results"] = []
        for individual in results:
            result = {
                "id": individual.tree_id,
                "score": individual.score,
            }
            response_data["results"].append(result)
        response = jsonify(response_data)
    else:
        response_data = {"message": PlayNodeMessage.ERROR}
        response = jsonify(response_data)

    return response


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
