#!/usr/bin/env python2
import sys
import os
import time
import random
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.play as play
from playground.config import load_data

import playground.gp.functions as funcs
from playground.gp.cartesian.cartesian_mutation import CartesianMutation
from playground.gp.cartesian.cartesian_generator import CartesianGenerator
from playground.gp.cartesian.cartesian_evaluator import evaluate
from playground.gp.cartesian.cartesian_evaluator import default_stop_func
from playground.gp.cartesian.cartesian_evaluator import print_func

from playground.selection import Selection
from playground.recorder.json_store import JSONStore

# SETTINGS
record_exception = False
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
# config_fp = os.path.join(script_path, "sine_config.json")
# config_fp = os.path.join(script_path, "simple_test_func_4-config.json")


if __name__ == "__main__":
    try:
        # setup
        # random.seed(10)  # seed random so results can be reproduced
        config = {
            "max_population": 100,
            "max_generation": 300000,
            "stale_limit": 2000,
            "stop_score": 0,

            "cartesian": {
                "rows": 1,
                "columns": 30,
                "levels_back": 40,

                "num_inputs": 2,
                "num_outputs": 1
            },

            "evaluator": {
                "use_cache": True
            },

            "selection": {
                "method": "TOURNAMENT_SELECTION",
                "tournament_size": 10
            },

            "mutation": {
                "methods": ["POINT_MUTATION"],
                "probability": 1.0
            },

            "function_nodes": [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "SIN", "arity": 1},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "RAD", "arity": 1}
            ],

            "data_file": "training_data/sine.dat",

            "input_variables": [
                {"type": "INPUT", "name": "x"},
                {"type": "CONSTANT", "name": "1.0"}
            ],

            "response_variables": [{"name": "y"}],

            "recorder": {
                "store_file": "/tmp/ea_stats.dat",
                "record_level": 2
            }
        }
        load_data(config, script_path)

        # add constants
        rows = len(config["data"]["y"])
        # for i in range(11):
        #     config["data"][str(i) + ".0"] = [float(i) for j in range(rows)]
        config["data"]["1.0"] = [1.0 for j in range(rows)]

        # import pprint
        # pprint.pprint(config)

        json_store = JSONStore(config)
        functions = [
            funcs.add_function,
            funcs.sub_function,
            funcs.mul_function,
            funcs.div_function,
            funcs.sin_function,
            funcs.cos_function,
            funcs.rad_function
        ]
        generator = CartesianGenerator(config)

        # genetic operators
        selection = Selection(config, recorder=json_store)
        mutation = CartesianMutation(config)

        # run symbolic regression
        population = generator.init()

        start_time = time.time()
        details = play.play_details(
            population=population,
            evaluate=evaluate,
            functions=functions,
            selection=selection,
            mutation=mutation,
            print_func=print_func,
            stop_func=default_stop_func,
            config=config
        )
        play.play_evolution_strategy(details)
        end_time = time.time()
        print "GP run took: %2.2fsecs\n" % (end_time - start_time)

    except Exception as err:
        print err
        print traceback.print_exc()
