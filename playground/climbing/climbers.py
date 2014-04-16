#!/usr/bin/env python
import copy

from playground.climbing.utils import stop_function as default_stop_function


def hill_climbing(config):
    tweak_function = config["tweak_function"]
    eval_function = config["eval_function"]
    stop_function = config.get("stop_function", default_stop_function)
    candidate = copy.deepcopy(config["candidate"])

    # assign initial best candidate
    initial_best = copy.deepcopy(candidate)
    config["best_score"] = eval_function(initial_best)
    config["best"] = initial_best

    # hill climb
    config["iteration"] = 0
    while stop_function(config) is False:
        # tweak candidate
        candidate = tweak_function(copy.deepcopy(config["best"]))

        # evaluate
        candidate_score = eval_function(candidate)

        # update best
        if candidate_score > config["best_score"]:
            config["best"] = copy.deepcopy(candidate)
            config["best_score"] = candidate_score

        # update iteration
        config["iteration"] += 1

        # print debug msgs
        if config.get("debug", False):
            print "iteration: {0} - {1} - score:{2}".format(
                config["iteration"],
                config["best"],
                config["best_score"]
            )

    return (config["best"], config["best_score"])


# def steepest_ascent_hill_climbing(config):
#     tweaks = config.get("tweaks", 1)
#     tweak_function = config["tweak_function"]
#     eval_function = config["eval_function"]
#     candidate = copy.deepcopy(config["candidate"])
#     stop_function = config.get("stop_function", default_stop_function)
#
#     # assign initial best candidate
#     initial_best = copy.deepcopy(candidate)
#     config["best_score"] = eval_function(initial_best)
#     config["best"] = initial_best
#
#     config["iteration"] = 0
#     while stop_function(config) is False:
#         # tweak candidate
#         for i in range(tweaks):
#             candidate = tweak_function(copy.deepcopy(candidate))
#
#         # evaluate
#         candidate_score = eval_function(candidate)
#
#         # update best
#         if candidate_score > config["best_score"]:
#             config["best"] = copy.deepcopy(candidate)
#             config["best_score"] = candidate_score
#
#         # update iteration
#         config["iteration"] += 1
#
#         # print debug msgs
#         if config.get("debug", False):
#             print "iteration: {0} - {1} - score:{2}".format(
#                 config["iteration"],
#                 config["best"],
#                 config["best_score"]
#             )
#
#     return (config["best"], config["best_score"])
