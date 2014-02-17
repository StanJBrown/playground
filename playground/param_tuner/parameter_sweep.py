#!/usr/bin/env python
import itertools


def naive_parameter_sweep(details, benchmark_func, debug=False):
    play_config = details["play_config"]
    iterations = details["iterations"]

    config_vars = [
        "population_size",
        "crossover_probability",
        "mutation_probability"
    ]

    config_sets = []
    for config_var in config_vars:
        config_sets.append(details[config_var]["range"])

    config_matrix = list(itertools.product(*config_sets))
    for seed in range(iterations):
        for config in config_matrix:
            play_config["random_seed"] = seed
            play_config["population_size"] = config[0]
            play_config["crossover"]["probability"] = config[1]
            play_config["mutation"]["probability"] = config[2]

            if debug is False:
                benchmark_func(play_config)

            print "PLAY CONFIGURATION"
            print "-" * 70
            print "random_seed:", seed
            print "population size:", config[0]
            print "crossover probability:", config[1]
            print "mutation probability:", config[2]
            print


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
