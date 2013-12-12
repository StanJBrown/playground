#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import playground.config as config
from playground.gp_tree.tree import Tree
from playground.gp_tree.tree_node import TreeNode
from playground.gp_tree.tree_node import TreeNodeType
from playground.gp_tree.tree_parser import TreeParser
from playground.gp_tree.tree_generator import TreeGenerator
from playground.functions import FunctionRegistry

# SETTINGS
cwd = os.path.dirname(__file__)
tree_config = os.path.join(cwd, "../config/tree.json")


class TreeParserTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(tree_config)

        self.functions = FunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)
        self.tree_parser = TreeParser()

        # create nodes
        left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node = TreeNode(TreeNodeType.TERM, value=2.0)

        cos_func = TreeNode(
            TreeNodeType.UNARY_OP,
            name="COS",
            value_branch=left_node,
        )
        sin_func = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=right_node,
        )

        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=cos_func,
            right_branch=sin_func
        )

        # create tree
        self.tree = Tree()
        self.tree.root = add_func
        self.tree.update_program()
        self.tree.update_func_nodes()
        self.tree.update_term_nodes()

    def tearDown(self):
        del self.config
        del self.tree_generator
        del self.tree_parser

    def test_parse_tree(self):
        # self.tree_parser.print_tree(tree.root)
        program = self.tree_parser.parse_tree(self.tree, self.tree.root)
        for i in program:
            if i.name is not None:
                print i.name
            else:
                print i.value

        self.assertEquals(self.tree.size, 5)
        self.assertEquals(self.tree.depth, 2)
        self.assertEquals(self.tree.branches, 2)
        self.assertEquals(self.tree.open_branches, 0)

        self.assertEquals(len(self.tree.func_nodes), 2)
        self.assertEquals(len(self.tree.term_nodes), 2)
        self.assertEquals(len(self.tree.input_nodes), 0)

    def test_parse_equation(self):
        # self.tree_parser.print_tree(tree.root)
        equation = self.tree_parser.parse_equation(self.tree.root)
        self.assertEquals(equation, "((cos(1.0)) + (sin(2.0)))")


if __name__ == '__main__':
    unittest.main()
