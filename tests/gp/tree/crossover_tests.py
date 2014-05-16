#!/usr/bin/env python2
import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

from playground.gp.tree import Tree
from playground.gp.tree import Node
from playground.gp.tree import NodeType
from playground.gp.tree.parser import TreeParser
from playground.gp.tree.generator import TreeGenerator
from playground.gp.tree.crossover import TreeCrossover
from playground.gp.functions import GPFunctionRegistry

# SETTINGS
script_path = os.path.dirname(__file__)
config_file = "../../config/crossover.json"
config_path = os.path.normpath(os.path.join(script_path, config_file))


class TreeCrossoverTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "tree_generation": {
                "initial_max_depth": 4
            },

            "crossover": {
                "method": "POINT_CROSSOVER",
                "probability": 1.0
            },

            "function_nodes": [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1},
                {"type": "FUNCTION", "name": "RAD", "arity": 1}
            ],

            "terminal_nodes": [
                {"type": "CONSTANT", "value": 1.0},
                {"type": "CONSTANT", "value": 2.0},
                {"type": "CONSTANT", "value": 2.0},
                {"type": "CONSTANT", "value": 3.0},
                {"type": "CONSTANT", "value": 4.0},
                {"type": "CONSTANT", "value": 5.0},
                {"type": "CONSTANT", "value": 6.0},
                {"type": "CONSTANT", "value": 7.0},
                {"type": "CONSTANT", "value": 8.0},
                {"type": "CONSTANT", "value": 9.0},
                {"type": "CONSTANT", "value": 10.0}
            ],

            "input_variables": [
                {"type": "INPUT", "name": "x"}
            ]
        }

        self.functions = GPFunctionRegistry("SYMBOLIC_REGRESSION")
        self.generator = TreeGenerator(self.config)

        self.crossover = TreeCrossover(self.config)
        self.parser = TreeParser()

        # create nodes
        left_node_1 = Node(NodeType.INPUT, name="x")
        right_node_1 = Node(NodeType.CONSTANT, value=2.0)
        node = Node(NodeType.CONSTANT, value=2.0)

        left_node_2 = Node(NodeType.CONSTANT, value=3.0)
        right_node_2 = Node(NodeType.CONSTANT, value=4.0)

        cos_func_1 = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[left_node_1, right_node_1]
        )

        sin_func_1 = Node(
            NodeType.FUNCTION,
            name="SIN",
            arity=1,
            branches=[node]
        )

        cos_func_2 = Node(
            NodeType.FUNCTION,
            name="COS",
            arity=1,
            branches=[left_node_2]
        )
        sin_func_2 = Node(
            NodeType.FUNCTION,
            name="SIN",
            arity=1,
            branches=[right_node_2]
        )

        add_func = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[cos_func_1, sin_func_1]
        )

        sub_func = Node(
            NodeType.FUNCTION,
            name="SUB",
            arity=2,
            branches=[sin_func_2, cos_func_2]
        )

        # create tree_1
        self.tree_1 = Tree()
        self.tree_1.root = add_func
        self.tree_1.update()

        print self.tree_1

        # create tree_2
        self.tree_2 = Tree()
        self.tree_2.root = sub_func
        self.tree_2.update()

    def tearDown(self):
        del self.config
        del self.generator
        del self.parser

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

    def test_common_region_point_crossover(self):
        # record before crossover
        tree_1_before = self.build_tree_str(self.tree_1)
        tree_2_before = self.build_tree_str(self.tree_2)

        # point crossover
        self.crossover.common_region_point_crossover(self.tree_1, self.tree_2)

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
    # random.seed(0)
    unittest.main()
