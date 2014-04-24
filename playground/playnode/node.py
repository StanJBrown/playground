#!/usr/bin/env python
import os
import sys
import json
import signal
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

from playground.gp.tree.tree_evaluation import evaluate
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry

# GLOBAL VARS
app = Flask(__name__)
functions = GPFunctionRegistry()
evaluate = evaluate


class PlayNodeType(object):
    EVALUATOR = "EVALUATOR"
    MONITOR = "MONITOR"


class PlayNodeStatus(object):
    OK = "OK"
    BUSY = "BUSY"
    SHUTDOWN = "SHUTDOWN"
    UNDEFINED = "UNDEFINED"
    ERROR = "ERROR"


def usage():
    print "Error! Insufficient command line arguments!"
    print "usage:"
    print "\tnode [localhost] [port] [type]"


def init(host, port):
    # check if process is already running
    pid = str(os.getpid())
    pid_fp = "/tmp/playground-{0}-{1}.pid".format(host, port)
    if os.path.isfile(pid_fp):
        print("{0} already exists, exiting".format(pid_fp))
        sys.exit()
    else:
        pid_content = json.dumps({"pid": pid, "status": PlayNodeStatus.OK})
        pidfile = file(pid_fp, "w")
        pidfile.write(pid_content)
        pidfile.close()

    # register signal handler
    signal.signal(signal.SIGTERM, terminate_handler)
    signal.signal(signal.SIGINT, terminate_handler)


def change_status(new_status):
    pid_fp = "/tmp/playground-{0}-{1}.pid".format(host, port)
    pidfile = file(pid_fp, "r+")

    # read dict
    pid_dict = json.loads(pidfile.read())
    pidfile.seek(0)
    pidfile.truncate()

    # modify dict and write new status
    pid_dict["status"] = new_status
    pidfile.write(pid_dict)
    pidfile.close()


def terminate_handler(signal, frame):
    print "Terminating down server ... "
    pid_fp = "/tmp/playground-{0}-{1}.pid".format(host, port)
    os.unlink(pid_fp)
    sys.exit(0)


@app.route("/")
def index():
    return render_template("index.html", title="home")


@app.route("/status")
def status():
    pid_fp = "/tmp/playground-{0}-{1}.pid".format(host, port)
    pidfile = file(pid_fp, "r+")
    pid_dict = json.loads(pidfile.read())
    pidfile.close()

    # read dict
    return jsonify({"status": pid_dict["status"]})


@app.route("/evaluate", methods=["POST"])
def evaluate_trees():
    results = []
    response = {}

    # parse incomming data
    if request.data is not None:
        incomming = json.loads(request.data)
        config = incomming["config"]
        individuals = incomming["individuals"]

        # convert dict to trees
        tree_parser = TreeGenerator(config)
        for individual in list(individuals):
            tree = tree_parser.generate_tree_from_dict(individual)
            individuals.append(tree)
            individuals.remove(individual)

        evaluate(individuals, functions, config, results)

        # jsonify results
        response["results"] = []
        for individual in results:
            result = {
                "id": individual.tree_id,
                "score": individual.score,
            }
            response["results"].append(result)

    else:
        response = {"status": PlayNodeStatus.ERROR}

    return jsonify(response)


@app.route("/monitor")
def monitor():
    return render_template("monitor.html", title="monitor")


@app.route("/monitor", methods=["POST"])
def monitor_add_data():
    response = {}
    if request.data is not None:
        incomming = json.loads(request.data)
        response["status"] = "OK"

    else:
        response["status"] = "ERROR"

    return jsonify(response)


@app.route("/monitor_data")
def monitor_get_data():
    pass


if __name__ == "__main__":
    if len(sys.argv) == 4:
        # parse command line arguments
        host = sys.argv[1]
        port = int(sys.argv[2])
        playnode_type = sys.argv[3]

        # run app
        init(host, port)
        app.run(debug=True, use_reloader=False, host=host, port=port)
    else:
        usage()
