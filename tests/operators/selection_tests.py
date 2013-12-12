#!/usr/bin/env python
import os
import sys
import random
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import playground.config as config
from playground.gp_tree.tree_generator import TreeGenerator
from playground.gp_tree.tree import TreeEvaluator
from playground.functions import FunctionRegistry
from playground.operators.selection import Selection

# SETTINGS
cwd = os.path.dirname(__file__)
config_fp = os.path.normpath(os.path.join(cwd, "../config/selection.json"))


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_generator = TreeGenerator(self.config, self.evaluator)

        self.selection = Selection(self.config)
        self.population = self.tree_generator.init()

        # give population random scores
        for inidividual in self.population.individuals:
            inidividual.score = random.triangular(1, 100)

    def test_normalize_scores(self):
        self.selection._normalize_scores(self.population)

        total_sum = 0
        for individual in self.population.individuals:
            total_sum += individual.score

        self.assertEquals(round(total_sum, 2), 1.0)

    def test_roulette_selection(self):
        new_pop = self.selection.roulette_wheel_selection(self.population)

        old_pop_size = len(self.population.individuals)
        new_pop_size = len(new_pop.individuals)

        self.assertFalse(old_pop_size == new_pop_size)
        self.assertEquals(new_pop_size, old_pop_size / 2)

    def test_tournament_selection(self):
        new_pop = self.selection.tournament_selection(self.population)

        old_pop_size = len(self.population.individuals)
        new_pop_size = len(new_pop.individuals)

        self.assertFalse(old_pop_size == new_pop_size)
        self.assertEquals(new_pop_size, old_pop_size / 2)

    def test_select(self):
        new_pop = self.selection.select(self.population)

        old_pop_size = len(self.population.individuals)
        new_pop_size = len(new_pop.individuals)

        self.assertFalse(old_pop_size == new_pop_size)
        self.assertEquals(new_pop_size, old_pop_size / 2)


if __name__ == '__main__':
    unittest.main()
