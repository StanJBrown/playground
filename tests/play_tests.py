#!/usr/bin/env python
import sys
import os
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import playground.config as config
import playground.play as play
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.tree.tree_evaluation import evaluate
from playground.gp.functions import GPFunctionRegistry
from playground.operators.selection import Selection
from playground.operators.crossover import GPTreeCrossover
from playground.operators.mutation import GPTreeMutation

# SETTINGS
cwd = os.path.dirname(__file__)
config_fp = os.path.normpath(os.path.join(cwd, "config/play.json"))


class PlayTests(unittest.TestCase):
    def setUp(self):
        # random.seed(10)

        self.config = config.load_config(config_fp)
        self.functions = GPFunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)

        self.selection = Selection(self.config, recorder=None)
        self.crossover = GPTreeCrossover(self.config, recorder=None)
        self.mutation = GPTreeMutation(self.config, recorder=None)

    def tearDown(self):
        del self.config

        del self.tree_generator

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

            # print "POPULATION"
            # for i in population.individuals:
            #     print i
            # print "\n"

            population = self.selection.select(population)

            # print "SELECTION"
            # for i in population.individuals:
            #     print i
            # print "\n"

            # reproduce
            play.reproduce(
                population,
                self.crossover,
                self.mutation,
                self.config
            )

            # print "REPRODUCE"
            # for i in population.individuals:
            #     print i

            # assert
            max_pop = self.config["max_population"]
            self.assertEquals(len(population.individuals), max_pop)
            self.assertTrue(population.config is self.config)
            self.assertEquals(population.generation, 0)

    # def test_play(self):
    #     population = self.tree_generator.init()

    #     # with cache
    #     start_time = time.time()
    #     details = play.play_details(
    #         population=population,
    #         functions=self.functions,
    #         evaluate=evaluate,
    #         selection=self.selection,
    #         crossover=self.crossover,
    #         mutation=self.mutation,
    #         stop_func=default_stop_func,
    #         print_func=print_func,
    #         config=self.config,
    #         recorder=None
    #     )
    #     play.play(details)
    #     end_time = time.time()
    #     print("GP run with cache: %2.2fsec\n" % (end_time - start_time))

    #     # without cache
    #     start_time = time.time()
    #     details = play.play_details(
    #         population=population,
    #         functions=self.functions,
    #         evaluate=evaluate,
    #         selection=self.selection,
    #         crossover=self.crossover,
    #         mutation=self.mutation,
    #         stop_func=default_stop_func,
    #         print_func=print_func,
    #         config=self.config,
    #         recorder=None
    #     )
    #     play.play(details)
    #     end_time = time.time()
    #     print("GP run without cache: %2.2fsec\n" % (end_time - start_time))

    #     # assert
    #     self.assertTrue(len(population.individuals) > 0)

    # def test_play_multicore(self):
    #     population = self.tree_generator.init()

    #     start_time = time.time()
    #     details = play.play_details(
    #         population=population,
    #         functions=self.functions,
    #         evaluate=evaluate,
    #         selection=self.selection,
    #         crossover=self.crossover,
    #         mutation=self.mutation,
    #         stop_func=default_stop_func,
    #         print_func=print_func,
    #         config=self.config,
    #         recorder=None
    #     )
    #     play.play_multicore(details)
    #     end_time = time.time()
    #     print("GP run without cache: %2.2fsec\n" % (end_time - start_time))

    #     # assert
    #     self.assertTrue(len(population.individuals) > 0)

    # def test_play_evolution_strategy(self):
    #     population = self.tree_generator.init()
    #     self.config["max_population"] = 4

    #     start_time = time.time()
    #     details = play.play_details(
    #         population=population,
    #         functions=self.functions,
    #         evaluate=evaluate,
    #         mutation=self.mutation,
    #         stop_func=default_stop_func,
    #         print_func=print_func,
    #         config=self.config
    #     )
    #     play.play_evolution_strategy(details)
    #     end_time = time.time()
    #     print("GP run without cache: %2.2fsec\n" % (end_time - start_time))

    #     # assert
    #     self.assertTrue(len(population.individuals) > 1)
    #     # because 1 or more individual may have evaluation error


if __name__ == "__main__":
    unittest.main()
