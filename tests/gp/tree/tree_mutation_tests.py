#!/usr/bin/env python
import os
import sys
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

import playground.config as config
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry
from playground.gp.tree.tree import Tree
from playground.gp.tree.tree import TreeNode
from playground.gp.tree.tree import TreeNodeType
from playground.gp.tree.tree_parser import TreeParser
from playground.gp.tree.tree_mutation import TreeMutation


# SETTINGS
script_path = os.path.dirname(__file__)
config_file = "../../config/mutation.json"
config_path = os.path.normpath(os.path.join(script_path, config_file))


class TreeMutatorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_path)

        self.functions = GPFunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)

        self.tree_parser = TreeParser()
        self.tree_mutation = TreeMutation(self.config)

        # create nodes
        left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node = TreeNode(TreeNodeType.INPUT, name="x")

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
        self.tree_generator._add_input_nodes(self.tree)

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

    def mutated(self, tree, mutation_func, mutation_index=None):
        tree_before = self.build_tree_str(self.tree)
        mutation_func(tree, mutation_index)
        tree_after = self.build_tree_str(self.tree)

        print("Before Mutation")
        print(tree_before)

        print("\nAfter Mutation")
        print(tree_after)

        self.assertTrue(self.tree_equals(tree_before, tree_before))
        self.assertTrue(self.tree_equals(tree_after, tree_after))
        self.assertFalse(self.tree_equals(tree_before, tree_after))

    def test_point_mutation(self):
        print "POINT MUATION!"
        self.mutated(self.tree, self.tree_mutation.point_mutation)

    def test_hoist_mutation(self):
        print "HOIST MUATION!"
        self.mutated(self.tree, self.tree_mutation.hoist_mutation, 3)

    def test_subtree_mutation(self):
        print "SUBTREE MUATION!"
        tree_before = self.build_tree_str(self.tree)
        self.tree_mutation.subtree_mutation(self.tree, 3)
        tree_after = self.build_tree_str(self.tree)

        print("Before Mutation")
        print(tree_before)

        print("\nAfter Mutation")
        print(tree_after)

        self.assertTrue(self.tree_equals(tree_before, tree_before))
        self.assertTrue(self.tree_equals(tree_after, tree_after))
        self.assertFalse(self.tree_equals(tree_before, tree_after))

    def test_shrink_mutation(self):
        print "SHRINK MUATION!"
        tree_before = self.build_tree_str(self.tree)
        self.tree_mutation.shrink_mutation(self.tree, 3)
        tree_after = self.build_tree_str(self.tree)

        print("Before Mutation")
        print(tree_before)

        print("\nAfter Mutation")
        print(tree_after)

        self.assertTrue(self.tree_equals(tree_before, tree_before))
        self.assertTrue(self.tree_equals(tree_after, tree_after))
        self.assertFalse(self.tree_equals(tree_before, tree_after))

    def test_expansion_mutation(self):
        print "EXPANSION MUATION!"
        tree_before = self.build_tree_str(self.tree)
        self.tree_mutation.expansion_mutation(self.tree, 3)
        tree_after = self.build_tree_str(self.tree)

        print("Before Mutation")
        print(tree_before)

        print("\nAfter Mutation")
        print(tree_after)

        self.assertTrue(self.tree_equals(tree_before, tree_before))
        self.assertTrue(self.tree_equals(tree_after, tree_after))
        self.assertFalse(self.tree_equals(tree_before, tree_after))

    def test_mutate(self):
        print "MUTATE!"
        tree_before = self.build_tree_str(self.tree)
        self.tree_mutation.mutate(self.tree)
        tree_after = self.build_tree_str(self.tree)

        print("Before Mutation")
        print(tree_before)

        print("\nAfter Mutation")
        print(tree_after)

        self.assertTrue(self.tree_equals(tree_before, tree_before))
        self.assertTrue(self.tree_equals(tree_after, tree_after))
        self.assertFalse(self.tree_equals(tree_before, tree_after))


if __name__ == '__main__':
    random.seed(0)
    unittest.main()
