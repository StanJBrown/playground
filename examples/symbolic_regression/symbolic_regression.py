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

# SETTINGS
config_fp = "config.json"


if __name__ == "__main__":
    # setup
    config = config.load_config(config_fp)
    random.seed(10)  # seed random so results can be reproduced

    functions = FunctionRegistry()
    tree_generator = TreeGenerator(config)

    # genetic operators
    selection = Selection(config)
    crossover = GPTreeCrossover(config)
    mutation = GPTreeMutation(config)

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
        "config": config
    }
    # play.play(details)
    play.play_multicore(details)
    end_time = time.time()

    print("GP run took: %2.2fsecs\n" % (end_time - start_time))
