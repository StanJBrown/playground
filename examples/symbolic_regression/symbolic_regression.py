#!/usr/bin/env python2
import sys
import os
import time
import random
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.config as config
import playground.play as play
from playground.gp.tree.generator import TreeGenerator
from playground.gp.tree.evaluation import default_stop_func
from playground.gp.tree.evaluation import print_func
from playground.gp.tree.evaluation_2 import plot_func
from playground.gp.tree.evaluation_2 import evaluate
from playground.gp.tree.editor import edit_trees
from playground.selection import Selection
from playground.gp.tree.crossover import TreeCrossover
from playground.gp.tree.mutation import TreeMutation
from playground.recorder.json_store import JSONStore

# SETTINGS
record_exception = False
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
config_fp = os.path.join(script_path, "sine_config.json")
# config_fp = os.path.join(script_path, "simple_test_func_4-config.json")


if __name__ == "__main__":
    try:
        # setup
        random.seed(10)  # seed random so results can be reproduced
        config = config.load_config(config_fp, script_path)
        json_store = JSONStore(config)
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
        generator = TreeGenerator(config)

        # genetic operators
        selection = Selection(config, recorder=json_store)
        crossover = TreeCrossover(config, recorder=json_store)
        mutation = TreeMutation(config, recorder=json_store)

        # run symbolic regression
        population = generator.init()

        start_time = time.time()
        details = play.play_details(
            population=population,
            evaluate=evaluate,
            functions=functions,
            selection=selection,
            crossover=crossover,
            mutation=mutation,
            print_func=print_func,
            plot_func=plot_func,
            stop_func=default_stop_func,
            config=config,
            editor=edit_trees,
            recorder=json_store
        )

        play.play(details)
        # play.play_evolution_strategy(details)

        end_time = time.time()
        print "GP run took: %2.2fsecs\n" % (end_time - start_time)

    except Exception as err:
        print err
        print traceback.print_exc()
