#!/usr/bin/env python2
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

import playground.config as config
from playground.gp.tree.tree import Tree
from playground.gp.tree.tree import TreeNode
from playground.gp.tree.tree import TreeNodeType
from playground.gp.tree.tree_parser import TreeParser

# SETTINGS
cwd = os.path.dirname(__file__)
tree_config = os.path.join(cwd, "../../config/tree.json")
tree_init_config = os.path.join(cwd, "../../config/initializer.json")
eval_config = os.path.join(cwd, "../../config/evaluator.json")


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


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(tree_config)
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
        res = self.tree.valid(self.config["input_variables"])
        self.assertTrue(res)

        # assert fail valid
        self.tree.input_nodes.pop()
        res = self.tree.valid(self.config["input_variables"])
        self.assertFalse(res)

    def test_get_linked_node(self):
        # setup
        del self.tree.input_nodes[:]
        left_node = TreeNode(TreeNodeType.INPUT, name="x")
        right_node = TreeNode(TreeNodeType.INPUT, name="y")
        add_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[left_node, right_node]
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

    def test_replace_node(self):
        # setup
        node_x = TreeNode(TreeNodeType.INPUT, name="x")
        node_y = TreeNode(TreeNodeType.INPUT, name="y")
        add_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[node_x, node_y]
        )

        # build tree
        tree = Tree()
        tree.root = add_func
        tree.update_program()

        # replace input node
        new_node = TreeNode(TreeNodeType.INPUT, name="z")
        before_replace = list(tree.program)
        tree.replace_node(node_x, new_node)
        after_replace = list(tree.program)

        # assert
        self.assertTrue(before_replace == before_replace)
        self.assertTrue(after_replace == after_replace)
        self.assertFalse(before_replace == after_replace)
        self.assertTrue(add_func.branches[0] is new_node)

    def test_equal(self):
        # create nodes
        left_node_1 = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node_1 = TreeNode(TreeNodeType.TERM, value=2.0)

        left_node_2 = TreeNode(TreeNodeType.TERM, value=3.0)
        right_node_2 = TreeNode(TreeNodeType.TERM, value=4.0)

        cos_func_1 = TreeNode(
            TreeNodeType.FUNCTION,
            name="COS",
            arity=1,
            branches=[left_node_1]
        )
        sin_func_1 = TreeNode(
            TreeNodeType.FUNCTION,
            name="SIN",
            arity=1,
            branches=[right_node_1]
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
        tree_1 = Tree()
        tree_1.root = add_func
        tree_1.update()

        # create tree_2
        tree_2 = Tree()
        tree_2.root = sub_func
        tree_2.update()

        self.assertTrue(tree_1.equals(tree_1))
        self.assertFalse(tree_1.equals(tree_2))
        self.assertTrue(tree_2.equals(tree_2))
        self.assertFalse(tree_2.equals(tree_1))

    def test_str(self):
        # setup
        del self.tree.input_nodes[:]
        left_node = TreeNode(TreeNodeType.INPUT, name="x")
        right_node = TreeNode(TreeNodeType.INPUT, name="y")
        add_func = TreeNode(
            TreeNodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[left_node, right_node]
        )
        self.tree.root = add_func
        self.tree.program = self.t_parser.post_order_traverse(self.tree.root)

        # assert
        self.assertEquals(str(self.tree), "(x ADD y)")


if __name__ == '__main__':
    unittest.main()
