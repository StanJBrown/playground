#!/usr/bin/env python
import sys
import os
import time
import random
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.config as config
import playground.play as play
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.tree.tree_evaluation import evaluate
from playground.gp.tree.tree_evaluation import default_stop_func
from playground.gp.tree.tree_evaluation import print_func
from playground.gp.tree.tree_editor import edit_trees
from playground.gp.functions import GPFunctionRegistry
from playground.selection import Selection
from playground.gp.tree.tree_crossover import TreeCrossover
from playground.gp.tree.tree_mutation import TreeMutation
from playground.recorder.json_store import JSONStore

# SETTINGS
record_exception = False
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
config_fp = os.path.join(script_path, "sine_config.json")
# config_fp = os.path.join(script_path, "config.json")


if __name__ == "__main__":
    try:
        # setup
        random.seed(10)  # seed random so results can be reproduced
        config = config.load_config(config_fp, script_path)
        json_store = JSONStore(config)
        functions = GPFunctionRegistry()
        tree_generator = TreeGenerator(config)

        # genetic operators
        selection = Selection(config, recorder=json_store)
        crossover = TreeCrossover(config, recorder=json_store)
        mutation = TreeMutation(config, recorder=json_store)

        # run symbolic regression
        population = tree_generator.init()

        start_time = time.time()
        details = play.play_details(
            population=population,
            functions=functions,
            evaluate=evaluate,
            selection=selection,
            crossover=crossover,
            mutation=mutation,
            print_func=print_func,
            stop_func=default_stop_func,
            config=config,
            tree_editor=edit_trees,
            recorder=json_store
        )

        play.play(details)
        # play.play_multicore(details)
        # play.play_evolution_strategy(details)

        end_time = time.time()
        print "GP run took: %2.2fsecs\n" % (end_time - start_time)

    except Exception as err:
        print err
        print traceback.print_exc()
