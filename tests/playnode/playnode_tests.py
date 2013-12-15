#!/usr/bin/env python
import os
import sys
import json
import time
import random
import httplib
import unittest
import subprocess
from subprocess import Popen
from subprocess import check_call
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from playnode.playnode import PlayNodeType
from playnode.playnode import PlayNodeMessage

import playground.config
from playground.gp_tree.tree_generator import TreeGenerator
from playground.gp_tree.tree_parser import TreeParser

# SETTINGS
n_script = "playnode/playnode.py"
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


class PlayNodeTests(unittest.TestCase):
    def setUp(self):
        self.processes = 0

        host = "localhost"
        self.ports = ["8080", "8081", "8082"]
        ntype = PlayNodeType.EVALUATOR

        # start the playground nodes
        Popen(["python", n_script, host, self.ports[0], ntype])
        Popen(["python", n_script, host, self.ports[1], ntype])
        Popen(["python", n_script, host, self.ports[2], ntype])

        # sleep for 2 seconds while the servers are starting
        time.sleep(1)

    def tearDown(self):
        # shutdown all the playground nodes
        for port in self.ports:
            print("Shutting down server at port: %s" % port)
            self.transmit("localhost", port, "GET", "shutdown")

    def transmit(self, host, port, req_type, path, data=None):
        request = "/" + path

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

        self.assertEquals(data["message"], PlayNodeMessage.UNDEFINED)

    def test_evaluate(self):
        random.seed(10)
        solution = {
            "results": [
                {
                    "score": 5850.583080457591
                },
                {
                    "score": 179.9910872464443
                },
                {
                    "score": 180.08885282752195
                },
                {
                    "score": 10268156.940222878
                },
                {
                    "score": 359.2584358901559
                },
                {
                    "score": 3882452.139430426
                },
                {
                    "score": 360.76259843056084
                },
                {
                    "score": 4910.532751076735
                }
            ]
        }

        # setup
        config = playground.config.load_config(config_fp)
        tree_parser = TreeParser()
        population = TreeGenerator(config).init()

        # create a JSON of trees
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

    def test_shutdown(self):
        servers_before = self.check_nodes()
        self.transmit("localhost", 8080, "GET", "shutdown")
        servers_after = self.check_nodes()

        self.ports.remove("8080")
        self.assertTrue(servers_before > servers_after)


if __name__ == '__main__':
    unittest.main()
