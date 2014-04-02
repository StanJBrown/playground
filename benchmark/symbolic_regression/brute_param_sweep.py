#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.benchmark.symreg_benchmark import gp_benchmark_loop
from playground.parameter_setter.tuner import brute_parameter_sweep


if __name__ == "__main__":
    config = {
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

        "evaluator": {
            "use_cache": True
        },

        "selection": {
            "method": "TOURNAMENT_SELECTION",
            "tournament_size": None
        },

        "crossover": {
            "method": "POINT_CROSSOVER",
            "probability": None
        },

        "mutation": {
            "methods": [
                "POINT_MUTATION"
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
            },
            {
                "type": "FUNCTION",
                "name": "RAD",
                "arity": 1
            }
        ],

        "terminal_nodes": [
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
            }
        ],

        "data_file": None,

        "input_variables": [
            {
                "type": "INPUT",
                "name": "var1"
            }
        ],

        "response_variable": {
            "name": "answer"
        },

        "recorder": {
            "store_file": "/tmp/test.json",
            "compress": True
        }

    }

    test_parameters = {
        "play_config": config,
        "iterations": 1,
        "processes": 4,

        "population_size": {
            "range": [
                # 10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000
                500
                # 1000
            ]
        },

        "crossover_probability": {
            "range": [
                # 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
                # 0.1, 0.2
                0.8
            ]
        },

        "mutation_probability": {
            "range": [
                # 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
                # 0.1, 0.2
                0.2
            ]
        },

        "training_data": [
            "training_data/arabas_et_al-f1.dat",
        ],

        "record_dir": "/tmp/data",
        "log_path": "/tmp/benchmark_navive_parameter_sweep.log"
    }

    brute_parameter_sweep(test_parameters, gp_benchmark_loop)
