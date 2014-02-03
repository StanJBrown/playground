#!/usr/bin/env python
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
from playground.playnode.node import PlayNodeMessage

import playground.config
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.tree.tree_parser import TreeParser

# SETTINGS
n_script = "playground/playnode/node.py"
cwd = os.path.dirname(__file__)
config_fp = os.path.normpath(os.path.join(cwd, "../config/playnode.json"))


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
            ["python", n_script, host, "8080", ntype],
            ["python", n_script, host, "8081", ntype],
            ["python", n_script, host, "8082", ntype]
        ]

        # start the playground nodes
        self.node_1 = Popen(nodes[0], preexec_fn=os.setsid)
        self.node_2 = Popen(nodes[1], preexec_fn=os.setsid)
        self.node_3 = Popen(nodes[2], preexec_fn=os.setsid)

        # sleep for 2 seconds while the servers are starting
        time.sleep(1)

    def tearDown(self):
        # shutdown all the playground nodes
        os.kill(self.node_1.pid, signal.SIGTERM)
        os.kill(self.node_2.pid, signal.SIGTERM)
        os.kill(self.node_3.pid, signal.SIGTERM)

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

    def test_message(self):
        msg = json.dumps({"message": "Hello World"})
        data = self.transmit("localhost", 8080, "POST", "message", msg)
        data = json.loads(data)

        self.assertEquals(data["message"], PlayNodeMessage.OK)

    def test_evaluate(self):
        random.seed(10)
        solution = {
            "results":
            [
                {"score": 15772136.12176585},
                {"score": 359.25843589015597},
                {"score": 26143.96584493737},
                {"score": 16037486.969560817},
                {"score": 14055183243.355433},
                {"score": 3665.4193106433404},
                {"score": 185.83838425682123},
                {"score": 23439.33097274221}
            ]
        }

        # setup
        config = playground.config.load_config(config_fp)
        tree_parser = TreeParser()
        population = TreeGenerator(config).init()

        # create a dictionary of trees
        data = {"config": config, "individuals": []}
        for individual in population.individuals:
            tree_json = tree_parser.tree_to_dict(individual, individual.root)
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
        path = "evaluate_trees"
        response = self.transmit(host, port, req_type, path, data)
        response = json.loads(response)

        print response

        # assert tests
        for score_solution in list(solution["results"]):
            for score_response in list(response["results"]):
                score_1 = round(score_response["score"], 5)
                score_2 = round(score_solution["score"], 5)
                if score_1 == score_2:
                    response["results"].remove(score_response)
                    solution["results"].remove(score_solution)
                    break

        self.assertEquals(len(response["results"]), 0)
        self.assertEquals(len(solution["results"]), 0)


if __name__ == '__main__':
    unittest.main()
