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
from playground.gp.tree.generator import TreeGenerator
from playground.gp.tree.evaluation import evaluate
from playground.gp.tree.evaluation import print_func
from playground.gp.tree.evaluation import default_stop_func
from playground.gp.tree.crossover import TreeCrossover
from playground.gp.tree.mutation import TreeMutation

from playground.gp.cartesian.generator import CartesianGenerator
import playground.gp.cartesian.evaluator as cgp_evaluate
from playground.gp.cartesian.mutation import CartesianMutation


# SETTINGS
cwd = os.path.dirname(__file__)
config_fp = os.path.normpath(os.path.join(cwd, "config/play.json"))


class PlayTests(unittest.TestCase):
    def setUp(self):
        random.seed(0)
        self.config = {
            "max_population" : 20,
            "max_generation" : 5,

            "tree_generation" : {
                "method" : "GROW_METHOD",
                "initial_max_depth" : 4
            },

            "evaluator": {
                "use_cache" : True
            },

            "selection" : {
                "method" : "TOURNAMENT_SELECTION",
                "tournament_size": 2
            },

            "crossover" : {
                "method" : "POINT_CROSSOVER",
                "probability" : 0.8
            },

            "mutation" : {
                "methods": [
                    "POINT_MUTATION",
                    "HOIST_MUTATION",
                    "SUBTREE_MUTATION",
                    "SHRINK_MUTATION",
                    "EXPAND_MUTATION"
                ],
                "probability" : 1.0
            },

            "function_nodes" : [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1},
                {"type": "FUNCTION", "name": "RAD", "arity": 1}
            ],

            "terminal_nodes" : [
                {"type": "TERM", "value": 1.0},
                {"type": "TERM", "value": 2.0},
                {"type": "TERM", "value": 2.0},
                {"type": "TERM", "value": 3.0},
                {"type": "TERM", "value": 4.0},
                {"type": "TERM", "value": 5.0},
                {"type": "TERM", "value": 6.0},
                {"type": "TERM", "value": 7.0},
                {"type": "TERM", "value": 8.0},
                {"type": "TERM", "value": 9.0},
                {"type": "TERM", "value": 10.0}
            ],

            "input_variables" : [
                {"type": "INPUT", "name": "x"}
            ],

            "data_file" : "tests/data/sine.dat",

            "response_variables" : [{"name": "y"}]
        }
        config.load_data(self.config)
        self.functions = GPFunctionRegistry("SYMBOLIC_REGRESSION")
        self.generator = TreeGenerator(self.config)

        self.selection = Selection(self.config, recorder=None)
        self.crossover = TreeCrossover(self.config, recorder=None)
        self.mutation = TreeMutation(self.config, recorder=None)

    def tearDown(self):
        del self.config

        del self.generator

        del self.selection
        del self.crossover
        del self.mutation

    def test_reproduce(self):
        tests = 1

        for i in range(tests):
            population = self.generator.init()

            res = []
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
            play_details = play.play_details(
                population=population,
                selection=self.selection,
                crossover=self.crossover,
                mutation=self.mutation,
                evaluate=None,
                config=self.config
            )
            play.play_ga_reproduce(play_details)

            # print "REPRODUCE"
            # for i in population.individuals:
            #     print i, i.score

            # assert
            max_pop = self.config["max_population"]
            self.assertEquals(len(population.individuals), max_pop)
            self.assertTrue(population.config is self.config)

    # def test_play(self):
    #     print "PLAY"
    #     population = self.generator.init()

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
    #     self.assertEquals(population.generation, 5)

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
    #     self.assertEquals(population.generation, 10)

    #     # assert
    #     self.assertTrue(len(population.individuals) > 0)

    # def test_play_multicore(self):
    #     print "PLAY MULTICORE"
    #     population = self.generator.init()

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
    #     self.assertEquals(population.generation, 5)

    #     # assert
    #     self.assertTrue(len(population.individuals) > 0)

    # def test_play_evolution_strategy(self):
    #     print "EVOLUTION STRATEGY"
    #     population = self.generator.init()
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
    #     self.assertEquals(population.generation, 5)

    #     # assert
    #     self.assertTrue(len(population.individuals) >= 1)
    #     # because 1 or more individual may have evaluation error

    # def test_play_evolution_strategy_cgp(self):
    #     print "EVOLUTION STRATEGY - CGP"
    #     config = {
    #         "stale_limit": 10,
    #         "stop_score": 0,
    #         "max_population": 4,
    #         "max_generation": 100,

    #         "cartesian": {
    #             "rows": 2,
    #             "columns": 3,
    #             "levels_back": 1,

    #             "num_inputs": 2,
    #             "num_outputs": 1
    #         },

    #         "function_nodes": [
    #             {"type": "FUNCTION", "name": "ADD", "arity": 2},
    #             {"type": "FUNCTION", "name": "SUB", "arity": 2},
    #             {"type": "FUNCTION", "name": "MUL", "arity": 2},
    #             {"type": "FUNCTION", "name": "DIV", "arity": 2}
    #         ],

    #         "input_variables": [
    #             {"name": "x"},
    #             {"name": "1"},
    #         ],

    #         "mutation": {
    #             "methods": [
    #                 "POINT_MUTATION"
    #             ],
    #             "probability": 1.0
    #         },

    #         "response_variables" : [{"name": "y"}],

    #         "data": {
    #             "x": [1, 2, 3, 4],
    #             "1": [1, 1, 1, 1],
    #             "y": [2, 4, 6, 8]
    #         },

    #     }
    #     cgp_functions = [
    #         functions.add_function,
    #         functions.sub_function,
    #         functions.mul_function,
    #         functions.div_function,
    #     ]

    #     generator = CartesianGenerator(config)
    #     population = generator.init()

    #     start_time = time.time()
    #     details = play.play_details(
    #         population=population,
    #         functions=cgp_functions,
    #         evaluate=cgp_evaluate.evaluate,
    #         mutation=CartesianMutation(config),
    #         stop_func=cgp_evaluate.default_stop_func,
    #         print_func=cgp_evaluate.print_func,
    #         config=config
    #     )
    #     play.play_evolution_strategy(details)
    #     end_time = time.time()
    #     print("GP run without cache: %2.2fsec\n" % (end_time - start_time))

    #     # assert
    #     generation = population.generation
    #     individuals = population.individuals
    #     self.assertTrue(generation <= config["max_generation"])
    #     self.assertEquals(len(individuals), config["max_population"])


if __name__ == "__main__":
    unittest.main()
