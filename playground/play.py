#!/usr/bin/env python2
import math
import copy
import random
import collections
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
            "plot_func",
            "editor",
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
        kwargs.get("plot_func", None),
        kwargs.get("editor", None),
        kwargs.get("recorder", None)
    )


def play_ga_reproduce(play):
    max_pop = play.config["max_population"]

    # make a copy of selected individuals and delete them from population
    play.selection.select(play.population)
    parents = list(play.population.individuals)
    del play.population.individuals[:]

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
        if play.crossover:
            play.crossover.crossover(child_1, child_2)

        # mutation
        if play.mutation:
            play.mutation.mutate(child_1)
            play.mutation.mutate(child_2)

        # append children to new generation
        new_gen.append(child_1)
        new_gen.append(child_2)

    # remove the extra at the end
    if len(new_gen) > max_pop:
        new_gen.pop()

    # assign new generation to population
    play.population.individuals = new_gen


def play_es_reproduce(play, stats):
    # clear population - because we already have the best
    del play.population.individuals[:]

    # reproduce
    for i in range(4):
        child = copy.deepcopy(stats["all_time_best"])
        play.mutation.mutate(child)
        play.population.individuals.append(child)


def play_update_generation_stats(play, stats):
    # obtain the best individual and set stale counter
    best_individuals = play.population.find_best_individuals()

    if len(best_individuals) > 0:
        stats["generation_best"] = best_individuals[0]
    else:
        stats["generation_best"] = None

    if stats["all_time_best"] is None:
        stats["all_time_best"] = copy.deepcopy(stats["generation_best"])

    if stats["generation_best"] is not None:
        if stats["generation_best"].score < stats["all_time_best"].score:
            stats["all_time_best"] = stats["generation_best"]
            stats["stale_counter"] = 1  # reset stale counter

    else:
        stats["stale_counter"] += 1

    stats["generation"] += 1


def play_display_status(play, stats):
    if play.print_func:
        play.print_func(play.population, stats["generation"])


def play_plot(play, stats):
    if play.plot_func:
        play.plot_func(play, stats)


def play_record(play):
    if play.recorder is not None and isinstance(play.recorder, JSONStore):
        play.recorder.record_population(play.population)
        play.recorder.record_to_file()


def play_finalize_recording(play):
    if play.recorder is not None:
        play.recorder.finalize()


def play_evaluate(play, cache, stats):
    results = []
    output = play.evaluate(
        play.population.individuals,
        play.functions,
        play.config,
        results,
        cache,
        play.recorder
    )
    play.population.individuals = results
    stats["best_output"] = output


def play_multiprocess_evaluate(play, cache):
    results = Manager().list()
    nproc = float(multiprocessing.cpu_count() * 2)
    chunk_sz = int(math.ceil(len(play.population.individuals) / nproc))

    # start multiprocesses
    processes = []
    for i in xrange(int(nproc)):
        start = chunk_sz * i
        end = chunk_sz * (i + 1)
        chunk = play.population.individuals[start:end]
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

    # assign results
    play.population.individuals = [r for r in results]


def play_edit_population(play, stats):
    if play.config.get("editor", False):
        every = play.config["editor"]["every"]
        if stats["generation"] != 0 and stats["generation"] % every == 0:
            print "\nEDIT TREES!\n"
            play.editor(play.population, play.functions)


def play(play):
    cache = {}
    stats = {
        "generation": 0,
        "stale_counter": 0,
        "all_time_best": None,
        "best_output": None
    }

    # evaluate initial population
    play_evaluate(play, cache, stats)
    play_plot(play, stats)

    while play.stop_func(play.population, stats, play.config) is False:
        # update stats and print status
        play_update_generation_stats(play, stats)
        play_display_status(play, stats)
        play_plot(play, stats)

        # genetic operators
        play_ga_reproduce(play)

        # record
        play_record(play)

        # evaluate population
        play_evaluate(play, cache, stats)
        play.population.generation += 1

        # edit population
        play_edit_population(play, stats)

    # finish up
    play_finalize_recording(play)

    return play.population


def play_multicore(play):
    cache = {}
    stats = {"generation": 0, "stale_counter": 0, "all_time_best": None}

    # evaluate population
    play_multiprocess_evaluate(play, cache)

    while play.stop_func(play.population, stats, play.config) is False:
        # update stats and print status
        play_update_generation_stats(play, stats)
        play_display_status(play, stats)

        # genetic operators
        play.selection.select(play.population)
        play_ga_reproduce(play)

        # record
        play_record(play)

        # evaluate population - start multiple proceses
        play_multiprocess_evaluate(play, cache)
        play.population.generation += 1

    # finish up
    play_finalize_recording(play)

    return play.population


def play_evolution_strategy(play):
    cache = {}
    stats = {
        "generation": 0,
        "stale_counter": 0,
        "all_time_best": None,
        "best_output": None
    }

    # evaluate initial population
    play_evaluate(play, cache, stats)
    play_plot(play, stats)

    while play.stop_func(play.population, stats, play.config) is False:
        # print function
        play_update_generation_stats(play, stats)
        play_display_status(play, stats)
        play_plot(play, stats)

        # reproduce
        play_es_reproduce(play, stats)

        # record
        play_record(play)

        # evaluate population
        play_evaluate(play, cache, stats)
        play.population.generation += 1

        # edit population
        play_edit_population(play, stats)

    # finalize recording
    play_finalize_recording(play)

    return play.population
