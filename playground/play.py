#!/usr/bin/env python
import math
import copy
# import json
import random
import multiprocessing
from multiprocessing import Process
from multiprocessing import Manager

from sympy import simplify

from playground.gp_tree.tree_parser import TreeParser
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


def play(details):
    population = details.get("population", None)
    functions = details.get("functions", None)
    evaluate = details.get("evaluate", None)
    selection = details.get("selection", None)
    crossover = details.get("crossover", None)
    mutation = details.get("mutation", None)
    config = details.get("config", None)
    recorder = details.get("recorder", None)

    generation = 0
    max_generation = config["max_generation"]
    goal_reached = False
    tree_parser = TreeParser()

    while generation < max_generation and goal_reached is not True:
        results = []
        evaluate(population.individuals, functions, config, results, recorder)
        population.individuals = results

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

        # record
        if recorder and isinstance(recorder, JSONStore):
            recorder.record_to_file()

    return population


def play_multicore(details):
    population = details.get("population", None)
    functions = details.get("functions", None)
    evaluate = details.get("evaluate", None)
    selection = details.get("selection", None)
    crossover = details.get("crossover", None)
    mutation = details.get("mutation", None)
    config = details.get("config", None)
    recorder = details.get("recorder", None)

    generation = 0
    max_generation = config["max_generation"]
    tree_parser = TreeParser()
    manager = Manager()
    nproc = multiprocessing.cpu_count() * 2

    processes = []
    while generation < max_generation:

        # start proceses
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

        # record
        if recorder and isinstance(recorder, JSONStore):
            # TODO: AGGREGATE different evaluation's before writing to file
            # since different evaluators will have different `eval_stats`
            recorder.record_to_file()

    return population


# def play_multinode(details):
#     population = details.get("population", None)
#     # functions = details.get("functions", None)
#     # evaluate = details.get("evaluate", None)
#     selection = details.get("selection", None)
#     crossover = details.get("crossover", None)
#     mutation = details.get("mutation", None)
#     config = details.get("config", None)
#
#     generation = 0
#     max_generation = config["max_generation"]
#     tree_parser = TreeParser()
#
#     while generation < max_generation:
#         # create a dictionary of trees
#         data = {"config": config, "individuals": []}
#         for individual in population.individuals:
#             tree_json = tree_parser.tree_to_dict(individual, individual.root)
#             data["individuals"].append(tree_json)
#         data = json.dumps(data)
#
#         # evaluate individuals in population
#         results = []
#         for node in config.nodes:
#             results = transmit(
#                 node.host,
#                 node.port,
#                 node.req_type,
#                 node.path,
#                 data
#             )
#         population.individuals = [r for r in results]
#
#         # display best individual
#         population.sort_individuals()
#         best_individual = population.best_individuals[0]
#         print "generation: ", generation
#         print "best_score: " + str(best_individual.score)
#         print "tree_size: " + str(best_individual.size)
#         print ""
#
#         if best_individual.score < 20.0:
#             eq = tree_parser.parse_equation(best_individual.root)
#             if best_individual.size < 50:
#                 print simplify(eq)
#             print ""
#
#         # genetic genetic operators
#         population = selection.select(population)
#         reproduce(population, crossover, mutation, config)
#         generation += 1
#
#     return population
