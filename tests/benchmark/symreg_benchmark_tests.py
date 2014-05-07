#!/usr/bin/env python2
import os
import sys
import math
import copy
import json
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.benchmark.symreg_benchmark import gp_benchmark_loop

# SETTINGS
script_path = os.path.dirname(__file__)


class SymRegBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "random_seed": 0,
            "call_path": script_path,
            "max_population": 100,
            "max_generation": 10,

            "tree_generation": {
                "method": "RAMPED_HALF_AND_HALF_METHOD",
                "depth_ranges": [
                    {"size": 4, "percentage": 0.40},
                    {"size": 3, "percentage": 0.60}
                ]
            },

            "evaluator": {
                "use_cache": True
            },

            "selection": {
                "method": "TOURNAMENT_SELECTION",
                "tournament_size": 10
            },

            "crossover": {
                "method": "COMMON_REGION_POINT_CROSSOVER",
                "probability": 0.8
            },

            "mutation": {
                "methods": [
                    "POINT_MUTATION"
                ],
                "probability": 0.8
            },

            "function_nodes": [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1}
            ],

            "terminal_nodes": [
                {"type": "TERM", "value": 1.0},
                {"type": "TERM", "value": 2.0},
                {"type": "TERM", "value": 2.0},
                {"type": "TERM", "value": 3.0},
                {"type": "TERM", "value": 4.0},
                {"type": "TERM", "value": 5.0},
                {"type": "TERM", "value": 6.0},
                {"type": "TERM", "value": 7.0},
                {"type": "TERM", "value": 8.0},
                {"type": "TERM", "value": 9.0},
                {"type": "TERM", "value": 10.0},
                {"type": "TERM", "value": math.pi}
            ],

            "data_file": "../data/sine.dat",

            "input_variables": [
                {"type": "INPUT", "name": "var1"}
            ],

            "response_variables": [{"name": "answer"}],

            "recorder": {
                "store_file": "/tmp/test.json",
                "compress": True
            },

            "log_path": "/tmp/test.log"

        }
        self.functions = {
            "ADD": "+",
            "SUB": "-",
            "MUL": "*",
            "DIV": "/",
            "POW": "**",
            "SIN": "math.sin",
            "COS": "math.cos",
            "RAD": "math.radians",
            "LN": "math.ln",
            "LOG": "math.log"
        }

    def tearDown(self):
        files = [
            self.config["recorder"]["store_file"],
            self.config["log_path"]
        ]

        for f in files:
            if os.path.isfile(f):
                os.remove(f)

    def test_gp_benchmark_loop(self):
        # pass test
        config_before = copy.deepcopy(self.config)
        self.config["functions"] = self.functions
        result = gp_benchmark_loop(self.config)
        self.assertIsNotNone(result)

        # make sure the data field is removed from benchmark log
        log_file = json.loads(open(self.config["log_path"], "r").read())
        self.assertFalse("data" in log_file)

        # import pprint
        # pprint.pprint(log_file)

        # fail test
        result["data_file"] = config_before["data_file"]
        result.pop("random_seed")
        self.assertRaises(Exception, gp_benchmark_loop, result)


if __name__ == "__main__":
    unittest.main()
