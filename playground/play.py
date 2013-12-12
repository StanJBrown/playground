#!/usr/bin/env python
import math
import copy
import random
import multiprocessing
from multiprocessing import Process
from multiprocessing import Manager

from sympy import simplify

from playground.gp_tree.tree_parser import TreeParser


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
    for i in range(0, reproduce + 2, 2):
        # get 2 parents
        parents = individuals[p_index: p_index + 2]
        p_index += 2

        # reset p_index if it is larger then available parents
        if p_index >= curr_pop:
            p_index = 0

        # produce 4 children
        for i in range(0, 2):
            child_1 = copy.deepcopy(parents[0])
            child_2 = copy.deepcopy(parents[1])

            crossover.crossover(child_1, child_2)

            mutation.mutate(child_1)
            mutation.mutate(child_2)

            population.individuals.append(child_1)
            population.individuals.append(child_2)

    # remove the extra at the end
    if len(population.individuals) > max_pop:
        for i in range(0, len(population.individuals) - max_pop):
            population.individuals.pop()


def play(population, selection, crossover, mutation, config, **kwargs):
    generation = 0
    max_generation = config["max_generation"]
    goal_reached = False
    tree_parser = TreeParser()

    while generation < max_generation and goal_reached is not True:
        population.evaluate_population()
        population.sort_individuals()

        # display best individual
        best_individual = population.best_individuals[0]
        print "generation: ", generation
        print "best_score: " + str(best_individual.score)
        print "tree_size: " + str(best_individual.size)
        print "match_cached: " + str(population.evaluator.match_cached)
        print "cache_size: " + str(len(population.evaluator.cache))
        population.evaluator.match_cached = 0  # reset match cached
        print ""

        if best_individual.score < 20.0:
            eq = tree_parser.parse_equation(best_individual.root)
            if best_individual.size < 50:
                print simplify(eq)
            print ""

        # genetic genetic operators
        population = selection.select(population)
        reproduce(population, crossover, mutation, config)
        generation += 1

    return population


def play_multicore(
        population,
        functions,
        evaluator,
        selection,
        crossover,
        mutation,
        config
):
    generation = 0
    max_generation = config["max_generation"]
    tree_parser = TreeParser()
    manager = Manager()
    nproc = multiprocessing.cpu_count()

    processes = []
    score_cache = manager.dict()
    while generation < max_generation:
        # start proceses
        results = manager.list()
        chunksize = int(math.ceil(len(population.individuals) / float(nproc)))
        for i in range(nproc):
            chunk = population.individuals[chunksize * i:chunksize * (i + 1)]
            p = Process(
                target=evaluator,
                args=(chunk, functions, config, score_cache, results)
            )
            processes.append(p)
            p.start()

        # wait till processes finish
        for p in processes:
            p.join()
        del processes[:]
        population.individuals = [r for r in results]

        # display best individual
        population.sort_individuals()
        best_individual = population.best_individuals[0]
        print "generation: ", generation
        print "best_score: " + str(best_individual.score)
        print "tree_size: " + str(best_individual.size)
        print ""

        if best_individual.score < 20.0:
            eq = tree_parser.parse_equation(best_individual.root)
            if best_individual.size < 50:
                print simplify(eq)
            print ""

        # genetic genetic operators
        population = selection.select(population)
        reproduce(population, crossover, mutation, config)
        generation += 1

    return population
