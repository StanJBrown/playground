#!/usr/bin/env python
import copy

from playground.climbing.utils import default_stop_function


def hill_climbing(details):
    tweak_function = details["tweak_function"]
    eval_function = details["eval_function"]
    stop_function = details.get("stop_function", default_stop_function)
    candidate = copy.deepcopy(details["candidate"])

    # assign initial best candidate
    best = copy.deepcopy(candidate)
    details["best_score"] = eval_function(best)
    details["best"] = best

    # hill climb
    details["iteration"] = 0
    while stop_function(details) is False:
        # tweak candidate
        candidate = tweak_function(copy.deepcopy(best))

        # evaluate
        candidate_score = eval_function(candidate)

        # update best
        if candidate_score > details["best_score"]:
            best = candidate
            details["best"] = best
            details["best_score"] = candidate_score

        # update iteration and candidate
        details["iteration"] += 1
        details["candidate"] = candidate

        if details.get("debug", False):
            print "iteration: {0} - {1} - score:{2}".format(
                details["iteration"],
                details["best"],
                details["best_score"]
            )

    return (details["best"], details["best_score"])


# def steepest_ascent_hill_climbing(**kwargs):
#     tweaks = kwargs("tweaks", 1)
#     tweak_function = kwargs["tweak_function"]
#     eval_function = kwargs["eval_function"]
#     candidate = copy.deepcopy(kwargs["candidate"])
#     stop_function = kwargs("stop_function", default_stop_function)
#
#     kwargs["iteration"] = 0
#     best = tweak_function(candidate)
#     while stop_function(kwargs):
#         # tweak candidate
#         for i in range(tweaks):
#             candidate = tweak_function(copy.deepcopy(candidate))
#
#
#         # update
#         kwargs["iteration"] += 1
#
#     return best
