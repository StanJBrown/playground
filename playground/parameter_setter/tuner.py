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
    params["crossover"]["probability"] = kwargs["crossover_probability"]
    params["mutation"]["probability"] = kwargs["mutation_probability"]
    params["data_file"] = kwargs["data_file"]

    if kwargs.get("log_path", False) and kwargs.get("log_path") is not None:
        params["log_path"] = kwargs["log_path"]

    return params


def _record_fp(details, seed, training_data):
    pop = details[0]
    cross = details[1]
    mut = details[2]

    # get training data file name
    basename = os.path.basename(training_data)
    td = os.path.splitext(basename)[0]

    # build record file path
    folder = "{0}/seed_{1}/pop_{2}".format(td, seed, pop)
    fn = "{0}-{1}.dat".format(cross, mut)
    record_fp = os.path.join(folder, fn)

    return record_fp


def _set_record_file(details, param, record_file):
    if details["record_dir"]:
        path = os.path.join(details["record_dir"], record_file)
        param["recorder"]["store_file"] = path

    else:
        param["recorder"]["store_file"] = record_file


def _parallel_param_sweep(details, params, loop_func):
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


def brute_parameter_sweep(details, functions, loop_func=None, debug=False):
    config_vars = [
        "population_size",
        "crossover_probability",
        "mutation_probability"
    ]
    config_sets = [details[var]["range"] for var in config_vars]
    config_matrix = list(itertools.product(*config_sets))

    # pre-check
    if details["iterations"] != len(details["random_seeds"]):
        err = "Number of iterations do no match number of random seeds!"
        raise RuntimeError(err)

    # build run parmaters
    params = []
    for data_file in details["training_data"]:
        for i in range(details["iterations"]):
            for config in config_matrix:
                # build parameters
                seed = details["random_seeds"][i]

                gp_param = _build_parameters(
                    seed,
                    details["play_config"],
                    max_population=config[0],
                    crossover_probability=config[1],
                    mutation_probability=config[2],
                    data_file=data_file,
                    log_path=details.get("log_path")
                )
                gp_param["functions"] = functions

                # record file
                record_file = _record_fp(config, seed, data_file)
                _set_record_file(details, gp_param, record_file)

                # add run parmaters to list of params
                params.append(gp_param)

    # execute parameter sweep
    if debug is False:
        _parallel_param_sweep(details, params, loop_func)
    else:
        pprint.pprint(params)
