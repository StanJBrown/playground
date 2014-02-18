#!/usr/bin/env python
import math
import copy
import collections
import random
import multiprocessing
from multiprocessing import Process
from multiprocessing import Manager

from playground.recorder.json_store import JSONStore


def play_details(**kwargs):
    PlayDetails = collections.namedtuple(
        "PlayDetails",
        [
            "population",
            "functions",
            "evaluate",
            "selection",
            "crossover",
            "mutation",
            "config",
            "stop_func",
            "print_func",
            "recorder",
        ]
    )

    return PlayDetails(
        kwargs["population"],
        kwargs.get("functions", None),
        kwargs["evaluate"],
        kwargs.get("selection", None),
        kwargs.get("crossover", None),
        kwargs["mutation"],
        kwargs["config"],
        kwargs.get("stop_func", None),
        kwargs.get("print_func", None),
        kwargs.get("recorder", None),
    )


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

    elif stats["generation_best"].score < stats["current_best"].score:
        stats["current_best"] = stats["generation_best"]
        stats["stale_counter"] = 1  # reset stale counter

    else:
        stats["stale_counter"] += 1

    stats["generation"] += 1


def play(play):
    population = play.population
    stats = {"generation": 0, "stale_counter": 0, "current_best": None}

    # evaluate population
    results = []
    play.evaluate(
        population.individuals,
        play.functions,
        play.config,
        results,
        play.recorder
    )
    population.individuals = results

    while play.stop_func(population, stats, play.config) is False:
        # update stats and print function
        update_generation_stats(stats, population)
        if play.print_func:
            play.print_func(population, stats["generation"])

        # genetic genetic operators
        population = play.selection.select(population)
        reproduce(population, play.crossover, play.mutation, play.config)

        # record
        if play.recorder and isinstance(play.recorder, JSONStore):
            play.recorder.record_population(population)
            play.recorder.record_to_file()

        # evaluate population
        results = []
        play.evaluate(
            population.individuals,
            play.functions,
            play.config,
            results,
            play.recorder
        )
        population.individuals = results

    return population


def play_multicore(play):
    population = play.population
    manager = Manager()
    nproc = float(multiprocessing.cpu_count() * 2)
    stats = {"generation": 0, "stale_counter": 0, "current_best": None}

    # evaluate population
    results = []
    play.evaluate(
        population.individuals,
        play.functions,
        play.config,
        results,
        play.recorder
    )
    population.individuals = results

    processes = []
    while play.stop_func(population, stats, play.config) is False:
        # print function
        update_generation_stats(stats, population)
        if play.print_func:
            play.print_func(population, stats["generation"])

        # genetic genetic operators
        population = play.selection.select(population)
        reproduce(population, play.crossover, play.mutation, play.config)

        # record
        if play.recorder and isinstance(play.recorder, JSONStore):
            play.recorder.record_population(population)
            play.recorder.record_to_file()

        # evaluate population - start multiple proceses
        results = manager.list()
        chunk_sz = int(math.ceil(len(population.individuals) / nproc))
        for i in xrange(int(nproc)):
            start = chunk_sz * i
            end = chunk_sz * (i + 1)
            chunk = population.individuals[start:end]
            args = (chunk, play.functions, play.config, results, play.recorder)

            p = Process(target=play.evaluate, args=args)
            processes.append(p)
            p.start()

        # wait till processes finish
        for p in processes:
            p.join()
        del processes[:]
        population.individuals = [r for r in results]

    return population


def play_evolution_strategy(play):
    population = play.population
    stats = {"generation": 0, "stale_counter": 0, "current_best": None}

    # evaluate population
    results = []
    play.evaluate(
        population.individuals,
        play.functions,
        play.config,
        results,
        play.recorder
    )
    population.individuals = results

    while play.stop_func(population, stats, play.config) is False:
        # print function
        update_generation_stats(stats, population)
        if play.print_func:
            play.print_func(population, stats["generation"])

        # reproduce
        del population.individuals[:]  # because we already have the best
        for i in xrange(play.config["max_population"]):
            child = copy.deepcopy(stats["current_best"])
            play.mutation.mutate(child)
            population.individuals.append(child)

        # record
        if play.recorder and isinstance(play.recorder, JSONStore):
            play.recorder.record_to_file()

        # evaluate population
        results = []
        play.evaluate(
            population.individuals,
            play.functions,
            play.config,
            results,
            play.recorder
        )
        population.individuals = results

    return population
