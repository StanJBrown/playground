#!/usr/bin/env python2.7
import os
import sys
import copy
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.config import load_data
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry
import playground.gp.tree.tree_evaluation as tree_eval_1
import playground.gp.tree.tree_evaluation_2 as tree_eval_2

# SETTINGS
script_path = os.path.dirname(__file__)
data_dir = os.path.join(script_path, "../symbolic_regression/training_data")
data_dir = os.path.normpath(data_dir)


if __name__ == "__main__":
    config = {
        "max_population": None,

        "tree_generation": {
            "method": "RAMPED_HALF_AND_HALF_METHOD",
            "depth_ranges": [
                {"size": 4, "percentage": 0.25},
                {"size": 3, "percentage": 0.25},
                {"size": 2, "percentage": 0.25},
                {"size": 1, "percentage": 0.25}
            ]
        },

        "evaluator": {"use_cache": False},

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
        "input_variables": [{"type": "INPUT", "name": "var1"}],
        "response_variable": {"name": "answer"},
        "data_file": "arabas_et_al-f1.dat"
    }
    config["max_population"] = 10000
    load_data(config, data_dir)
    generator = TreeGenerator(config)
    population = generator.init()
    results = []

    # Tree Evalutor 1
    start_time = time.time()
    tree_eval_1.evaluate(
        copy.deepcopy(population.individuals),
        GPFunctionRegistry(),
        config,
        results
    )
    end_time = time.time()
    time_taken = end_time - start_time
    print "Evaluator 1 took:", str(round(time_taken, 2)) + "s"

    # Tree Evalutor 2
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
    start_time = time.time()
    tree_eval_2.evaluate(
        copy.deepcopy(population.individuals),
        functions,
        config,
        results
    )
    end_time = time.time()
    time_taken = end_time - start_time
    print "Evaluator 2 took:", str(round(time_taken, 2)) + "s"
