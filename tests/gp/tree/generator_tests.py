#!/usr/bin/env python2
import os
import sys
import decimal
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from playground.gp.tree import Tree
from playground.gp.tree import TreeNode
from playground.gp.tree import TreeNodeType
from playground.gp.tree.parser import TreeParser
from playground.gp.tree.generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry

# SETTINGS
cwd = os.path.dirname(__file__)


class TreeGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "max_population": 10,

            "tree_generation": {
                "method": "RAMPED_HALF_AND_HALF_METHOD",
                "initial_max_depth": 3
            },

            "function_nodes": [
                {"type": "FUNCTION", "arity": 2, "name": "ADD"},
                {"type": "FUNCTION", "arity": 2, "name": "SUB"},
                {"type": "FUNCTION", "arity": 2, "name": "MUL"},
                {"type": "FUNCTION", "arity": 2, "name": "DIV"},
                {"type": "FUNCTION", "arity": 1, "name": "COS"},
                {"type": "FUNCTION", "arity": 1, "name": "SIN"}
            ],

            "terminal_nodes": [
                {"type": "CONSTANT", "value": 1.0},
                {"type": "INPUT", "name": "x"},
                {"type": "INPUT", "name": "y"},
                {
                    "type": "RANDOM_CONSTANT",
                    "upper_bound": 10.0,
                    "lower_bound": -10.0,
                    "decimal_places": 1
                }
            ],

            "input_variables": [
                {"name": "x"},
                {"name": "y"}
            ]
        }

        self.functions = GPFunctionRegistry("SYMBOLIC_REGRESSION")
        self.generator = TreeGenerator(self.config)
        self.parser = TreeParser()

    def tearDown(self):
        del self.config
        del self.generator
        del self.parser

    def test_generate_func_node(self):
        for i in range(100):
            tree = Tree()
            node = self.generator.generate_func_node(tree)
            self.assertEquals(node.node_type, TreeNodeType.FUNCTION)

    def test_resolve_random_constant(self):
        upper_bound = 10.0
        lower_bound = -10.0
        decimal_places = 0

        for i in range(100):
            node_details = {
                "type": "RANDOM_CONSTANT",
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "decimal_places": decimal_places
            }
            new_node_details = self.generator.resolve_random_constant(node_details)
            node_type = new_node_details["type"]
            node_value = new_node_details["value"]

            self.assertEquals(node_type, "CONSTANT")
            self.assertTrue(upper_bound >= node_value)
            self.assertTrue(lower_bound <= node_value)
            self.assertEquals(node_value, int(node_value))

        upper_bound = 100.0
        lower_bound = -100.0
        decimal_places = 1

        for i in range(100):
            node_details = {
                "type": "RANDOM_CONSTANT",
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "decimal_places": decimal_places
            }
            new_node_details = self.generator.resolve_random_constant(node_details)
            node_type = new_node_details["type"]
            node_value = new_node_details["value"]

            self.assertEquals(node_type, "CONSTANT")
            self.assertTrue(upper_bound >= node_value)
            self.assertTrue(lower_bound <= node_value)

            node_value = decimal.Decimal(str(node_value))
            node_decimal_places = abs(node_value.as_tuple().exponent)
            self.assertEquals(decimal_places, node_decimal_places)

    def test_generate_term_node(self):
        for i in range(100):
            node = self.generator.generate_term_node()
            self.assertTrue(
                node.node_type == TreeNodeType.CONSTANT or TreeNodeType.INPUT
            )

    def test_full_method(self):
        tests = 1

        for i in xrange(tests):
            tree = self.generator.full_method()

            # asserts
            init_max = self.config["tree_generation"]["initial_max_depth"]
            self.assertEquals(tree.depth, init_max)
            self.assertTrue(tree.size > init_max)

    def test_grow_method(self):
        tests = 1000

        for i in xrange(tests):
            tree = self.generator.grow_method()

            # asserts
            init_max = self.config["tree_generation"]["initial_max_depth"]
            self.assertEquals(tree.depth, init_max)
            self.assertTrue(tree.size > init_max)

    def test_generate_tree_from_dict(self):
        population = self.generator.init()
        tree = population.individuals[0]
        tree_dict = self.parser.tree_to_dict(tree, tree.root)
        tree_generated = self.generator.generate_tree_from_dict(tree_dict)

        program_str = ""
        for i in tree.program:
            if i.name is not None:
                program_str += i.name
            else:
                program_str += str(i.value)

        generated_str = ""
        for i in tree_generated.program:
            if i.name is not None:
                generated_str += i.name
            else:
                generated_str += str(i.value)

        self.assertEquals(program_str, generated_str)

    def test_init(self):
        population = self.generator.init()
        self.assertEquals(len(population.individuals), 10)


if __name__ == '__main__':
    unittest.main()
