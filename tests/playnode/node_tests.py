#!/usr/bin/env python2
import os
import sys
import json
import time
import signal
import random
import httplib
import unittest
import subprocess
from subprocess import Popen
from subprocess import check_call
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from playground.playnode.node import PlayNodeType
from playground.playnode.node import PlayNodeStatus

from playground.gp.tree.generator import TreeGenerator
from playground.gp.tree.parser import TreeParser

# SETTINGS
n_script = "playground/playnode/node.py"


def check_call_modify(command, output_file):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in p.stdout:
        output_file.write(line)
    p.wait()
    if p.returncode:
        raise subprocess.CalledProcessError(p.returncode, command)
    return p.returncode


class NodeTests(unittest.TestCase):
    def setUp(self):
        self.processes = 0

        host = "localhost"
        ntype = PlayNodeType.EVALUATOR
        nodes = [
            ["./" + n_script, host, "8080", ntype],
            ["./" + n_script, host, "8081", ntype],
            ["./" + n_script, host, "8082", ntype]
        ]

        # start the playground nodes
        self.node_1 = Popen(nodes[0], preexec_fn=os.setsid)
        # self.node_2 = Popen(nodes[1], preexec_fn=os.setsid)
        # self.node_3 = Popen(nodes[2], preexec_fn=os.setsid)

        # sleep for 2 seconds while the servers are starting
        time.sleep(1)

    def tearDown(self):
        # shutdown all the playground nodes
        os.kill(self.node_1.pid, signal.SIGTERM)
        # os.kill(self.node_2.pid, signal.SIGTERM)
        # os.kill(self.node_3.pid, signal.SIGTERM)

    def transmit(self, host, port, req_type, path, data=None):
        request = "/".join(path.split("/"))

        # transmit
        conn = httplib.HTTPConnection(host, port)
        if data:
            conn.request(req_type, request, data)
        else:
            conn.request(req_type, request)

        # response
        response = conn.getresponse()
        data = response.read()
        conn.close()

        return data

    def check_nodes(self):
        check_call(["isrunning", "python"])
        print "\n"

        output = open("out", "w")
        check_call_modify(["isrunning", "python"], output)
        output.close()

        output = open("out", "r")
        processes = len(output.read().split("\n"))
        output.close()
        os.remove("out")

        return processes

    def check_state(self, host, port, state):
        data = self.transmit(host, port, "GET", "state")
        data = json.dumps(data)

        if (data["state"] == state):
            return True
        else:
            return False

    def test_status(self):
        response = self.transmit("localhost", 8080, "GET", "status")
        response = json.loads(response)
        self.assertEquals(response["status"], PlayNodeStatus.OK)

    def test_evaluate(self):
        random.seed(10)
        # solution = {
        #     "results":
        #     [
        #         {"score": 15726642.002161335},
        #         {"score": 359.25843589015597},
        #         {"score": 92155571.22132382},
        #         {"score": 26186.46142920347},
        #         {"score": 15649304.847552022},
        #         {"score": 188.86069156360125},
        #         {"score": 23439.33097274221},
        #     ]
        # }

        # setup
        config = {
            "max_population" : 10,
            "max_generation" : 5,

            "tree_generation" : {
                "method" : "GROW_METHOD",
                "initial_max_depth" : 3
            },

            "evaluator": {
                "use_cache" : True
            },

            "selection" : {
                "method" : "TOURNAMENT_SELECTION",
                "tournament_size": 5
            },

            "crossover" : {
                "method" : "POINT_CROSSOVER",
                "probability" : 0.8
            },

            "mutation" : {
                "methods": [
                    "POINT_MUTATION",
                    "HOIST_MUTATION",
                    "SUBTREE_MUTATION",
                    "SHRINK_MUTATION",
                    "EXPAND_MUTATION"
                ],
                "probability" : 0.9
            },

            "function_nodes" : [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1}
            ],

            "terminal_nodes" : [
                {"type": "CONSTANT", "value": 1.0},
                {"type": "CONSTANT", "value": 2.0},
                {"type": "CONSTANT", "value": 2.0},
                {"type": "CONSTANT", "value": 3.0},
                {"type": "CONSTANT", "value": 4.0},
                {"type": "CONSTANT", "value": 5.0},
                {"type": "CONSTANT", "value": 6.0},
                {"type": "CONSTANT", "value": 7.0},
                {"type": "CONSTANT", "value": 8.0},
                {"type": "CONSTANT", "value": 9.0},
                {"type": "CONSTANT", "value": 10.0}
            ],


            "data_file" : "tests/data/sine.dat",

            "input_variables" : [{"type": "INPUT", "name": "x"}],
            "response_variables" : [{"name": "y"}]
        }
        parser = TreeParser()
        population = TreeGenerator(config).init()

        # create a dictionary of trees
        data = {"config": config, "individuals": []}
        for individual in population.individuals:
            tree_json = parser.tree_to_dict(individual, individual.root)
            data["individuals"].append(tree_json)

        # make sure population size is equals to number of trees
        population_size = len(population.individuals)
        individuals = len(data["individuals"])
        self.assertEquals(population_size, individuals)

        # evaluating individuals
        data = json.dumps(data)
        host = "localhost"
        port = 8080
        req_type = "POST"
        path = "evaluate"
        response = self.transmit(host, port, req_type, path, data)
        response = json.loads(response)
        print response

        # assert tests
        # for score_solution in list(solution["results"]):
        #     for score_response in list(response["results"]):
        #         score_1 = round(score_response["score"], 5)
        #         score_2 = round(score_solution["score"], 5)
        #         if score_1 == score_2:
        #             response["results"].remove(score_response)
        #             solution["results"].remove(score_solution)
        #             break

        # self.assertEquals(len(response["results"]), 0)
        # self.assertEquals(len(solution["results"]), 0)


if __name__ == "__main__":
    unittest.main()
