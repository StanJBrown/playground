#!/usr/bin/env python
import operator

from playground.evaluator import EvaluationError


class Population(object):
    def __init__(self, config, evaluator):
        self.config = config
        self.generation = 0
        self.individuals = []
        self.evaluator = evaluator

    def sort_individuals(self):
        self.individuals.sort(key=operator.attrgetter('score'))

    def evaluate_population(self):
        index = 0
        bad_eggs = []

        # evaluate population
        for individual in self.individuals:
            try:
                self.evaluator.evaluate(individual)
                index += 1
            except EvaluationError as e:
                bad_eggs.append(individual)

                print(
                    "Error evaluating individual[{0}]: {1}".format(
                        index,
                        e.message
                    )
                )

        # remove bad individuals
        self.individuals = [i for i in self.individuals if i not in bad_eggs]

    def evaluate_individual(self, individual):
        if individual in self.individuals:
            self.evaluator.evaluate(individual)
