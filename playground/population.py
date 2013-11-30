#!/usr/bin/env python
import operator


class Population(object):
    def __init__(self, config):
        self.config = config
        self.generation = 0
        self.individuals = []
        self.best_individuals = []

    def sort_individuals(self):
        self.individuals.sort(key=operator.attrgetter('score'))
