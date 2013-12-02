#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
import playground.data_loader as data
import playground.play as play
from playground.initializer import TreeInitializer
from playground.evaluator import TreeEvaluator
from playground.functions import FunctionRegistry
from playground.operators.selection import Selection
from playground.operators.crossover import TreeCrossover
from playground.operators.mutation import TreeMutation

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/play.json")


class PlayTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        data.load_data(self.config)

        functions = FunctionRegistry()
        self.tree_evaluator = TreeEvaluator(self.config, functions)
        self.tree_initializer = TreeInitializer(self.config)

        self.selection = Selection(self.config)
        self.crossover = TreeCrossover(self.config)
        self.mutation = TreeMutation(self.config)

    def tearDown(self):
        del self.config

        del self.tree_evaluator
        del self.tree_initializer

        del self.selection
        del self.crossover
        del self.mutation

    def test_reproduce(self):
        population = self.tree_initializer.init()
        population.evaluator = self.tree_evaluator
        population.evaluate_population()
        population = self.selection.select(population)

        print("len before reproduction: " + str(len(population.individuals)))
        play.reproduce(population, self.crossover, self.mutation, self.config)
        print("len after reproduce: " + str(len(population.individuals)))

        max_pop = self.config["max_population"]
        self.assertEquals(len(population.individuals), max_pop)

    def test_play(self):
        print ""
        # functions = FunctionRegistry()
        # tree_evaluator = TreeEvaluator(self.config, self.functions)

if __name__ == '__main__':
    unittest.main()
