#!/usr/bin/env python
import sys
import os
# import copy
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import playground.config as config
from playground.initializer import TreeInitializer
from playground.functions import FunctionRegistry
from playground.evaluator import TreeEvaluator
from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeParser
from playground.operators.crossover import GPTreeCrossover

# SETTINGS
config_fp = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../config/crossover.json")
)


class GPTreeCrossoverTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        self.crossover = GPTreeCrossover(self.config)
        self.tree_parser = TreeParser()

        # create nodes
        left_node_1 = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node_1 = TreeNode(TreeNodeType.TERM, value=2.0)

        left_node_2 = TreeNode(TreeNodeType.TERM, value=3.0)
        right_node_2 = TreeNode(TreeNodeType.TERM, value=4.0)

        cos_func_1 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="COS",
            value_branch=left_node_1,
        )
        sin_func_1 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=right_node_1,
        )

        cos_func_2 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="COS",
            value_branch=left_node_2,
        )
        sin_func_2 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=right_node_2,
        )

        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=cos_func_1,
            right_branch=sin_func_1
        )

        sub_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="SUB",
            left_branch=sin_func_2,
            right_branch=cos_func_2
        )

        # create tree_1
        self.tree_1 = Tree()
        self.tree_1.root = add_func
        self.tree_1.update_program()
        self.tree_1.update_func_nodes()
        self.tree_1.update_term_nodes()
        self.tree_initializer._add_input_nodes(self.tree_1)

        # create tree_2
        self.tree_2 = Tree()
        self.tree_2.root = sub_func
        self.tree_2.update_program()
        self.tree_2.update_func_nodes()
        self.tree_2.update_term_nodes()
        self.tree_initializer._add_input_nodes(self.tree_2)

    def tearDown(self):
        del self.config
        del self.tree_initializer
        del self.tree_parser

    def build_tree_str(self, tree):
        tree_str = ""

        for node in tree.program:
            if hasattr(node, "name") and node.name is not None:
                tree_str += "node:{0} addr:{1}\n".format(node.name, id(node))
            else:
                tree_str += "node:{0} addr:{1}\n".format(node.value, id(node))

        return tree_str

    def tree_equals(self, tree_1_str, tree_2_str):
        if tree_1_str == tree_2_str:
            return True
        else:
            return False

    def test_point_crossover(self):
        # record before crossover
        tree_1_before = self.build_tree_str(self.tree_1)
        tree_2_before = self.build_tree_str(self.tree_2)

        # point crossover
        self.crossover.point_crossover(self.tree_1, self.tree_2)

        # record after crossover
        tree_1_after = self.build_tree_str(self.tree_1)
        tree_2_after = self.build_tree_str(self.tree_2)

        print("Before Crossover")
        print("\nTree 1")
        print(tree_1_before)
        print("\nTree 2")
        print(tree_2_before)

        print("\nAfter Crossover")
        print("\nTree 1")
        print(tree_1_after)
        print("\nTree 2")
        print(tree_2_after)

        # asserts
        self.assertTrue(self.tree_equals(tree_1_before, tree_1_before))
        self.assertTrue(self.tree_equals(tree_2_before, tree_2_before))
        self.assertTrue(self.tree_equals(tree_1_after, tree_1_after))
        self.assertTrue(self.tree_equals(tree_2_after, tree_2_after))

        self.assertFalse(self.tree_equals(tree_1_before, tree_1_after))
        self.assertFalse(self.tree_equals(tree_2_before, tree_2_after))

    def test_crossover(self):
        # record before crossover
        tree_1_before = self.build_tree_str(self.tree_1)
        tree_2_before = self.build_tree_str(self.tree_2)

        # point crossover
        self.crossover.crossover(self.tree_1, self.tree_2)

        # record after crossover
        tree_1_after = self.build_tree_str(self.tree_1)
        tree_2_after = self.build_tree_str(self.tree_2)

        print("Before Crossover")
        print("\nTree 1!")
        print(tree_1_before)
        print("\nTree 2!")
        print(tree_2_before)

        print("\nAfter Crossover")
        print("\nTree 1!")
        print(tree_1_after)
        print("\nTree 2!")
        print(tree_2_after)

        # asserts
        self.assertTrue(self.tree_equals(tree_1_before, tree_1_before))
        self.assertTrue(self.tree_equals(tree_2_before, tree_2_before))
        self.assertTrue(self.tree_equals(tree_1_after, tree_1_after))
        self.assertTrue(self.tree_equals(tree_2_after, tree_2_after))

        self.assertFalse(self.tree_equals(tree_1_before, tree_1_after))
        self.assertFalse(self.tree_equals(tree_2_before, tree_2_after))


if __name__ == '__main__':
    unittest.main()
