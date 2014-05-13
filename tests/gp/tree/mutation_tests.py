#!/usr/bin/env python2
import os
import sys
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

import playground.config as config
from playground.gp.tree.generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry
from playground.gp.tree import Tree
from playground.gp.tree import TreeNode
from playground.gp.tree import TreeNodeType
from playground.gp.tree.parser import TreeParser
from playground.gp.tree.mutation import TreeMutation


class TreeMutatorTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "tree_generation" : {
                "method" : "GROW_METHOD",
                "initial_max_depth" : 4
            },

            "mutation" : {
                "methods": [
                    "POINT_MUTATION",
                    "HOIST_MUTATION",
                    "SUBTREE_MUTATION",
                    "SHRINK_MUTATION",
                    "EXPAND_MUTATION"
                ],
                "probability": 1.0
            },

            "function_nodes" : [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1},
                {"type": "FUNCTION", "name": "RAD", "arity": 1}
            ],
            "terminal_nodes" : [
                {"type": "CONSTANT", "value": 1.0},
                {"type": "INPUT", "name": "x"}
            ],

            "input_variables" : [
                {"type": "INPUT", "name": "x"}
            ]

        }

        self.functions = GPFunctionRegistry("SYMBOLIC_REGRESSION")
        self.generator = TreeGenerator(self.config)

        self.parser = TreeParser()
        self.mutation = TreeMutation(self.config)

        # create nodes
        left_node = TreeNode(TreeNodeType.CONSTANT, value=1.0)
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
        self.mutated(self.tree, self.mutation.point_mutation)

    def test_hoist_mutation(self):
        print "HOIST MUATION!"
        self.mutated(self.tree, self.mutation.hoist_mutation, 3)

    def test_SUBTREE_MUTATION(self):
        print "SUBTREE MUATION!"
        tree_before = self.build_tree_str(self.tree)
        self.mutation.subtree_mutation(self.tree, 3)
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
        self.mutation.shrink_mutation(self.tree, 3)
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
        self.mutation.expansion_mutation(self.tree, 3)
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
        self.mutation.mutate(self.tree)
        tree_after = self.build_tree_str(self.tree)

        print "----->", self.mutation.method
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
