#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeNodeBranch
from playground.tree import TreeParser

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/tree_tests.json")


class TreeNodeTests(unittest.TestCase):
    def setUp(self):
        self.left_node = TreeNode(TreeNodeType.CONSTANT, value=1.0)
        self.left_node_2 = TreeNode(TreeNodeType.CONSTANT, value=1.0)

        self.right_node = TreeNode(TreeNodeType.CONSTANT, value=2.0)
        self.right_node_2 = TreeNode(TreeNodeType.CONSTANT, value=2.0)

        self.binary_node = TreeNode(
            TreeNodeType.BINARY_OP,
            left_branch=self.left_node,
            right_branch=self.right_node
        )

    def test_has_value_node(self):
        # assert left branch
        res = self.binary_node.has_value_node(self.left_node)
        self.assertEquals(res, TreeNodeBranch.LEFT)

        # assert right branch
        res = self.binary_node.has_value_node(self.right_node)
        self.assertEqual(res, TreeNodeBranch.RIGHT)

        # assert fail left branch
        res = self.binary_node.has_value_node(self.left_node_2)
        self.assertFalse(res)

        # assert fail right branch
        res = self.binary_node.has_value_node(self.right_node_2)
        self.assertFalse(res)


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        self.t_parser = TreeParser()
        self.tree = Tree()

        node_x = TreeNode(TreeNodeType.INPUT, name="x")
        node_y = TreeNode(TreeNodeType.INPUT, name="y")
        node_z = TreeNode(TreeNodeType.INPUT, name="z")

        self.tree.input_nodes.append(node_x)
        self.tree.input_nodes.append(node_y)
        self.tree.input_nodes.append(node_z)

    def test_valid(self):
        # assert valid
        res = self.tree.valid(self.config["input_nodes"])
        self.assertTrue(res)

        # assert fail valid
        self.tree.input_nodes.pop()
        res = self.tree.valid(self.config["input_nodes"])
        self.assertFalse(res)

    def test_get_linked_node(self):
        # setup
        del self.tree.input_nodes[:]
        left_node = TreeNode(TreeNodeType.INPUT, name="x")
        right_node = TreeNode(TreeNodeType.INPUT, name="y")
        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=left_node,
            right_branch=right_node
        )
        self.tree.root = add_func
        self.tree.program = self.t_parser.post_order_traverse(self.tree.root)

        # pass test
        linked_node = self.tree.get_linked_node(left_node)
        self.assertTrue(linked_node is add_func)
        linked_node = self.tree.get_linked_node(right_node)
        self.assertTrue(linked_node is add_func)

        # fail test
        random_node = TreeNode(TreeNodeType.INPUT, name="z")
        linked_node = self.tree.get_linked_node(random_node)
        self.assertFalse(linked_node is add_func)


if __name__ == '__main__':
    unittest.main()
