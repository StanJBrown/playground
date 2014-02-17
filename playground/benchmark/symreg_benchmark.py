#!/usr/bin/env python
import sys
import os
import time
import random
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

# import playground.config as config
import playground.play as play
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.tree.tree_evaluation import evaluate
from playground.functions import FunctionRegistry
from playground.operators.selection import Selection
from playground.operators.crossover import GPTreeCrossover
from playground.operators.mutation import GPTreeMutation
from playground.recorder.json_store import JSONStore

import playground.benchmark.symreg_test_funcs as test_funcs

# SETTINGS
record_exception = False
script_path = os.path.dirname(os.path.realpath(__file__))
config_fp = os.path.join(script_path, "config.json")


def benchmark_arabas_et_al_test_functions():
    # generate test data
    test_funcs.arabas_et_al_test_functions(script_path)

    pass


def benchmark_nguyen_et_al_test_functions():
    # generate test data
    test_funcs.nguyen_et_al_test_functions(script_path)

    pass


def benchmark_loop(config):
    try:
        # setup
        random.seed(config["random_seed"])  # VERY IMPORTANT!
        json_store = JSONStore(config)
        functions = FunctionRegistry()
        tree_generator = TreeGenerator(config)

        # genetic operators
        selection = Selection(config, recorder=json_store)
        crossover = GPTreeCrossover(config, recorder=json_store)
        mutation = GPTreeMutation(config, recorder=json_store)

        # run symbolic regression
        population = tree_generator.init()

        start_time = time.time()
        details = {
            "population": population,
            "functions": functions,
            "evaluate": evaluate,
            "selection": selection,
            "crossover": crossover,
            "mutation": mutation,
            "config": config,
            "recorder": json_store
        }

        play.play(details)
        end_time = time.time()

        print("GP run took: %2.2fsecs\n" % (end_time - start_time))

    except Exception as err:
        print err

        # write exception out
        if record_exception:
            exception_file = open("/tmp/symbolic_regression_err.log", "w")
            exception_file.write(str(err) + "\n")
            exception_file.close()


if __name__ == "__main__":
    pass
