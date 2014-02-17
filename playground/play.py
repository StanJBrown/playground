#!/usr/bin/env python
import math
import copy
# import json
import random
import multiprocessing
from multiprocessing import Process
from multiprocessing import Manager

from playground.recorder.json_store import JSONStore


def reproduce(population, crossover, mutation, config):
    max_pop = config["max_population"]
    individuals = list(population.individuals)
    del population.individuals[:]

    # make individuals even numbered
    if len(individuals) % 2 == 1:
        individuals.append(random.sample(individuals, 1)[0])

    # reproduce individuals
    p_index = 0
    curr_pop = len(individuals)
    reproduce = max_pop - curr_pop
    for i in xrange(0, reproduce + 2, 2):
        # get 2 parents
        parents = individuals[p_index: p_index + 2]
        p_index += 2

        # reset p_index if it is larger then available parents
        if p_index >= curr_pop:
            p_index = 0

        # produce 4 children
        for i in xrange(0, 2):
            child_1 = copy.deepcopy(parents[0])
            child_2 = copy.deepcopy(parents[1])

            crossover.crossover(child_1, child_2)

            mutation.mutate(child_1)
            mutation.mutate(child_2)

            population.individuals.append(child_1)
            population.individuals.append(child_2)

    # remove the extra at the end
    if len(population.individuals) > max_pop:
        for i in xrange(0, len(population.individuals) - max_pop):
            population.individuals.pop()


def update_generation_stats(stats, population):
    # obtain the best individual and set stale counter
    stats["generation_best"] = population.find_best_individuals()[0]

    if stats["current_best"] is None:
        stats["current_best"] = copy.deepcopy(stats["generation_best"])

    elif stats["generation_best"].score <= stats["current_best"].score:
        stats["current_best"] = stats["generation_best"]
        stats["stale_counter"] = 1  # reset stale counter

    else:
        stats["stale_counter"] += 1

    stats["generation"] += 1


def play(details, stop_func, print_func=None):
    population = details["population"]
    functions = details["functions"]
    evaluate = details["evaluate"]
    selection = details["selection"]
    crossover = details["crossover"]
    mutation = details["mutation"]
    config = details["config"]
    recorder = details.get("recorder", None)

    # evolution details
    stats = {"generation": 0, "stale_counter": 0, "current_best": None}

    # evaluate population
    results = []
    evaluate(population.individuals, functions, config, results, recorder)
    population.individuals = results

    while stop_func(population, stats, config) is False:
        # print function
        if print_func:
            print_func(population, stats["generation"])

        # genetic genetic operators
        population = selection.select(population)
        reproduce(population, crossover, mutation, config)
        update_generation_stats(stats, population)

        # evaluate population
        results = []
        evaluate(population.individuals, functions, config, results, recorder)
        population.individuals = results

        # record
        if recorder and isinstance(recorder, JSONStore):
            recorder.record_to_file()

    return population


def play_multicore(details, stop_func, print_func=None):
    population = details["population"]
    functions = details["functions"]
    evaluate = details["evaluate"]
    selection = details["selection"]
    crossover = details["crossover"]
    mutation = details["mutation"]
    config = details["config"]
    recorder = details.get("recorder", None)

    manager = Manager()
    nproc = multiprocessing.cpu_count() * 2

    # evolution details
    stats = {"generation": 0, "stale_counter": 0, "current_best": None}

    # evaluate population
    results = []
    evaluate(population.individuals, functions, config, results, recorder)
    population.individuals = results

    processes = []
    while stop_func(population, stats, config) is False:
        # print function
        if print_func:
            print_func(population, stats["generation"])

        # genetic genetic operators
        population = selection.select(population)
        reproduce(population, crossover, mutation, config)
        update_generation_stats(stats, population)

        # evaluate population - start multiple proceses
        results = manager.list()
        chunksize = int(math.ceil(len(population.individuals) / float(nproc)))
        for i in xrange(nproc):
            chunk = population.individuals[chunksize * i:chunksize * (i + 1)]
            args = (chunk, functions, config, results, recorder)
            p = Process(target=evaluate, args=args)
            processes.append(p)
            p.start()

        # wait till processes finish
        for p in processes:
            p.join()
        del processes[:]
        population.individuals = [r for r in results]

        # record
        if recorder and isinstance(recorder, JSONStore):
            recorder.record_to_file()

    return population


def play_evolution_strategy(details, stop_func, print_func=None):
    # strategy details
    children = details["evolution_strategy"]["lambda"]
    population = details["population"]
    functions = details["functions"]
    evaluate = details["evaluate"]
    mutation = details["mutation"]
    config = details["config"]
    recorder = details.get("recorder", None)

    # evolution details
    results = []
    stats = {"generation": 0, "stale_counter": 0, "current_best": None}

    # evaluate population
    evaluate(population.individuals, functions, config, results, recorder)
    population.individuals = results

    while stop_func(population, stats, config) is False:
        # print function
        if print_func:
            print_func(population, stats["generation"])

        # obtain the best, and destroy current population
        update_generation_stats(stats, population)
        del population.individuals[:]

        # reproduce
        for i in xrange(children):
            child = copy.deepcopy(stats["current_best"])
            mutation.mutate(child)
            population.individuals.append(child)

        # evaluate population
        results = []
        evaluate(population.individuals, functions, config, results, recorder)
        population.individuals = results

        # record
        if recorder and isinstance(recorder, JSONStore):
            recorder.record_to_file()

    return population
