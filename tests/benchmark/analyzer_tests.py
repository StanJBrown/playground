#!/usr/bin/env python
import os
import sys
import math
import shutil
import unittest
# import time
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.benchmark.analyzer as analyzer
from playground.benchmark.symreg_benchmark import gp_benchmark_loop
from playground.parameter_setter.tuner import brute_parameter_sweep

# SETTINGS
cwd = os.path.dirname(__file__)
log_file = os.path.normpath(os.path.join(cwd, "../data/test.log"))
data_file = "../data/bps--arabas_et_al-f1--100_0.05_0.05-0.zip"
data_file = os.path.join(cwd, data_file)
data_file = os.path.normpath(data_file)

data_file_2 = "$HOME/data/seed_0/bps--arabas_et_al-f1--800_0.8_0.8.zip"


class AnalzyerTests(unittest.TestCase):
    def setUp(self):
        config = {
            "call_path": os.path.dirname(os.path.realpath(sys.argv[0])),
            "max_population": None,
            "max_generation": 100,

            "tree_generation": {
                "method": "RAMPED_HALF_AND_HALF_METHOD",
                "depth_ranges": [
                    {"size": 2, "percentage": 1.0},
                ]
            },

            "evaluator": {"use_cache": True},

            "selection": {"method": "ELITEST_SELECTION"},

            "crossover": {
                "method": "POINT_CROSSOVER",
                "probability": None
            },

            "mutation": {
                "methods": [
                    "SUBTREE_MUTATION",
                    "SHRINK_MUTATION"
                ],
                "probability": None
            },

            "function_nodes": [
                {
                    "type": "FUNCTION",
                    "name": "ADD",
                    "arity": 2
                },
                {
                    "type": "FUNCTION",
                    "name": "SUB",
                    "arity": 2
                },
                {
                    "type": "FUNCTION",
                    "name": "MUL",
                    "arity": 2
                },
                {
                    "type": "FUNCTION",
                    "name": "DIV",
                    "arity": 2
                },
                {
                    "type": "FUNCTION",
                    "name": "COS",
                    "arity": 1
                },
                {
                    "type": "FUNCTION",
                    "name": "SIN",
                    "arity": 1
                }
            ],

            "terminal_nodes": [
                {
                    "type": "TERM",
                    "value": 0.0
                },
                {
                    "type": "TERM",
                    "value": 1.0
                },
                {
                    "type": "TERM",
                    "value": 2.0
                },
                {
                    "type": "TERM",
                    "value": 2.0
                },
                {
                    "type": "TERM",
                    "value": 3.0
                },
                {
                    "type": "TERM",
                    "value": 4.0
                },
                {
                    "type": "TERM",
                    "value": 5.0
                },
                {
                    "type": "TERM",
                    "value": 6.0
                },
                {
                    "type": "TERM",
                    "value": 7.0
                },
                {
                    "type": "TERM",
                    "value": 8.0
                },
                {
                    "type": "TERM",
                    "value": 9.0
                },
                {
                    "type": "TERM",
                    "value": 10.0
                },
                {
                    "type": "TERM",
                    "value": math.pi
                }
            ],
            "data_file": None,

            "input_variables": [{"type": "INPUT", "name": "var1"}],
            "response_variable": {"name": "answer"},

            "recorder": {
                "store_file": None,
                "record_level": "MAX",
                "compress": True
            }

        }

        test_parameters = {
            "play_config": config,
            "iterations": 1,
            "processes": 1,

            "population_size": {"range": [100]},
            "crossover_probability": {"range": [0.80]},
            "mutation_probability": {"range": [0.80, 0.70]},

            "training_data": ["../data/arabas_et_al-f1.dat"],

            "record_dir": "./analyzer_test_data",
            "log_path": "./analyzer_test_data/benchmark.log"
        }
        brute_parameter_sweep(test_parameters, gp_benchmark_loop)

    def tearDown(self):
        shutil.rmtree("./analyzer_test_data")

    def test_parse_datafile(self):
        # pass test
        result = analyzer.parse_data(data_file)
        solution = {
            "population": {
                "generation": 0,
                "best_individual": "(COS((var1 MUL 0.0)))",
                "best_score": 133.6826393201821
            }
        }
        self.assertEquals(result[0]["population"], solution["population"])

        # exception test
        self.assertRaises(IOError, analyzer.parse_data, log_file)

    def test_summarize_data_min_level(self):
        # pass test
        result = analyzer.summarize_data(data_file)

        # import pprint
        # pprint.pprint(result)

        self.assertIsNotNone(result)
        self.assertTrue(len(result["population"]["generation"]), 11)
        self.assertTrue(len(result["population"]["best_score"]), 11)
        self.assertTrue(len(result["population"]["best_individual"]), 11)

        self.assertTrue(len(result["crossover"]["crossovers"]), 11)
        self.assertTrue(len(result["crossover"]["no_crossovers"]), 11)

        self.assertTrue(len(result["mutation"]["mutations"]), 11)
        self.assertTrue(len(result["mutation"]["no_mutations"]), 11)

    def test_summarize_data_max_level(self):
        # test data
        test_data = "bps--arabas_et_al-f1--100_0.8_0.8.zip"
        test_dir = "./analyzer_test_data/seed_0/"
        test_fp = os.path.join(test_dir, test_data)
        test_fp = os.path.normpath(test_fp)

        # summarize data
        result = analyzer.summarize_data(test_fp)

        # import pprint
        # pprint.pprint(result)

        # self.assertIsNotNone(result)
        self.assertTrue(len(result["population"]["generation"]), 14)
        self.assertTrue(len(result["population"]["best_score"]), 14)
        self.assertTrue(len(result["population"]["best_individual"]), 14)

        self.assertTrue(len(result["crossover"]["crossovers"]), 14)
        self.assertTrue(len(result["crossover"]["no_crossovers"]), 14)

        self.assertTrue(len(result["mutation"]["mutations"]), 14)
        self.assertTrue(len(result["mutation"]["no_mutations"]), 14)

    def test_plot_summary(self):
        # tes data
        test_data_1 = "bps--arabas_et_al-f1--100_0.8_0.8.zip"
        test_dir = "./analyzer_test_data/seed_0/"
        test_1_fp = os.path.join(test_dir, test_data_1)

        test_data_2 = "bps--arabas_et_al-f1--100_0.8_0.7.zip"
        test_2_fp = os.path.join(test_dir, test_data_2)

        # summarize data
        test_data_1 = analyzer.summarize_data(test_1_fp)
        test_data_2 = analyzer.summarize_data(test_2_fp)
        data = [test_data_1, test_data_2]
        labels = [
            "c_prob = 0.8, mut_prob = 0.8",
            "c_prob = 0.8, mut_prob = 0.7"
        ]
        analyzer.plot_summary(data, labels)


if __name__ == "__main__":
    unittest.main()
