#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.initializer import TreeInitializer
from playground.evaluator import TreeEvaluator
from playground.functions import FunctionRegistry

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/evaluator.json")


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

    def tearDown(self):
        del self.config
        del self.tree_initializer
        del self.functions
        del self.evaluator

    def test_gen_term_node(self):
        row = 0
        node_x = TreeNode(TreeNodeType.INPUT, name="x")
        term_node = self.evaluator._gen_term_node(node_x, row)

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
        self.evaluator.eval_node(term_node_1, stack)
        self.assertEquals(len(stack), 1)
        self.assertTrue(stack[0] is term_node_1)

        # evaluate unary_node
        stack = []
        stack.append(term_node_1)
        self.evaluator.eval_node(unary_node, stack)
        self.assertEquals(len(stack), 1)
        self.assertTrue(stack[0].value == 1.0)

        # evaluate binary_node
        stack = []
        stack.append(term_node_2)
        stack.append(term_node_3)
        self.evaluator.eval_node(binary_node, stack)
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
        res = self.evaluator.eval_program(tree.program, tree.size)

        # assert
        self.assertTrue(res is not None)
        self.assertEquals(round(res, 4), 0.0)

    def test_eval_sub_tree(self):
        # create nodes
        term_node_1 = TreeNode(TreeNodeType.TERM, value=100.0)
        term_node_2 = TreeNode(TreeNodeType.TERM, value=10.0)
        term_node_3 = TreeNode(TreeNodeType.TERM, value=20.0)
        input_node = TreeNode(TreeNodeType.INPUT, name="x")

        div_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="DIV",
            left_branch=term_node_1,
            right_branch=term_node_2
        )

        mul_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="MUL",
            left_branch=term_node_3,
            right_branch=input_node
        )

        root = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=div_func,
            right_branch=mul_func
        )

        # create tree
        tree = Tree()
        tree.root = root
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
        res = self.evaluator.eval_sub_tree(div_func, tree.size)
        self.assertTrue(res is not None)

    def test_evaluate(self):
        population = self.tree_initializer.init()
        population.evaluator = self.evaluator
        population.evaluate_population()

        for individual in population.individuals:
            self.assertTrue(individual.score is not None)
            self.assertTrue(individual.score > 0)


if __name__ == '__main__':
    unittest.main()
