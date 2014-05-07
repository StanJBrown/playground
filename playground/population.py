#!/usr/bin/env python2
import operator


class Population(object):
    def __init__(self, config):
        self.config = config

        self.generation = 0
        self.best_top = 10
        self.best_individuals = []
        self.individuals = []

    def sort_individuals(self, reverse=False):
        individuals = []
        no_score = []

        for i in self.individuals:
            if i.score is not None:
                individuals.append(i)
            else:
                no_score.append(i)

        individuals.sort(key=operator.attrgetter('score'), reverse=reverse)
        individuals.extend(no_score)

        self.individuals = individuals

    def find_best_individuals(self, reverse=False):
        individuals = [i for i in self.individuals if i.score is not None]
        individuals.sort(key=operator.attrgetter('score'), reverse=reverse)
        self.best_individuals = individuals[0:self.best_top]
        return self.best_individuals

    def to_dict(self):
        self.find_best_individuals()
        self_dict = {
            "generation": self.generation,
            "best_individual": str(self.best_individuals[0]),
            "best_score": self.best_individuals[0].score,
            "individuals": [i.to_dict() for i in self.individuals]
        }

        return self_dict
