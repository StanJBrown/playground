#!/usr/bin/env python
import copy
import random

from sympy import simplify

from playground.tree import TreeParser


def reproduce(population, crossover, mutation, config):
    curr_pop = len(population.individuals)
    max_pop = config["max_population"]
    reproduce = max_pop - curr_pop

    p_index = 0
    # create children
    for i in range(0, reproduce, 2):
        # get 2 parents
        parents = population.individuals[p_index: p_index + 2]
        p_index += 1

        # produce 2 children
        child_1 = copy.deepcopy(parents[0])
        child_2 = copy.deepcopy(parents[1])

        crossover.crossover(child_1, child_2)

        mutation.mutate(child_1)
        mutation.mutate(child_2)

        population.individuals.append(child_1)
        population.individuals.append(child_2)

    # remove the one extra at the end
    if len(population.individuals) > max_pop:
        population.individuals.pop()


def play(initializer, selection, crossover, mutation, config):
    random.seed(10)
    generation = 0
    max_generation = config["max_generation"]
    goal_reached = False

    tree_parser = TreeParser()

    population = initializer.init()
    while generation < max_generation and goal_reached is not True:
        population.evaluate_population()
        population.sort_individuals()

        best_individual = population.best_individuals[0]
        print "generation: ", generation
        print "best_score: " + str(best_individual.score)
        print "tree_size: " + str(best_individual.size)
        print "match_cached: " + str(population.evaluator.match_cached)
        print "cache_size: " + str(len(population.evaluator.cache))
        population.evaluator.match_cached = 0
        print ""

        if best_individual.score < 1.0:
            eq = tree_parser.parse_equation(best_individual.root)
            if best_individual.size < 20:
                print simplify(eq)
            print ""

        population = selection.select(population)
        reproduce(population, crossover, mutation, config)
        generation += 1
