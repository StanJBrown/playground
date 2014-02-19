#!/usr/bin/env python
import os
import sys
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

import playground.config as config
from playground.gp.tree.tree import Tree
from playground.gp.tree.tree_node import TreeNode
from playground.gp.tree.tree_node import TreeNodeType
from playground.gp.tree.tree_parser import TreeParser
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry

# SETTINGS
cwd = os.path.dirname(__file__)
tree_config = os.path.join(cwd, "../../config/tree.json")


class TreeParserTests(unittest.TestCase):
    def setUp(self):
        random.seed(10)

        self.config = config.load_config(tree_config)

        self.functions = GPFunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)
        self.tree_parser = TreeParser()

        # create nodes
        left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node = TreeNode(TreeNodeType.TERM, value=2.0)

        cos_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="COS",
            arity=1,
            branches=[left_node]
        )
        sin_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="SIN",
            arity=1,
            branches=[right_node]
        )

        add_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[cos_func, sin_func]
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

    def test_tree_to_dict(self):
        solution = {
            'program': [
                {'type': 'TERM', 'value': 1.0},
                {'arity': 1, 'type': 'FUNCTION', 'name': 'COS'},
                {'type': 'TERM', 'value': 2.0},
                {'arity': 1, 'type': 'FUNCTION', 'name': 'SIN'},
                {'arity': 2, 'type': 'FUNCTION', 'root': True, 'name': 'ADD'}
            ]
        }
        results = self.tree_parser.tree_to_dict(self.tree, self.tree.root)
        self.assertEquals(results["program"], solution["program"])


if __name__ == '__main__':
    unittest.main()
