#!/usr/bin/env python
import operator

from playground.functions import EvaluationError


class Population(object):
    def __init__(self, config, evaluator):
        self.config = config
        self.evaluator = evaluator

        self.generation = 0
        self.best_top = 10
        self.best_individuals = []
        self.individuals = []

    def sort_individuals(self):
        self.individuals.sort(key=operator.attrgetter('score'))
        self.best_individuals = self.individuals[0:self.best_top]

    def evaluate_population(self):
        index = 0
        bad_eggs = []

        # evaluate population
        for individual in self.individuals:
            try:
                self.evaluator.evaluate(individual)
                index += 1
            except EvaluationError:
                bad_eggs.append(individual)

        # remove bad individuals
        self.individuals = [i for i in self.individuals if i not in bad_eggs]

    def evaluate_individual(self, individual):
        try:
            if individual in self.individuals:
                self.evaluator.evaluate(individual)
        except EvaluationError:
            self.individuals.remove(individual)
