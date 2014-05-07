#!/usr/bin/env python2
import sys
import os
import time
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import playground.play as play
import playground.config as config
from playground.selection import Selection
from playground.gp.functions import GPFunctionRegistry
import playground.gp.functions as functions
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.tree.tree_evaluation import evaluate
from playground.gp.tree.tree_evaluation import default_stop_func
from playground.gp.tree.tree_evaluation import print_func
from playground.gp.tree.tree_crossover import TreeCrossover
from playground.gp.tree.tree_mutation import TreeMutation

from playground.gp.cartesian.cartesian_generator import CartesianGenerator
import playground.gp.cartesian.cartesian_evaluator as cgp_evaluate
from playground.gp.cartesian.cartesian_mutation import CartesianMutation


# SETTINGS
cwd = os.path.dirname(__file__)
config_fp = os.path.normpath(os.path.join(cwd, "config/play.json"))


class PlayTests(unittest.TestCase):
    def setUp(self):
        random.seed(0)
        self.config = config.load_config(config_fp)
        self.functions = GPFunctionRegistry("SYMBOLIC_REGRESSION")
        self.tree_generator = TreeGenerator(self.config)

        self.selection = Selection(self.config, recorder=None)
        self.crossover = TreeCrossover(self.config, recorder=None)
        self.mutation = TreeMutation(self.config, recorder=None)

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
            #     print i, i.score
            # print "\n"

            self.selection.select(population)

            # print "SELECTION"
            # for i in population.individuals:
            #     print i, i.score
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
            #     print i, i.score

            # assert
            max_pop = self.config["max_population"]
            self.assertEquals(len(population.individuals), max_pop)
            self.assertTrue(population.config is self.config)

    def test_play(self):
        print "PLAY"
        population = self.tree_generator.init()

        # with cache
        start_time = time.time()
        details = play.play_details(
            population=population,
            functions=self.functions,
            evaluate=evaluate,
            selection=self.selection,
            crossover=self.crossover,
            mutation=self.mutation,
            stop_func=default_stop_func,
            print_func=print_func,
            config=self.config,
            recorder=None
        )
        play.play(details)
        end_time = time.time()
        print("GP run with cache: %2.2fsec\n" % (end_time - start_time))
        self.assertEquals(population.generation, 5)

        # without cache
        start_time = time.time()
        details = play.play_details(
            population=population,
            functions=self.functions,
            evaluate=evaluate,
            selection=self.selection,
            crossover=self.crossover,
            mutation=self.mutation,
            stop_func=default_stop_func,
            print_func=print_func,
            config=self.config,
            recorder=None
        )
        play.play(details)
        end_time = time.time()
        print("GP run without cache: %2.2fsec\n" % (end_time - start_time))
        self.assertEquals(population.generation, 10)

        # assert
        self.assertTrue(len(population.individuals) > 0)

    def test_play_multicore(self):
        print "PLAY MULTICORE"
        population = self.tree_generator.init()

        start_time = time.time()
        details = play.play_details(
            population=population,
            functions=self.functions,
            evaluate=evaluate,
            selection=self.selection,
            crossover=self.crossover,
            mutation=self.mutation,
            stop_func=default_stop_func,
            print_func=print_func,
            config=self.config,
            recorder=None
        )
        play.play_multicore(details)
        end_time = time.time()
        print("GP run without cache: %2.2fsec\n" % (end_time - start_time))
        self.assertEquals(population.generation, 5)

        # assert
        self.assertTrue(len(population.individuals) > 0)

    def test_play_evolution_strategy(self):
        print "EVOLUTION STRATEGY"
        population = self.tree_generator.init()
        self.config["max_population"] = 4

        start_time = time.time()
        details = play.play_details(
            population=population,
            functions=self.functions,
            evaluate=evaluate,
            mutation=self.mutation,
            stop_func=default_stop_func,
            print_func=print_func,
            config=self.config
        )
        play.play_evolution_strategy(details)
        end_time = time.time()
        print("GP run without cache: %2.2fsec\n" % (end_time - start_time))
        self.assertEquals(population.generation, 5)

        # assert
        self.assertTrue(len(population.individuals) >= 1)
        # because 1 or more individual may have evaluation error

    def test_play_evolution_strategy_cgp(self):
        print "EVOLUTION STRATEGY - CGP"
        config = {
            "stale_limit": 10,
            "stop_score": 0,
            "max_population": 4,
            "max_generation": 100,

            "cartesian": {
                "rows": 2,
                "columns": 3,
                "levels_back": 1,

                "num_inputs": 2,
                "num_outputs": 1
            },

            "function_nodes": [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2}
            ],

            "input_variables": [
                {"name": "x"},
                {"name": "1"},
            ],

            "mutation": {
                "methods": [
                    "POINT_MUTATION"
                ],
                "probability": 1.0
            },

            "response_variables" : [{"name": "y"}],

            "data": {
                "x": [1, 2, 3, 4],
                "1": [1, 1, 1, 1],
                "y": [2, 4, 6, 8]
            },

        }
        cgp_functions = [
            functions.add_function,
            functions.sub_function,
            functions.mul_function,
            functions.div_function,
        ]

        generator = CartesianGenerator(config)
        population = generator.init()

        start_time = time.time()
        details = play.play_details(
            population=population,
            functions=cgp_functions,
            evaluate=cgp_evaluate.evaluate,
            mutation=CartesianMutation(config),
            stop_func=cgp_evaluate.default_stop_func,
            print_func=cgp_evaluate.print_func,
            config=config
        )
        play.play_evolution_strategy(details)
        end_time = time.time()
        print("GP run without cache: %2.2fsec\n" % (end_time - start_time))

        # assert
        generation = population.generation
        individuals = population.individuals
        self.assertTrue(generation <= config["max_generation"])
        self.assertEquals(len(individuals), config["max_population"])


if __name__ == "__main__":
    unittest.main()
