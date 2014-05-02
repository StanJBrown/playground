#!/usr/bin/env python2.7
import os
import sys
import random
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import playground.config as config
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry
from playground.selection import Selection

# SETTINGS
cwd = os.path.dirname(__file__)
config_fp = os.path.normpath(os.path.join(cwd, "config/selection.json"))


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)

        self.functions = GPFunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)

        self.selection = Selection(self.config)
        self.population = self.tree_generator.init()

        # give population random scores
        for inidividual in self.population.individuals:
            inidividual.score = random.triangular(1, 100)

    def print_population(self, phase, population):
        print "{0}[{1}]:".format(phase, len(population.individuals))
        for individual in population.individuals:
            print individual, individual.score
        print '\n\n'

        return len(population.individuals)

    def test_normalize_scores(self):
        self.selection._normalize_scores(self.population)

        total_sum = 0
        for individual in self.population.individuals:
            total_sum += individual.score

        self.assertEquals(round(total_sum, 2), 1.0)

    def test_roulette_selection(self):
        print "ROULETTE SELECTION"

        old_pop_size = len(self.population.individuals)
        self.selection.roulette_wheel_selection(self.population)
        new_pop_size = len(self.population.individuals)

        # assert
        # check for object uniqueness
        individual_ids = []
        for i in self.population.individuals:
            self.assertFalse(id(i) in individual_ids)
            individual_ids.append(id(i))

        self.assertEquals(new_pop_size, old_pop_size)

    def test_tournament_selection(self):
        print "TOURNAMENT SELECTION"

        # tournament selection
        old_pop_size = self.print_population("OLD", self.population)
        self.selection.tournament_selection(self.population)
        new_pop_size = self.print_population("NEW", self.population)

        # assert
        # check for object uniqueness
        individual_ids = []
        for i in self.population.individuals:
            self.assertFalse(id(i) in individual_ids)
            individual_ids.append(id(i))

        self.assertEqual(old_pop_size, new_pop_size)

    def test_elitest_selection(self):
        print "ELITEST SELECTION"

        # elitest selection
        old_pop_size = self.print_population("OLD", self.population)
        self.selection.elitest_selection(self.population)
        new_pop_size = self.print_population("NEW", self.population)

        self.assertEquals(old_pop_size, new_pop_size)

    def test_greedy_over_selection(self):
        print "GREEDY-OVER SELECTION"

        # create population of size 1000
        self.config["max_population"] = 1000
        generator = TreeGenerator(self.config)
        population = generator.init()

        # greedy over selection
        old_pop_size = self.print_population("OLD", population)
        self.selection.greedy_over_selection(population)
        new_pop_size = self.print_population("NEW", population)

        self.assertEquals(old_pop_size, new_pop_size)

    def test_select(self):
        old_pop_size = len(self.population.individuals)
        self.selection.select(self.population)
        new_pop_size = len(self.population.individuals)

        # assert
        # check for object uniqueness
        individual_ids = []
        for i in self.population.individuals:
            self.assertFalse(id(i) in individual_ids)
            individual_ids.append(id(i))

        self.assertEquals(old_pop_size, new_pop_size)


if __name__ == '__main__':
    unittest.main()
