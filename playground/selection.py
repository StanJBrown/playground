#!/usr/bin/env python
from random import random
from random import sample
import operator

from playground.recorder.record_type import RecordType


class Selection(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.recorder = kwargs.get("recorder", None)

        self.method = None
        self.selected = 0

    def _normalize_scores(self, population):
        # get total
        total_score = 0
        for individual in population.individuals:
            total_score += individual.score

        # normalize
        for individual in population.individuals:
            individual.score = individual.score / total_score

    def roulette_wheel_selection(self, population):
        # normalize individuals
        self._normalize_scores(population)

        # select loop
        self.selected = 0
        max_select = len(population.individuals) / 2
        winners = []
        while self.selected < max_select:

            # spin the wheel
            probability = random()
            cumulative_prob = 0.0
            for individual in population.individuals:
                cumulative_prob += individual.score

                if cumulative_prob >= probability:
                    winners.append(individual)
                    self.selected += 1
                    break

        del population.individuals[:]
        population.individuals = winners
        self.new_pop = population

    def tournament_selection(self, population):
        # select loop
        self.selected = 0
        max_select = self.config["max_population"] / 2
        t_size = self.config["selection"].get("tournament_size", 2)

        winners = []
        while self.selected < max_select:
            # randomly select N individuals for tournament
            tournament = sample(population.individuals, t_size)

            # find best by sorting
            tournament.sort(key=operator.attrgetter('score'))

            # insert winner into new_pop
            winner = tournament[0]
            winners.append(winner)
            self.selected += 1

        del population.individuals[:]
        population.individuals = winners
        self.new_pop = population

    def elitest_selection(self, population):
        percentage = self.config["selection"].get("percentage", 10)
        self.selected = self.config["selection"].get("percentage", 10)
        top = len(population.individuals) / percentage

        # sort population based on fitness and prune the weak
        population.sort_individuals()
        population.individuals = population.individuals[0:top]
        self.new_pop = population

    def select(self, population):
        self.method = self.config["selection"]["method"]

        if self.method == "ROULETTE_SELECTION":
            self.roulette_wheel_selection(population)
        elif self.method == "TOURNAMENT_SELECTION":
            self.tournament_selection(population)
        elif self.method == "ELITEST_SELECTION":
            self.elitest_selection(population)
        else:
            raise RuntimeError("Undefined selection method!")

        if self.recorder:
            self.recorder.record(RecordType.SELECTION, self)

    def to_dict(self):
        self_dict = {
            "method": self.method,
            "selected": self.selected,
            "selected_individuals": [
                i.to_dict()["id"] for i in self.new_pop.individuals
            ]
        }

        return self_dict
