#!/usr/bin/env python
import operator


class Population(object):
    def __init__(self, config):
        self.config = config

        self.generation = 0
        self.best_top = 10
        self.best_individuals = []
        self.individuals = []

    def sort_individuals(self):
        self.individuals.sort(key=operator.attrgetter('score'))
        self.best_individuals = self.individuals[0:self.best_top]
