#!/usr/bin/env python


def check_iterations(max_iterations, iteration):
    if iteration is None:
        raise RuntimeError("iteration is not defined for stop function!")

    if iteration == max_iterations:
        return True
    else:
        return False


def check_score(target_score, score, comparator):
    if score is None:
        raise RuntimeError("score is not defined for stop function!")
    if comparator is None:
        raise RuntimeError("comparator is not defined for stop function!")

    if comparator(score, target_score) == 0:
        return True
    else:
        return False


def check_time(max_time, time):
    if time is None:
        raise RuntimeError("time is not defined for stop function!")

    if max_time == time:
        return True
    else:
        return False


def stop_function(details):
    max_iterations = details.get("max_iterations", None)
    max_time = details.get("max_time", None)
    target_score = details.get("target_score", None)
    comparator = details.get("comparator", None)

    if max_iterations:
        if check_iterations(max_iterations, details.get("iteration")):
            return True

    if max_time:
        if check_time(max_time, details.get("time")):
            return True

    if target_score:
        if check_score(target_score, details.get("best_score"), comparator):
            return True

    return False
