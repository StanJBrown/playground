#!/usr/bin/env python
import sys
import os
import time
import random
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.config as config
import playground.play as play
from playground.tree import TreeInitializer
from playground.tree import TreeEvaluator
from playground.functions import FunctionRegistry
from playground.operators.selection import Selection
from playground.operators.crossover import GPTreeCrossover
from playground.operators.mutation import GPTreeMutation

# SETTINGS
config_fp = "config.json"


if __name__ == '__main__':
    config = config.load_config(config_fp)

    functions = FunctionRegistry()
    evaluator = TreeEvaluator(config, functions)
    tree_initializer = TreeInitializer(config, evaluator)

    selection = Selection(config)
    crossover = GPTreeCrossover(config)
    mutation = GPTreeMutation(config)

    random.seed(10)  # seed random so results can be reproduced

    # run symbolic regression
    start_time = time.time()
    play.play(tree_initializer, selection, crossover, mutation, config)
    end_time = time.time()
    print("GP run took: %2.2fsecs\n" % (end_time - start_time))
