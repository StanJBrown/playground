#!/usr/bin/env python
import sys
import os
import time
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import playground.config as config
import playground.play as play
from playground.gp_tree.tree_generator import TreeGenerator
from playground.gp_tree.tree_evaluation import evaluate
from playground.functions import FunctionRegistry
# from playground.recorder.db import DB
from playground.operators.selection import Selection
from playground.operators.crossover import GPTreeCrossover
from playground.operators.mutation import GPTreeMutation

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/play.json")


class PlayTests(unittest.TestCase):
    def setUp(self):
        random.seed(10)

        self.config = config.load_config(config_fp)
        self.functions = FunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)

        # self.db = DB(self.config)
        # self.db.setup_tables()
        self.db = None

        self.selection = Selection(self.config, recorder=self.db)
        self.crossover = GPTreeCrossover(self.config, recorder=self.db)
        self.mutation = GPTreeMutation(self.config, recorder=self.db)

    def tearDown(self):
        # self.db.purge_tables()

        del self.config

        del self.tree_generator
        del self.db

        del self.selection
        del self.crossover
        del self.mutation

    def test_reproduce(self):
        tests = 1

        for i in range(tests):
            res = []

            population = self.tree_generator.init()
            evaluate(population.individuals, self.functions, self.config, res)
            population.individuals = res
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
            self.assertEquals(population.generation, 0)

    def test_play(self):
        population = self.tree_generator.init()

        # with cache
        start_time = time.time()
        play.play(
            population,
            self.functions,
            evaluate,
            self.selection,
            self.crossover,
            self.mutation,
            self.config
        )
        end_time = time.time()
        print("GP run with cache: %2.2fsec\n" % (end_time - start_time))

        # without cache
        start_time = time.time()
        play.play(
            population,
            self.functions,
            evaluate,
            self.selection,
            self.crossover,
            self.mutation,
            self.config
        )
        end_time = time.time()
        print("GP run without cache: %2.2fsec\n" % (end_time - start_time))

    def test_play_multicore(self):
        population = self.tree_generator.init()

        start_time = time.time()
        play.play_multicore(
            population,
            self.functions,
            evaluate,
            self.selection,
            self.crossover,
            self.mutation,
            self.config
        )
        end_time = time.time()
        print("GP run without cache: %2.2fsec\n" % (end_time - start_time))


if __name__ == '__main__':
    unittest.main()
