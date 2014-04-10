#!/usr/bin/env python


def default_stop_function(details):
    max_iterations = details.get("max_iterations", 10)
    max_time = details.get("max_time", None)
    target_score = details.get("target_score", None)
    comparator = details.get("comparator", None)

    if max_iterations:
        if details.get("iteration") == max_iterations:
            return True

    if max_time:
        if details.get("time") >= max_time:
            return True

    if target_score and details.get("best_score"):
        if comparator(details.get("best_score"), target_score) == 0:
            return True

    return False
