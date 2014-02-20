#!/usr/bin/env python
import os
import sys
import time
import json
import random
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

# import playground.config as config
import playground.play as play
from playground.config import load_config
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.tree.tree_evaluation import evaluate
from playground.gp.tree.tree_evaluation import default_stop_func
from playground.gp.functions import GPFunctionRegistry
from playground.operators.selection import Selection
from playground.operators.crossover import GPTreeCrossover
from playground.operators.mutation import GPTreeMutation
from playground.recorder.json_store import JSONStore
from playground.parameter_setter.tuner import naive_parameter_sweep

# SETTINGS
record_exception = False
script_path = os.path.dirname(os.path.realpath(__file__))
config_fp = os.path.join(script_path, "config", "template_config.json")


def benchmark_naive_parameter_sweep(config, training_files):
    for data_file in training_files:
        config["data_file"] = data_file
        naive_parameter_sweep(config, benchmark_loop_gp_tree)


def benchmark_loop_gp_tree(config):
    print(
        "RUN -> pop size: {0} crossover prob: {1} mutation prob: {2}".format(
            config["max_population"],
            config["crossover"]["probability"],
            config["mutation"]["probability"]
        )
    ),
    try:
        # setup
        random.seed(config["random_seed"])  # VERY IMPORTANT!
        json_store = JSONStore(config)
        functions = GPFunctionRegistry()
        tree_generator = TreeGenerator(config)

        # genetic operators
        selection = Selection(config, recorder=json_store)
        crossover = GPTreeCrossover(config, recorder=json_store)
        mutation = GPTreeMutation(config, recorder=json_store)

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
            stop_func=default_stop_func,
            config=config,
            recorder=json_store
        )

        play.play(details)
        end_time = time.time()

        print(
            "pop size: {0} crossover prob: {1} mutation prob: {2}".format(
                config["max_population"],
                config["crossover"]["probability"],
                config["mutation"]["probability"]
            )
        ),
        print(" [run took: %2.2fsecs]" % (end_time - start_time))

    except Exception as err_msg:
        print err_msg

        # write exception out
        err = open(
            "/tmp/play-{0}-{1}-{2}-{3}.err".format(
                config["max_population"],
                config["crossover"]["probability"],
                config["mutation"]["probability"],
                config["random_seed"],
            ),
            "w+"
        )
        err.write(str(err_msg) + "\n\n")
        err.write(json.dumps(config))
        err.close()


if __name__ == "__main__":
    config = load_config(config_fp, script_path)

    training_data = [
        "training_data/arabas_et_al-f1.dat",
    ]

    param_config = {
        "play_config": config,
        "iterations": 1,

        "population_size": {
            "range": [
                # 10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000
                500
                # 10
            ]
        },

        "crossover_probability": {
            "range": [
                # 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
                # 0.1, 0.2
                0.8
            ]
        },

        "mutation_probability": {
            "range": [
                # 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
                # 0.1, 0.2
                0.2
            ]
        },

        "record_dir": "/tmp/data"
    }

    benchmark_naive_parameter_sweep(param_config, training_data)
