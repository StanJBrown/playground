#!/usr/bin/env python
import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

import playground.config as config
from playground.gp.functions import GPFunctionRegistry
from playground.gp.tree.tree import Tree
from playground.gp.tree.tree import TreeNode
from playground.gp.tree.tree import TreeNodeType
from playground.gp.tree.tree_parser import TreeParser
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.tree.tree_crossover import TreeCrossover

# SETTINGS
script_path = os.path.dirname(__file__)
config_file = "../../config/crossover.json"
config_path = os.path.normpath(os.path.join(script_path, config_file))


class TreeCrossoverTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_path)

        self.functions = GPFunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)

        self.crossover = TreeCrossover(self.config)
        self.tree_parser = TreeParser()

        # create nodes
        left_node_1 = TreeNode(TreeNodeType.TERM, name="x")
        right_node_1 = TreeNode(TreeNodeType.TERM, value=2.0)
        node = TreeNode(TreeNodeType.TERM, value=2.0)

        left_node_2 = TreeNode(TreeNodeType.TERM, value=3.0)
        right_node_2 = TreeNode(TreeNodeType.TERM, value=4.0)

        cos_func_1 = TreeNode(
            TreeNodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[left_node_1, right_node_1]
        )

        sin_func_1 = TreeNode(
            TreeNodeType.FUNCTION,
            name="SIN",
            arity=1,
            branches=[node]
        )

        cos_func_2 = TreeNode(
            TreeNodeType.FUNCTION,
            name="COS",
            arity=1,
            branches=[left_node_2]
        )
        sin_func_2 = TreeNode(
            TreeNodeType.FUNCTION,
            name="SIN",
            arity=1,
            branches=[right_node_2]
        )

        add_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[cos_func_1, sin_func_1]
        )

        sub_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="SUB",
            arity=2,
            branches=[sin_func_2, cos_func_2]
        )

        # create tree_1
        self.tree_1 = Tree()
        self.tree_1.root = add_func
        self.tree_1.update()
        self.tree_generator._add_input_nodes(self.tree_1)

        print self.tree_1

        # create tree_2
        self.tree_2 = Tree()
        self.tree_2.root = sub_func
        self.tree_2.update()
        self.tree_generator._add_input_nodes(self.tree_2)

    def tearDown(self):
        del self.config
        del self.tree_generator
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
