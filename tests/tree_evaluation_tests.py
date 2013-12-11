##!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import playground.config as config
from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeInitializer
from playground.functions import FunctionRegistry
import playground.tree_evaluation as evaluator

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/evaluator.json")


class TreeEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)

        self.functions = FunctionRegistry()
        self.tree_initializer = TreeInitializer(self.config, None)

    def tearDown(self):
        del self.config
        del self.tree_initializer
        del self.functions

    def test_gen_term_node(self):
        row = 0
        node_x = TreeNode(TreeNodeType.INPUT, name="x")
        term_node = evaluator.gen_term_node(node_x, row, self.config)

        # asserts
        self.assertEquals(term_node.node_type, TreeNodeType.TERM)
        self.assertEquals(term_node.name, None)
        self.assertEquals(term_node.value, 10.0)

    def test_eval_node(self):
        term_node_1 = TreeNode(TreeNodeType.TERM, value=0.0)
        term_node_2 = TreeNode(TreeNodeType.TERM, value=90.0)
        term_node_3 = TreeNode(TreeNodeType.TERM, value=10.0)
        unary_node = TreeNode(TreeNodeType.UNARY_OP, name="COS")
        binary_node = TreeNode(TreeNodeType.BINARY_OP, name="ADD")

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
            TreeNodeType.UNARY_OP,
            name="RAD",
            value_branch=input_node
        )

        mul_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="MUL",
            left_branch=rad_func,
            right_branch=term_node
        )

        sin_func = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=mul_func
        )

        # create tree
        tree = Tree()
        tree.root = sin_func
        tree.update_program()
        tree.update_func_nodes()
        tree.update_term_nodes()

        # program
        print("\nPROGRAM STACK!")
        for block in tree.program:
            if block.name is not None:
                print block.name
            else:
                print block.value
        print ""

        # evaluate tree
        results = {}
        res = evaluator.eval_program(
            tree,
            tree.size,
            self.functions,
            self.config,
            results
        )

        # assert
        self.assertTrue(res)
        self.assertEquals(round(results[str(id(tree))], 4), 0.0)

    def test_evaluate(self):
        population = self.tree_initializer.init()
        cache = {}
        results = {}

        evaluator.evaluate(
            population.individuals,
            self.functions,
            self.config,
            cache,
            results
        )

        # write results back to individuals
        bad_eggs = 0
        for individual in list(population.individuals):
            exists_in_results = str(id(individual)) in results
            not_none = results.get(str(id(individual)), None) is not None

            if exists_in_results and not_none:
                individual.score = results[str(id(individual))]
            else:
                population.individuals.remove(individual)
                bad_eggs += 1

        # assert
        for individual in population.individuals:
            self.assertTrue(individual.score is not None)
            self.assertTrue(individual.score > 0)


if __name__ == "__main__":
    unittest.main()
