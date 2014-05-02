#!/usr/bin/env python2.7
import os
import sys
import time
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

import playground.config as config
from playground.gp.tree.tree import Tree
from playground.gp.tree.tree import TreeNode
from playground.gp.tree.tree import TreeNodeType
from playground.gp.tree.tree_generator import TreeGenerator
import playground.gp.tree.tree_evaluation_2 as evaluator


class TreeEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "max_population": 50,

            "tree_generation": {
                "method": "FULL_METHOD",
                "initial_max_depth": 4
            },

            "evaluator": {
                "use_cache": True
            },

            "function_nodes": [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1}
            ],

            "terminal_nodes": [
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

            "input_variables": [
                {"type": "INPUT", "name": "x"}
            ],

            "data_file": "tests/data/sine.dat",

            "response_variable": {"name": "y"}
        }
        config.load_data(self.config)

        self.functions = {
            "ADD": "+",
            "SUB": "-",
            "MUL": "*",
            "DIV": "/",
            "POW": "**",
            "SIN": "math.sin",
            "COS": "math.cos",
            "RAD": "math.radians",
            "LN": "math.ln",
            "LOG": "math.log"
        }
        self.tree_generator = TreeGenerator(self.config)

    def tearDown(self):
        del self.config
        del self.tree_generator
        del self.functions

    def test_generate_eq_function(self):
        # create terminal nodes
        term_node = TreeNode(TreeNodeType.TERM, value=100.0)
        input_node = TreeNode(TreeNodeType.INPUT, name="x")

        # create function nodes
        mul_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="MUL",
            arity=2,
            branches=[input_node, term_node]
        )

        rad_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="RAD",
            arity=1,
            branches=[mul_func]
        )

        sin_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="SIN",
            arity=1,
            branches=[rad_func]
        )

        # create tree
        tree = Tree()
        tree.root = sin_func
        tree.update()

        # generate equation function
        eq_func = evaluator.generate_eq_function(
            tree,
            self.functions,
            self.config
        )

        # assert
        self.assertIsNotNone(eq_func)
        self.assertEquals(round(eq_func(1), 4), 0.9848)

    def test_generate_eq_function_multivars(self):
        # create terminal nodes
        term_node = TreeNode(TreeNodeType.INPUT, name="var2")
        input_node = TreeNode(TreeNodeType.INPUT, name="var1")

        # create function nodes
        div_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="DIV",
            arity=2,
            branches=[input_node, term_node]
        )

        # create tree
        tree = Tree()
        tree.root = div_func
        tree.update()

        # generate equation function
        config = {
            "input_variables": [
                {
                    "type": "INPUT",
                    "name": "var1"
                },
                {
                    "type": "INPUT",
                    "name": "var2"
                }
            ]
        }
        eq_func = evaluator.generate_eq_function(tree, self.functions, config)

        # assert
        self.assertIsNotNone(eq_func)
        self.assertEquals(eq_func(1.0, 2.0), 0.5)

    def test_eval_tree(self):
        # create terminal nodes
        term_node = TreeNode(TreeNodeType.TERM, value=100.0)
        input_node = TreeNode(TreeNodeType.INPUT, name="x")

        # create function nodes
        mul_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="MUL",
            arity=2,
            branches=[input_node, term_node]
        )

        rad_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="RAD",
            arity=1,
            branches=[mul_func]
        )

        sin_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="SIN",
            arity=1,
            branches=[rad_func]
        )

        # create tree
        tree = Tree()
        tree.root = sin_func
        tree.update()

        # evaluate tree
        result = evaluator.eval_tree(tree, self.functions, self.config)
        self.assertEquals(round(result, 7), 0.5000001)

    def test_evaluate(self):
        population = self.tree_generator.init()
        results = []

        start_time = time.time()
        evaluator.evaluate(
            population.individuals,
            self.functions,
            self.config,
            results
        )
        end_time = time.time()
        print("GP run took: %2.2fsecs\n" % (end_time - start_time))

        population.individuals = results

        # assert
        for individual in population.individuals:
            self.assertTrue(individual.score is not None)
            self.assertTrue(individual.score > 0)


if __name__ == "__main__":
    unittest.main()
