#!/usr/bin/env python
import os
import sys
import shutil
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from playground.benchmark.symreg_benchmark import gp_benchmark_loop
import playground.parameter_setter.tuner as tuner


# SETTINGS
script_path = os.path.dirname(__file__)
unittest_root = os.path.normpath(os.path.join(script_path, "../"))


class TunerTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "random_seed": None,
            "max_population": None,

            "crossover": {"probability": None},
            "mutation": {"probability": None},

            "data_file": None,
            "log_path": None
        }

    def tearDown(self):
        if os.path.exists("/tmp/unittest/"):
            shutil.rmtree("/tmp/unittest/")

    def test_build_parameters(self):
        details = {
            "max_population": 10,
            "crossover_probability": 0.7,
            "mutation_probability": 0.7,
            "data_file": "test_file.dat",
            "log_path": "/tmp"
        }
        param = tuner._build_parameters(0, self.config, **details)

        # assert
        self.assertEquals(param["random_seed"], 0)
        self.assertEquals(param["crossover"]["probability"], 0.7)
        self.assertEquals(param["mutation"]["probability"], 0.7)
        self.assertEquals(param["data_file"], "test_file.dat")
        self.assertEquals(param["log_path"], "/tmp")

    def test_record_fp(self):
        details = [100, 0.8, 0.7]
        result = tuner._record_fp(details, 0, "test_file.dat")

        # assert
        self.assertEquals(result, "test_file/seed_0/pop_100/0.8-0.7.dat")

    def test_set_record_file(self):
        details = {
            "record_dir": "/tmp",
        }
        param = {"recorder": {"store_file": None}}
        record_file = "test.json"
        tuner._set_record_file(details, param, record_file)

        # assert
        self.assertEqual(param["recorder"]["store_file"], "/tmp/test.json")

    def test_brute_parameter_sweep(self):
        config = {
            "call_path": unittest_root,
            "max_population": None,
            "max_generation": 1000,

            "tree_generation": {
                "method": "RAMPED_HALF_AND_HALF_METHOD",
                "depth_ranges": [
                    {"size": 4, "percentage": 0.25},
                    {"size": 3, "percentage": 0.25},
                    {"size": 2, "percentage": 0.25},
                    {"size": 1, "percentage": 0.25}
                ]
            },

            "evaluator": {"use_cache": True},
            "selection": {"method": "ELITEST_SELECTION"},
            "crossover": {"method": "POINT_CROSSOVER", "probability": None},
            "mutation": {"methods": ["SUBTREE_MUTATION"], "probability": None},

            "function_nodes": [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1}
            ],

            "terminal_nodes": [
                {"type": "TERM", "value": 0.0},
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
            ],

            "data_file": None,

            "input_variables": [{"type": "INPUT", "name": "var1"}],
            "response_variable": {"name": "answer"},

            "recorder": {
                "store_file": None,
                "record_level": "MIN",
                "compress": True
            }
        }

        test_parameters = {
            "play_config": config,
            "iterations": 1,
            "processes": 1,

            "population_size": {"range": [100]},
            "crossover_probability": {"range": [0.80]},
            "mutation_probability": {"range": [0.10]},

            "training_data": ["data/arabas_et_al-f1.dat"],

            "record_dir": "/tmp/unittest",
            "log_path": "/tmp/unittest/benchmark.log"
        }

        tuner.brute_parameter_sweep(test_parameters, gp_benchmark_loop)


if __name__ == "__main__":
    unittest.main()
