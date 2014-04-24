#!/usr/bin/env python
import math
import copy
import random
import collections
import multiprocessing
from multiprocessing import Process
from multiprocessing import Manager

# import matplotlib.pyplot as plt

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
            "tree_editor",
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
        kwargs.get("tree_editor", None),
        kwargs.get("recorder", None)
    )


def reproduce(population, crossover, mutation, config):
    max_pop = config["max_population"]

    # make a copy of population individuals and delete them from population
    parents = list(population.individuals)
    del population.individuals[:]

    # make individuals even numbered
    if len(parents) % 2 == 1:
        parents.append(random.sample(parents, 1)[0])

    # reproduce individuals
    new_gen = []
    for i in xrange(0, len(parents) / 2):
        # get 2 parents
        child_1 = parents.pop()
        child_2 = parents.pop()

        # crossover
        crossover.crossover(child_1, child_2)

        # mutation
        mutation.mutate(child_1)
        mutation.mutate(child_2)

        # append children to new generation
        new_gen.append(child_1)
        new_gen.append(child_2)

    # remove the extra at the end
    if len(new_gen) > max_pop:
        new_gen.pop()

    # assign new generation to population
    population.individuals = new_gen


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
    cache = {}
    play.evaluate(
        population.individuals,
        play.functions,
        play.config,
        results,
        cache,
        play.recorder
    )
    population.individuals = results

    while play.stop_func(population, stats, play.config) is False:
        # update stats and print function
        update_generation_stats(stats, population)
        if play.print_func:
            play.print_func(population, stats["generation"])

        # genetic genetic operators
        play.selection.select(population)
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
            cache,
            play.recorder
        )
        population.individuals = results
        population.generation += 1

        # edit population
        if play.config.get("tree_editor", False):
            every = play.config["tree_editor"]["every"]
            if stats["generation"] != 0 and stats["generation"] % every == 0:
                print "\nEDIT TREES!\n"
                play.tree_editor(population, play.functions)

    # finalize recording
    if play.recorder is not None:
        play.recorder.finalize()
    return population


def play_multicore(play):
    population = play.population
    manager = Manager()
    nproc = float(multiprocessing.cpu_count() * 2)
    stats = {"generation": 0, "stale_counter": 0, "current_best": None}

    # evaluate population
    results = []
    cache = {}
    play.evaluate(
        population.individuals,
        play.functions,
        play.config,
        results,
        cache,
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
        play.selection.select(population)
        reproduce(population, play.crossover, play.mutation, play.config)

        # record
        if play.recorder and isinstance(play.recorder, JSONStore):
            play.recorder.record_population(population)
            play.recorder.record_to_file()

        # evaluate population - start multiple proceses
        results = manager.list()
        cache = manager.dict()
        chunk_sz = int(math.ceil(len(population.individuals) / nproc))
        for i in xrange(int(nproc)):
            start = chunk_sz * i
            end = chunk_sz * (i + 1)
            chunk = population.individuals[start:end]
            args = (
                chunk,
                play.functions,
                play.config,
                results,
                cache,
                play.recorder
            )

            p = Process(target=play.evaluate, args=args)
            processes.append(p)
            p.start()

        # wait till processes finish
        for p in processes:
            p.join()
        del processes[:]
        population.individuals = [r for r in results]
        population.generation += 1

    # finalize recording
    if play.recorder is not None:
        play.recorder.finalize()
    return population


def play_evolution_strategy(play):
    population = play.population
    stats = {"generation": 0, "stale_counter": 0, "current_best": None}

    # evaluate population
    results = []
    cache = {}
    play.evaluate(
        population.individuals,
        play.functions,
        play.config,
        results,
        cache,
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
            cache,
            play.recorder
        )
        population.individuals = results
        population.generation += 1

        # edit population
        if play.config.get("tree_editor", False):
            every = play.config["tree_editor"]["every"]
            if stats["generation"] != 0 and stats["generation"] % every == 0:
                print "\nEDIT TREES!\n"
                play.tree_editor(population, play.functions)

    # finalize recording
    if play.recorder is not None:
        play.recorder.finalize()
    return population
