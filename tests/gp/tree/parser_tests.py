#!/usr/bin/env python2
import os
import sys
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

import playground.config as config
from playground.gp.tree import Tree
from playground.gp.tree import TreeNode
from playground.gp.tree import TreeNodeType
from playground.gp.tree.parser import TreeParser
from playground.gp.tree.generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry


class TreeParserTests(unittest.TestCase):
    def setUp(self):
        random.seed(10)

        self.config = {
            "max_population" : 10,

            "tree_generation": {
                "method" : "FULL_METHOD",
                "initial_max_depth" : 4
            },

            "function_nodes" : [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1}
            ],

            "terminal_nodes" : [
                {"type": "CONSTANT", "value": 1.0},
                {"type": "INPUT", "name": "x"},
                {"type": "INPUT", "name": "y"},
                {"type": "INPUT", "name": "z"}
            ],

            "input_variables" : [
                {"name": "x"},
                {"name": "y"},
                {"name": "z"}
            ]
        }

        self.functions = GPFunctionRegistry("SYMBOLIC_REGRESSION")
        self.generator = TreeGenerator(self.config)
        self.parser = TreeParser()

        # create nodes
        left_node = TreeNode(TreeNodeType.CONSTANT, value=1.0)
        right_node = TreeNode(TreeNodeType.CONSTANT, value=2.0)

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
        del self.generator
        del self.parser

    def test_parse_tree(self):
        # self.parser.print_tree(tree.root)
        program = self.parser.parse_tree(self.tree, self.tree.root)
        for i in program:
            if i.name is not None:
                print i.name
            else:
                print i.value

        self.assertEquals(self.tree.size, 5)
        self.assertEquals(self.tree.depth, 2)

        self.assertEquals(len(self.tree.func_nodes), 2)
        self.assertEquals(len(self.tree.term_nodes), 2)
        self.assertEquals(len(self.tree.input_nodes), 0)

    def test_parse_equation(self):
        # self.parser.print_tree(tree.root)
        equation = self.parser.parse_equation(self.tree.root)
        self.assertEquals(equation, "((COS(1.0)) ADD (SIN(2.0)))")

    def test_tree_to_dict(self):
        solution = {
            'program': [
                {'type': 'CONSTANT', 'value': 1.0},
                {'arity': 1, 'type': 'FUNCTION', 'name': 'COS'},
                {'type': 'CONSTANT', 'value': 2.0},
                {'arity': 1, 'type': 'FUNCTION', 'name': 'SIN'},
                {'arity': 2, 'type': 'FUNCTION', 'root': True, 'name': 'ADD'}
            ]
        }
        results = self.parser.tree_to_dict(self.tree, self.tree.root)
        self.assertEquals(results["program"], solution["program"])


if __name__ == '__main__':
    unittest.main()
