#!/usr/bin/env python
import os
import copy
import itertools
import multiprocessing


def naive_parameter_sweep(details, loop_func=None, debug=False):
    cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(details.get("processes", cpus))
    config_vars = [
        "population_size",
        "crossover_probability",
        "mutation_probability"
    ]
    config_sets = [details[var]["range"] for var in config_vars]
    config_matrix = list(itertools.product(*config_sets))
    iterations = details["iterations"]

    # build sweep parameters
    p_configs = []
    for seed in range(iterations):
        for config in config_matrix:
            p_config = {}
            p_config = copy.deepcopy(details["play_config"])

            # main parameters
            p_config["random_seed"] = seed
            p_config["max_population"] = config[0]
            p_config["selection"]["tournament_size"] = config[0] / 10
            p_config["crossover"]["probability"] = config[1]
            p_config["mutation"]["probability"] = config[2]

            # record file
            file_format = "np_sweep_{0}_{1}_{2}-{3}.dat".format(
                config[0],
                config[1],
                config[2],
                seed
            )

            # record file and dir
            if details["record_dir"]:
                path = os.path.join(details["record_dir"], file_format)
                p_config["json_store"]["store_file"] = path

            else:
                p_config["json_store"]["store_file"] = file_format

            p_configs.append(p_config)

    # execute parameter sweep
    if debug is False:
        pool.map(loop_func, p_configs)


if __name__ == "__main__":
    details = {
        "iterations": 5,

        "play_config": {

            "population_size": None,

            "crossover": {
                "probability": None
            },

            "mutation": {
                "probability": None
            }
        },

        "population_size": {
            "range": [
                10,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ]
        },

        "crossover_probability": {
            "range": [
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1.0,
            ]
        },

        "mutation_probability": {
            "range": [
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1.0,
            ]
        }
    }

    naive_parameter_sweep(details, None, True)
