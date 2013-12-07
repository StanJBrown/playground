#!/usr/bin/env python
import sys
import os
import time
import random
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
import playground.data_loader as data
import playground.play as play
from playground.initializer import TreeInitializer
from playground.evaluator import TreeEvaluator
from playground.functions import FunctionRegistry
from playground.db.db_adaptor import DBAdaptor
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
        self.evaluator = TreeEvaluator(self.config, functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        self.db = DBAdaptor(self.config)
        self.db.setup_tables()

        self.selection = Selection(self.config, recorder=self.db)
        self.crossover = TreeCrossover(self.config, recorder=self.db)
        self.mutation = TreeMutation(self.config, recorder=self.db)

    def tearDown(self):
        del self.config

        del self.evaluator
        del self.tree_initializer

        del self.selection
        del self.crossover
        del self.mutation

    def test_reproduce(self):
        tests = 10

        for i in range(tests):
            population = self.tree_initializer.init()
            population.evaluate_population()
            population = self.selection.select(population)

            # reproduce
            play.reproduce(
                population,
                self.crossover,
                self.mutation,
                self.config
            )

            # assert
            max_pop = self.config["max_population"]
            self.assertEquals(len(population.individuals), max_pop)
            self.assertTrue(population.config is self.config)
            self.assertTrue(population.evaluator is self.evaluator)
            self.assertEquals(population.generation, 0)

    def test_play(self):
        random.seed(10)

        start_time = time.time()
        play.play(
            self.tree_initializer,
            self.selection,
            self.crossover,
            self.mutation,
            self.config
        )
        end_time = time.time()
        print("With cache: %2.2fsec\n" % (end_time - start_time))

        # without cache
        self.evaluator.use_cache = False
        self.evaluator.cache = {}
        self.evaluator.matched_cache = 0

        start_time = time.time()
        play.play(
            self.tree_initializer,
            self.selection,
            self.crossover,
            self.mutation,
            self.config
        )
        end_time = time.time()
        print("Without cache: %2.2fsec\n" % (end_time - start_time))

if __name__ == '__main__':
    unittest.main()
