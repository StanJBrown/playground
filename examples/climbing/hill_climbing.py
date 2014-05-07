#!/usr/bin/env python2
import os
import sys
import random
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.climbing.climbers import hill_climbing
from playground.climbing.utils import stop_function


def eval_function(candidate):
    solution = list("helloworld")
    test = list(candidate)

    # calcuate character difference between two strings
    dist_err = 0
    for i in range(len(test)):
        dist_err += abs(ord(test[i]) - ord(solution[i]))

    return 1000 - dist_err


def tweak_function(candidate):
    # make a copy of candidate to be tweaked
    tweak_candidate = list(candidate)

    # randomly select a character to be tweak
    index = random.randint(0, len(candidate) - 1)

    # randomly tweak up or down
    if random.random() > 0.5:
        tweak_candidate[index] = chr(ord(candidate[index]) + 1)
    else:
        tweak_candidate[index] = chr(ord(candidate[index]) - 1)

    return "".join(tweak_candidate)


def int_cmp(num_1, num_2):
    if num_1 > num_2:
        return 1
    elif num_1 < num_2:
        return -1
    else:
        return 0


if __name__ == "__main__":
    candidate = "abcdefghij"

    details = {
        "debug": True,

        "tweak_function": tweak_function,
        "eval_function": eval_function,
        "stop_function": stop_function,

        "candidate": candidate,
        "max_iterations": 1000,
        "target_score": 1000,

        "comparator": int_cmp
    }

    result = hill_climbing(details)
    print "\nSOLUTION -->", result[0]
