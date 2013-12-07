#!/usr/bin/env python
import sys
import os
import copy
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import playground.config as config
from playground.initializer import TreeInitializer
from playground.functions import FunctionRegistry
from playground.evaluator import TreeEvaluator
from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeParser
from playground.operators.mutation import GPTreeMutation

# SETTINGS
config_fp = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../config/mutation.json")
)


class MutatorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        self.tree_parser = TreeParser()
        self.tree_mutation = GPTreeMutation(self.config)

        # create nodes
        left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node = TreeNode(TreeNodeType.INPUT, name="x")

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

    def test_point_mutation(self):
        print "POINT MUATION!"
        tree_before = self.build_tree_str(self.tree)
        self.tree_mutation.point_mutation(self.tree)
        tree_after = self.build_tree_str(self.tree)

        print("Before Mutation")
        print(tree_before)

        print("\nAfter Mutation")
        print(tree_after)

        self.assertTrue(self.tree_equals(tree_before, tree_before))
        self.assertTrue(self.tree_equals(tree_after, tree_after))
        self.assertFalse(self.tree_equals(tree_before, tree_after))

    def test_hoist_mutation(self):
        print "HOIST MUATION!"
        tree_before = self.build_tree_str(self.tree)
        self.tree_mutation.hoist_mutation(self.tree, 3)
        tree_after = self.build_tree_str(self.tree)

        print("Before Mutation")
        print(tree_before)

        print("\nAfter Mutation")
        print(tree_after)

        self.assertTrue(self.tree_equals(tree_before, tree_before))
        self.assertTrue(self.tree_equals(tree_after, tree_after))
        self.assertFalse(self.tree_equals(tree_before, tree_after))

        self.assertEquals(self.tree.size, 2)
        self.assertEquals(self.tree.depth, 1)
        self.assertEquals(self.tree.branches, 1)
        self.assertEquals(self.tree.open_branches, 0)

        self.assertEquals(len(self.tree.func_nodes), 0)
        self.assertEquals(len(self.tree.term_nodes), 0)
        self.assertEquals(len(self.tree.input_nodes), 1)

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

    # def test_mutate(self):
    #     print "MUTATE!"
    #     tree_before = self.build_tree_str(self.tree)
    #     self.tree_mutation.mutate(self.tree)
    #     tree_after = self.build_tree_str(self.tree)

    #     print("Before Mutation")
    #     print(tree_before)

    #     print("\nAfter Mutation")
    #     print(tree_after)

    #     self.assertTrue(self.tree_equals(tree_before, tree_before))
    #     self.assertTrue(self.tree_equals(tree_after, tree_after))
    #     self.assertFalse(self.tree_equals(tree_before, tree_after))


if __name__ == '__main__':
    unittest.main()
