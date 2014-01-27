#!/usr/bin/env python
import sys
import os
import time
import random
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.config as config
import playground.play as play
from playground.gp_tree.tree_generator import TreeGenerator
from playground.gp_tree.tree_evaluation import evaluate
from playground.functions import FunctionRegistry
from playground.operators.selection import Selection
from playground.operators.crossover import GPTreeCrossover
from playground.operators.mutation import GPTreeMutation
from playground.recorder.json_store import JSONStore

# SETTINGS
config_fp = "config.json"


if __name__ == "__main__":
    # setup
    random.seed(10)  # seed random so results can be reproduced
    config = config.load_config(config_fp)
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
    # play.play_multicore(details)
    end_time = time.time()

    print("GP run took: %2.2fsecs\n" % (end_time - start_time))
