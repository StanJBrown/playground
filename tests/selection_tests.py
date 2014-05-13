#!/usr/bin/env python2
import os
import sys
import random
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from playground.gp.tree.generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry
from playground.selection import Selection


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "max_population" : 10,

            "tree_generation" : {
                "method" : "FULL_METHOD",
                "initial_max_depth" : 3
            },

            "selection" : {
                    "method" : "ROULETTE_SELECTION"
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
                {"type": "CONSTANT", "value": 1.0},
                {"type": "CONSTANT", "value": 2.0},
                {"type": "CONSTANT", "value": 2.0},
                {"type": "CONSTANT", "value": 3.0},
                {"type": "CONSTANT", "value": 4.0},
                {"type": "CONSTANT", "value": 5.0},
                {"type": "CONSTANT", "value": 6.0},
                {"type": "CONSTANT", "value": 7.0},
                {"type": "CONSTANT", "value": 8.0},
                {"type": "CONSTANT", "value": 9.0},
                {"type": "CONSTANT", "value": 10.0}
            ],

            "input_variables" : [
                {"type": "INPUT", "name": "x"}
            ]
        }

        self.functions = GPFunctionRegistry("SYMBOLIC_REGRESSION")
        self.generator = TreeGenerator(self.config)

        self.selection = Selection(self.config)
        self.population = self.generator.init()

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
