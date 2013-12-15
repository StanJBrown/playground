#!/usr/bin/env python
import os
import sys
import json
import math
from multiprocessing import cpu_count
from multiprocessing import Manager
from multiprocessing import Process
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

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
manager = Manager()


class PlayNodeType(object):
    EVALUATOR = "EVALUATOR"
    GRAND_CENTRAL = "GRAND_CENTRAL"


class PlayNodeMessage(object):
    OK = "OK"
    SHUTDOWN = "SHUTDOWN"
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


@app.route('/evaluate_trees', methods=["POST"])
def evaluate_trees():
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

    # start proceses
    processes = []
    results = manager.list()
    nproc = cpu_count() * 2
    chunksize = int(math.ceil(len(individuals) / float(nproc)))
    for i in range(nproc):
        chunk = individuals[chunksize * i:chunksize * (i + 1)]
        args = (chunk, functions, config, results)
        p = Process(target=evaluate, args=args)
        processes.append(p)
        p.start()

    # wait till processes finish
    for p in processes:
        p.join()
    del processes[:]

    # jsonify results
    for individual in results:
        result = {"id": individual.tree_id, "score": individual.score}
        response_data["results"].append(result)
    response = jsonify(response_data)

    return response


@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    response_data = {"message": PlayNodeMessage.OK}
    return jsonify(response_data)


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
