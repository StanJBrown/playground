#!/usr/bin/env python2
import math
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.benchmark.symreg_benchmark import gp_benchmark_loop
from playground.parameter_setter.tuner import brute_parameter_sweep


if __name__ == "__main__":
    config = {
        "call_path": os.path.dirname(os.path.realpath(sys.argv[0])),
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
            "tournament_size": 10
        },

        "crossover": {
            "method": "POINT_CROSSOVER",
            "probability": None
        },

        "mutation": {
            "methods": [
                "SUBTREE_MUTATION"
            ],
            "probability": None
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
            {"type": "CONSTANT", "value": 1.0},
            {"type": "CONSTANT", "value": math.pi}
        ],

        "data_file": None,

        "input_variables": [{"type": "INPUT", "name": "var1"}],

        "response_variables": [{"name": "answer"}],

        "recorder": {
            "store_file": None,
            "record_level": "MIN",
            "compress": True
        }

    }

    test_parameters = {
        "play_config": config,
        "random_seeds": [0, 10],
        "iterations": 2,
        "processes": 20,

        "population_size": {
            "range": [
                # 100
                # 150,
                # 200,
                # 250,
                # 300,
                # 350,
                # 400,
                # 450,
                500,
                # 550,
                # 600,
                # 650,
                # 700,
                # 750,
                # 800,
                # 850,
                # 900,
                # 950,
                # 1000
            ]
        },

        "crossover_probability": {
            "range": [
                # 0.05
                # 0.10,
                # 0.15,
                # 0.20,
                # 0.25,
                # 0.30,
                # 0.35,
                # 0.40,
                # 0.45,
                # 0.50,
                0.55,
                0.60,
                0.65,
                0.70,
                # 0.75,
                # 0.80,
                # 0.85,
                # 0.90,
                # 0.95,
                # 1.00
            ]
        },

        "mutation_probability": {
            "range": [
                # 0.05
                # 0.10,
                # 0.15,
                # 0.20,
                # 0.25,
                # 0.30,
                # 0.35,
                # 0.40,
                # 0.45,
                0.50,
                0.55,
                0.60,
                0.65,
                0.70,
                0.75,
                0.80,
                # 0.85,
                # 0.90,
                # 0.95,
                # 1.00
            ]
        },

        "training_data": [
            "training_data/arabas_et_al-f1.dat"
        ],

        "record_dir": "$HOME/data",
        "log_path": "$HOME/data/f1.log"
    }
    functions = {
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

    brute_parameter_sweep(test_parameters, functions, gp_benchmark_loop)
