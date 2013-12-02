#!/usr/bin/env python
import sys
import os
import copy
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import playground.config as config
from playground.initializer import TreeInitializer
from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeParser
from playground.operators.crossover import TreeCrossover

# SETTINGS
config_fp = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../config/crossover.json")
)


class CrossoverTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        self.tree_initializer = TreeInitializer(self.config)
        self.crossover = TreeCrossover(self.config)
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

    def test_point_crossover(self):
        print("Before Crossover")
        print("\nTree 1!")
        self.tree_parser.print_tree(self.tree_1.root)
        print("\nTree 2!")
        self.tree_parser.print_tree(self.tree_2.root)

        # tree_1_before = copy.deepcopy(self.tree_1)
        # tree_2_before = copy.deepcopy(self.tree_2)
        self.crossover.point_crossover(self.tree_1, self.tree_2)
        # tree_1_after = copy.deepcopy(self.tree_1)
        # tree_2_after = copy.deepcopy(self.tree_2)

        print("After Crossover")
        print("\nTree 1!")
        self.tree_parser.print_tree(self.tree_1.root)
        print("\nTree 2!")
        self.tree_parser.print_tree(self.tree_2.root)

        # asserts
        # self.assertFalse(tree_1_before.equals(tree_1_after))
        # self.assertFalse(tree_2_before.equals(tree_2_after))

    # def test_crossover(self):
    #     print("Before Crossover")
    #     print("\nTree 1!")
    #     self.tree_parser.print_tree(self.tree_1.root)
    #     print("\nTree 2!")
    #     self.tree_parser.print_tree(self.tree_2.root)

    #     tree_1_before = copy.deepcopy(self.tree_1)
    #     tree_2_before = copy.deepcopy(self.tree_2)
    #     self.crossover.crossover(self.tree_1, self.tree_2)
    #     tree_1_after = copy.deepcopy(self.tree_1)
    #     tree_2_after = copy.deepcopy(self.tree_2)

    #     print("After Crossover")
    #     print("\nTree 1!")
    #     self.tree_parser.print_tree(self.tree_1.root)
    #     print("\nTree 2!")
    #     self.tree_parser.print_tree(self.tree_2.root)

    #     # asserts
    #     self.assertFalse(tree_1_before.equals(tree_1_after))
    #     self.assertFalse(tree_2_before.equals(tree_2_after))


if __name__ == '__main__':
    unittest.main()
