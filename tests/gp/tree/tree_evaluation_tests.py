##!/usr/bin/env python
import os
import sys
import time
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

import playground.config as config
from playground.gp.tree.tree import Tree
from playground.gp.tree.tree_node import TreeNode
from playground.gp.tree.tree_node import TreeNodeType
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry
import playground.gp.tree.tree_evaluation as evaluator

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

    def test_gen_term_node(self):
        row = 0
        node_x = TreeNode(TreeNodeType.INPUT, name="x")
        term_node = evaluator.gen_term_node(node_x, row, self.config)

        # asserts
        self.assertEquals(term_node.node_type, TreeNodeType.TERM)
        self.assertEquals(term_node.name, None)
        self.assertEquals(term_node.value, 0.0)

    def test_eval_node(self):
        term_node_1 = TreeNode(TreeNodeType.TERM, value=0.0)
        term_node_2 = TreeNode(TreeNodeType.TERM, value=90.0)
        term_node_3 = TreeNode(TreeNodeType.TERM, value=10.0)
        unary_node = TreeNode(TreeNodeType.FUNCTION, arity=1, name="COS")
        binary_node = TreeNode(TreeNodeType.FUNCTION, arity=2, name="ADD")

        # evaluate term_node
        stack = []
        evaluator.eval_node(term_node_1, stack, self.functions, self.config)
        self.assertEquals(len(stack), 1)
        self.assertTrue(stack[0] is term_node_1)

        # evaluate unary_node
        stack = []
        stack.append(term_node_1)
        evaluator.eval_node(unary_node, stack, self.functions, self.config)
        self.assertEquals(len(stack), 1)
        self.assertTrue(stack[0].value == 1.0)

        # evaluate binary_node
        stack = []
        stack.append(term_node_2)
        stack.append(term_node_3)
        evaluator.eval_node(binary_node, stack, self.functions, self.config)
        self.assertEquals(len(stack), 1)
        self.assertTrue(stack[0].value == 100.0)

    def test_eval_program(self):
        # create nodes
        term_node = TreeNode(TreeNodeType.TERM, value=100.0)
        input_node = TreeNode(TreeNodeType.INPUT, name="x")

        rad_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="RAD",
            arity=1,
            branches=[input_node]
        )

        mul_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="MUL",
            arity=2,
            branches=[rad_func, term_node]
        )

        sin_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="SIN",
            arity=1,
            branches=[mul_func]
        )

        # create tree
        tree = Tree()
        tree.root = sin_func
        tree.update()

        # program
        print("\nPROGRAM STACK!")
        for block in tree.program:
            if block.name is not None:
                print block.name
            else:
                print block.value
        print ""

        # evaluate tree
        res = evaluator.eval_program(
            tree,
            tree.size,
            self.functions,
            self.config,
        )

        # assert
        self.assertTrue(res is not None)
        self.assertEquals(round(res, 4), 0.5)

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
