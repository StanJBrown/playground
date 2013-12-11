#!/usr/bin/env python
import sys
import os
import time
import copy
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import playground.config as config
import playground.play as play
from playground.tree import TreeInitializer
from playground.tree import TreeEvaluator
from playground.functions import FunctionRegistry
from playground.tree_evaluation import evaluate
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
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        # self.db = DB(self.config)
        # self.db.setup_tables()
        self.db = None

        self.selection = Selection(self.config, recorder=self.db)
        self.crossover = GPTreeCrossover(self.config, recorder=self.db)
        self.mutation = GPTreeMutation(self.config, recorder=self.db)

    def tearDown(self):
        # self.db.purge_tables()

        del self.config

        del self.evaluator
        del self.tree_initializer
        del self.db

        del self.selection
        del self.crossover
        del self.mutation

    def test_reproduce(self):
        tests = 1

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
        population = self.tree_initializer.init()
        pop_1 = copy.deepcopy(population)
        pop_2 = copy.deepcopy(population)

        start_time = time.time()
        p_1 = play.play(
            pop_1,
            self.selection,
            self.crossover,
            self.mutation,
            self.config
        )
        end_time = time.time()
        print("GP run with cache: %2.2fsec\n" % (end_time - start_time))

        # without cache
        self.evaluator.use_cache = True
        self.evaluator.cache = {}
        self.evaluator.matched_cache = 0

        start_time = time.time()
        p_2 = play.play(
            pop_2,
            self.selection,
            self.crossover,
            self.mutation,
            self.config
        )
        end_time = time.time()
        print("GP run without cache: %2.2fsec\n" % (end_time - start_time))

        match = False
        for individual_1 in pop_1.individuals:
            for individual_2 in pop_2.individuals:
                match = individual_1.equals(individual_2)
                if match:
                    print "MATCH: ", str(individual_1), "--", str(individual_2)
                    break
            if match is False:
                print "MISSMATCH: ", str(individual_1), "--", str(individual_2)
                break
        print ""

        print "pop_1"
        for i in p_1.individuals:
            print str(i)

        print "\n\npop_2"
        for i in p_2.individuals:
            print str(i)
#
#     def test_play_multi(self):
#         play.play_multi(
#             self.tree_initializer,
#             self.functions,
#             evaluate,
#             self.selection,
#             self.crossover,
#             self.mutation,
#             self.config
#         )


if __name__ == '__main__':
    unittest.main()
