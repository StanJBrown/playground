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
from playground.operators.mutation import TreeMutation

# SETTINGS
config_fp = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../config/crossover.json")
)


class MutatorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        self.tree_initializer = TreeInitializer(self.config)
        self.tree_parser = TreeParser()
        self.tree_mutation = TreeMutation(self.config)

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
        self.tree_initializer._add_input_nodes(self.tree)

    def tearDown(self):
        del self.config
        del self.tree_initializer
        del self.tree_parser

    def test_point_mutation(self):
        tree_before = copy.deepcopy(self.tree)
        self.tree_mutation.point_mutation(self.tree)
        tree_after = copy.deepcopy(self.tree)

        print("Before Mutation")
        self.tree_parser.print_tree(tree_before.root)
        print("\n")

        print("After Mutation")
        self.tree_parser.print_tree(tree_after.root)

        self.assertTrue(tree_before.equals(tree_before))
        self.assertTrue(tree_after.equals(tree_after))
        self.assertFalse(tree_before.equals(tree_after))


if __name__ == '__main__':
    unittest.main()
