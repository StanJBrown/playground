##!/usr/bin/env python
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
from playground.gp.functions import GPFunctionRegistry
import playground.gp.tree.tree_evaluation_2 as evaluator

# SETTINGS
cwd = os.path.dirname(__file__)
config_fp = os.path.join(cwd, "../../config/evaluator.json")


class TreeEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        self.functions = GPFunctionRegistry()
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
        eq_func = evaluator.generate_eq_function(tree)

        # assert
        self.assertIsNotNone(eq_func)
        self.assertEquals(round(eq_func(1), 4), 0.9848)

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
        result = evaluator.eval_tree(tree, self.config)
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
