#!/usr/bin/env python2
import sys
import os
import time
import random
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.play as play
from playground.config import load_data
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
        config = {
            "max_population": 700,
            "max_generation": 100,
            "stale_limit": 10,

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
                "tournament_size": 150
            },

            "crossover": {
                "method": "POINT_CROSSOVER",
                "probability": 0.9
            },

            "mutation": {
                "methods": [
                    "SUBTREE_MUTATION",
                    "SHRINK_MUTATION",
                    "POINT_MUTATION"
                ],
                "probability": 0.8
            },

            "function_nodes": [
                {
                    "type": "CLASS_FUNCTION",
                    "name": "GREATER_THAN",
                    "arity": 2,

                    "data_range": {
                        "lower_bound": 0.0,
                        "upper_bound": 10.0,
                        "decimal_places": 0,
                    }
                },
                {
                    "type": "CLASS_FUNCTION",
                    "name": "LESS_THAN",
                    "arity": 2,

                    "data_range": {
                        "lower_bound": 0.0,
                        "upper_bound": 10.0,
                        "decimal_places": 0,
                    }
                },
                {
                    "type": "CLASS_FUNCTION",
                    "name": "EQUALS",
                    "arity": 2,
                    "decimal_precision": 2
                }
            ],

            "classification_attributes": [
                "sepal_length",
                "sepal_width",
                "petal_length",
                "petal_width"
            ],

            "terminal_nodes": [
                {"type": "INPUT", "name": "species"}
            ],

            "data_file": "training_data/sine.dat",

            "input_variables": [
                {"type": "INPUT", "name": "sepal_length"},
                {"type": "INPUT", "name": "sepal_width"},
                {"type": "INPUT", "name": "petal_length"},
                {"type": "INPUT", "name": "petal_width"}
            ],

            "response_variables": [{"name": "species"}],

            "live_plot": {
                "every": 1,
                "x-axis": "x",
                "y-axis": "y"
            },

            "recorder": {
                "store_file": "/tmp/ea_stats.dat",
                "record_level": 2
            }
        }
        load_data(config, script_path)
        json_store = JSONStore(config)
        functions = None
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
