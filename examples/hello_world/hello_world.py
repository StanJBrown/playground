#!/usr/bin/env python2
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.play as play
from playground.ga.bit_string_generator import BitStringGenerator
from playground.ga.bit_string_crossover import BitStringCrossover
from playground.ga.bit_string_mutation import BitStringMutation
from playground.selection import Selection

# GLOBAL VARS
solution = ["h", "e", "l", "l", "o", " ", "w", "o", "r", "l", "d", "!"]


def eval_bit_string(string):
    # pre-check
    if len(string.genome) != len(solution):
        raise RuntimeError("Solution and string are not same length!")

    # evaluate string
    fitness = 0
    for i in range(len(string.genome)):
        if string.genome[i] != solution[i]:
            fitness += 1

    return fitness, None


def evaluate(individuals, functions, config, results, cache={}, recorder=None):
    match_cached = 0

    # evaluate bit strings
    for individual in individuals:
        score = None
        res = None

        if str(individual.genome) not in cache:
            score, res = eval_bit_string(individual)
        else:
            score = cache[str(individual.genome)]
            match_cached += 1

        # check result
        if score is not None:
            individual.score = score
            results.append(individual)

        cache[str(individual.genome)] = score


def print_func(population, generation):
    # display best individual
    best = population.find_best_individuals()[0]
    print "> gen: {0} best: {1} [score: {2}]".format(
        generation,
        "".join(best.genome),
        str(best.score)
    )


def stop_func(population, general_stats, config):
    max_gen = config["max_generation"]
    stale_limit = config.get("stale_limit", 10)
    stop_score = config.get("stop_score", None)

    if general_stats["generation"] > 1:
        if stop_score >= general_stats["all_time_best"].score:
            return True

    if general_stats["generation"] >= max_gen:
        return True

    elif general_stats["stale_counter"] >= stale_limit:
        return True

    return False


if __name__ == "__main__":
    try:
        config = {
            "max_population": 100,
            "max_generation": 2000,
            "stale_limit": 2000,
            "stop_score": 0,

            "bitstring_generation": {
                "genome_length": len(solution)
            },

            "codons": [
                # big caps - alphabet
                "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y", "Z",

                # small caps - alphabet
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                "u", "v", "w", "x", "y", "z",

                # symbols
                "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                "_", "+", "-", "=", "{", "}", "|", ":", '"', ";",
                "'", "<", ">", "?", ",", ".", "/",

                # space char
                " "
            ],

            "selection": {
                "method": "TOURNAMENT_SELECTION",
                "tournament_size": 2
            },

            "crossover": {
                "method": "ONE_POINT_CROSSOVER",
                "probability": 0.8
            },

            "mutation": {
                "method": ["POINT_MUTATION"],
                "probability": 0.2
            }
        }

        generator = BitStringGenerator(config)

        # genetic operators
        selection = Selection(config)
        crossover = BitStringCrossover(config)
        mutation = BitStringMutation(config)

        # run GA
        population = generator.init()

        details = play.play_details(
            population=population,
            evaluate=evaluate,
            functions=None,
            selection=selection,
            crossover=crossover,
            mutation=mutation,
            print_func=print_func,
            stop_func=stop_func,
            config=config,
        )
        start_time = time.time()
        play.play(details)
        end_time = time.time()
        print "GA run took: %2.2fsecs\n" % (end_time - start_time)

    except Exception as err:
        raise
