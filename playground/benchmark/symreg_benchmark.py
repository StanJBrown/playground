#!/usr/bin/env python
import os
import sys
import time
import json
import random
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

# import playground.config as config
import playground.play as play
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.tree.tree_evaluation import evaluate
from playground.gp.tree.tree_evaluation import default_stop_func
from playground.gp.tree.tree_crossover import TreeCrossover
from playground.gp.tree.tree_mutation import TreeMutation
from playground.gp.functions import GPFunctionRegistry
from playground.selection import Selection
from playground.recorder.json_store import JSONStore


def gp_benchmark_loop(config):
    try:
        # setup
        random.seed(config["random_seed"])  # VERY IMPORTANT!
        json_store = JSONStore(config)
        functions = GPFunctionRegistry()
        tree_generator = TreeGenerator(config)

        # genetic operators
        selection = Selection(config, recorder=json_store)
        crossover = TreeCrossover(config, recorder=json_store)
        mutation = TreeMutation(config, recorder=json_store)

        # setup the initial random population
        population = tree_generator.init()

        # create play details
        details = play.play_details(
            population=population,
            functions=functions,
            evaluate=evaluate,
            selection=selection,
            crossover=crossover,
            mutation=mutation,
            stop_func=default_stop_func,
            config=config,
            recorder=json_store
        )

        # run symbolic regression
        start_time = time.time()
        play.play(details)
        end_time = time.time()
        time_taken = end_time - start_time

        # print msg
        print(
            "DONE -> pop: {0} cross_prob: {1} mut_prob: {2} [{3}s]".format(
                config["max_population"],
                config["crossover"]["probability"],
                config["mutation"]["probability"],
                round(time_taken, 2)
            )
        )

        # log on completion
        if config.get("log_path", False):
            msg = {
                "timestamp": time.mktime(datetime.now().timetuple()),
                "status": "DONE",
                "config": config,
                "runtime": time_taken
            }
            log_file = open(config["log_path"], "a+")
            log_file.write(json.dumps(msg) + "\n")
            log_file.close()

    except Exception as err_msg:
        import traceback
        traceback.print_exc()
        print err_msg

        # log exception
        if config.get("log_path", False):
            msg = {
                "timestamp": time.mktime(datetime.now().timetuple()),
                "status": "ERROR",
                "config": config,
                "error": err_msg
            }
            log_file = open(config["log_path"], "a+")
            log_file.write(json.dumps(msg) + "\n")
            log_file.close()

    return config
