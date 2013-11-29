#!/usr/bin/env python


class Population(object):
    def __init__(self):
        self.max_generation = 0
        self.max_population = 0

        self.generation = 0
        self.population = []

        self.best_individuals = []
        self.top = 0
