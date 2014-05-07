#!/usr/bin/env python2
from random import random
from random import sample
import operator

import copy
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
        max_select = self.config["max_population"]
        winners = []
        while self.selected < max_select:

            # spin the wheel
            probability = random()
            cumulative_prob = 0.0
            for individual in population.individuals:
                cumulative_prob += individual.score

                if cumulative_prob >= probability:
                    winners.append(copy.deepcopy(individual))
                    self.selected += 1
                    break

        # replace old population with new
        del population.individuals[:]
        population.individuals = winners
        self.new_pop = population

    def tournament_selection(self, population):
        # select loop
        self.selected = 0
        max_select = self.config["max_population"]
        t_size = self.config["selection"].get("tournament_size", 2)

        winners = []
        while self.selected < max_select:
            # randomly select N individuals for tournament
            tournament = sample(population.individuals, t_size)

            # find best by sorting
            tournament.sort(key=operator.attrgetter('score'))

            # insert winner into new_pop
            winner = tournament[0]
            winners.append(copy.deepcopy(winner))
            self.selected += 1

        # replace old population with new
        del population.individuals[:]
        population.individuals = winners
        self.new_pop = population

    def elitest_selection(self, population):
        percentage = self.config["selection"].get("percentage", 10)
        self.selected = self.config["selection"].get("percentage", 10)

        # sort population based on fitness and get the elites
        population.sort_individuals()
        top = round(len(population.individuals) * percentage, 0)
        elites = population.individuals[0:int(top)]

        # fill out the new population with elites
        parents = []
        elite_index = 0
        for i in range(self.config["max_population"]):
            parents.append(copy.deepcopy(elites[elite_index]))
            elite_index += 1

            # reset elite_index
            if elite_index > (len(elites) - 1):
                elite_index = 0

        # replace old population with new
        del population.individuals[:]
        population.individuals = parents
        self.new_pop = population

    def greedy_over_selection(self, population):
        top = self.config.get("top", 320)
        max_pop = self.config["max_population"]
        pop_size = len(population.individuals)

        # pre-check
        if max_pop < 1000 or pop_size < 1000:
            err_msg = "Error! Greedy-Over selection is for population > 1000"
            raise RuntimeError(err_msg)

        # sort population based on score and place population into 2 groups
        population.sort_individuals()
        group_1 = copy.deepcopy(population.individuals[0:top])
        group_2 = copy.deepcopy(population.individuals[top:])

        # randomly sample from group 1 and 2
        parents = []
        for i in range(self.config["max_population"]):
            if random() >= 0.2:
                parents.append(sample(group_1, 1)[0])
            else:
                parents.append(sample(group_2, 1)[0])

        # replace old population with new
        del population.individuals[:]
        population.individuals = parents
        self.new_pop = population

    def select(self, population):
        self.method = self.config["selection"]["method"]

        if self.method == "ROULETTE_SELECTION":
            self.roulette_wheel_selection(population)
        elif self.method == "TOURNAMENT_SELECTION":
            self.tournament_selection(population)
        elif self.method == "ELITEST_SELECTION":
            self.elitest_selection(population)
        elif self.method == "GREEDY_OVER_SELECTION":
            self.greedy_over_selection(population)
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
