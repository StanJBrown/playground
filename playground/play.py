#!/usr/bin/env python
import copy


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
    generation = 0
    max_generation = config["max_generation"]
    goal_reached = False

    population = initializer.init()
    while generation < max_generation and goal_reached is not True:
        print "generation: ", generation
        population.evaluate_population()
        population.sort_individuals()

        population = selection.select(population)
        reproduce(population, crossover, mutation, config)
        generation += 1
