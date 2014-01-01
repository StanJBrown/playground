#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from playground.gp_tree.tree_node import TreeNode
from playground.gp_tree.tree_node import TreeNodeType


class TreeNodeTests(unittest.TestCase):
    def setUp(self):
        self.left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        self.left_node_2 = TreeNode(TreeNodeType.TERM, value=1.0)

        self.right_node = TreeNode(TreeNodeType.TERM, value=2.0)
        self.right_node_2 = TreeNode(TreeNodeType.TERM, value=2.0)

        self.binary_node = TreeNode(
            TreeNodeType.FUNCTION,
            arity=2,
            branches=[self.left_node, self.right_node]
        )

    def test_has_value_node(self):
        # assert left branch
        res = self.binary_node.has_value_node(self.left_node)
        self.assertEquals(res, 0)

        # assert right branch
        res = self.binary_node.has_value_node(self.right_node)
        self.assertEqual(res, 1)

        # assert fail left branch
        res = self.binary_node.has_value_node(self.left_node_2)
        self.assertFalse(res)

        # assert fail right branch
        res = self.binary_node.has_value_node(self.right_node_2)
        self.assertFalse(res)

    def test_equal(self):
        term_node = TreeNode(TreeNodeType.TERM, value=2)

        # assert UNARY_OP node
        unary_node = TreeNode(TreeNodeType.FUNCTION, name="SIN")
        self.assertTrue(unary_node.equals(unary_node))
        self.assertFalse(unary_node.equals(term_node))

        # assert BINARY_OP node
        binary_node = TreeNode(TreeNodeType.FUNCTION, name="ADD")
        self.assertTrue(binary_node.equals(binary_node))
        self.assertFalse(binary_node.equals(term_node))

        # assert TERM node
        term_node_2 = TreeNode(TreeNodeType.TERM, value=1.0)
        self.assertTrue(term_node_2.equals(term_node_2))
        self.assertFalse(term_node_2.equals(term_node))

        # assert INPUT node
        input_node = TreeNode(TreeNodeType.INPUT, name="x")
        self.assertTrue(input_node.equals(input_node))
        self.assertFalse(input_node.equals(term_node))


if __name__ == '__main__':
    unittest.main()
