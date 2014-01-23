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
        individuals = []
        no_score = []
        for i in self.individuals:
            if i.score is not None:
                individuals.append(i)
            else:
                no_score.append(i)
        individuals.sort(key=operator.attrgetter('score'))
        individuals.extend(no_score)
        self.individuals = individuals

        self.best_individuals = self.individuals[0:self.best_top]

    def to_dict(self):
        self_dict = {
            "generation": self.generation,
            "best_individual": str(self.best_individuals[0]),
            "best_score": self.best_individuals[0].score,
            "individuals": [i.to_dict() for i in self.individuals]
        }

        return self_dict
