#!/usr/bin/env python
import os
import copy
import pprint
import itertools
import multiprocessing
from datetime import datetime


def _build_parameters(seed, play_config, **kwargs):
    params = {}
    params = copy.deepcopy(play_config)

    # main parameters
    params["random_seed"] = seed
    params["max_population"] = kwargs["max_population"]
    params["selection"]["tournament_size"] = int(
        kwargs["max_population"] * 0.1
    )
    params["crossover"]["probability"] = kwargs["crossover_probability"]
    params["mutation"]["probability"] = kwargs["mutation_probability"]
    params["data_file"] = kwargs["data_file"]

    if kwargs.get("log_path", False) and kwargs.get("log_path") is not None:
        params["log_path"] = kwargs["log_path"]

    return params


def naive_parameter_sweep(details, loop_func=None, debug=False):
    config_vars = [
        "population_size",
        "crossover_probability",
        "mutation_probability"
    ]
    config_sets = [details[var]["range"] for var in config_vars]
    config_matrix = list(itertools.product(*config_sets))

    # build sweep parameters
    params = []
    for data_file in details["training_data"]:
        for seed in range(details["iterations"]):
            for config in config_matrix:
                # build parameters
                param = _build_parameters(
                    seed,
                    details["play_config"],
                    max_population=config[0],
                    crossover_probability=config[1],
                    mutation_probability=config[2],
                    data_file=data_file,
                    log_path=details.get("log_path")
                )

                # record file
                record_file = "np_sweep_{0}_{1}_{2}-{3}.dat".format(
                    config[0],
                    config[1],
                    config[2],
                    seed
                )

                # record file and dir
                if details["record_dir"]:
                    path = os.path.join(details["record_dir"], record_file)
                    param["json_store"]["store_file"] = path

                else:
                    param["json_store"]["store_file"] = record_file

                params.append(param)

    # execute parameter sweep in parallel
    if debug is False:
        try:
            pool = multiprocessing.Pool(details.get("processes", 1))
            pool.map(loop_func, params)

        except KeyboardInterrupt:
            msg = "Received TERM signal, terminating..."
            print msg

            # write exception to log
            if details.get("log_path", False):
                timestamp = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
                log_file = open(details["log_path"], "a+")
                log_file.write(timestamp + ": " + msg + "\n")
                log_file.close()

            pool.terminate()

    else:
        pprint.pprint(params)


def racing_algorithm_sweep(details, loop_func=None, debug=False):
    pass
