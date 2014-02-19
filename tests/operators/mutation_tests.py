#!/usr/bin/env python
import os
import sys
import random
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import playground.config as config
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry
from playground.gp.tree.tree import Tree
from playground.gp.tree.tree_node import TreeNode
from playground.gp.tree.tree_node import TreeNodeType
from playground.gp.tree.tree_parser import TreeParser
from playground.ga.bitstr_generator import BitStrGenerator
from playground.operators.mutation import GPTreeMutation
from playground.operators.mutation import GABitStrMutation

# SETTINGS
script_path = os.path.dirname(__file__)
config_file = "../config/mutation.json"
config_path = os.path.normpath(os.path.join(script_path, config_file))


class MutatorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_path)

        self.functions = GPFunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)

        self.tree_parser = TreeParser()
        self.tree_mutation = GPTreeMutation(self.config)

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


class GABitStrMutationTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "max_population": 10,

            "bitstring_generation": {
                "genome_length": 10
            },

            "codons": [
                "0000",
                "0001",
                "0010",
                "0011",
                "0100",
                "0101",
                "0110",
                "0111",
                "1000",
                "1001",
                "1011",
                "1111"
            ]
        }
        generator = BitStrGenerator(self.config)
        self.bitstr = generator.generate_random_bitstr()
        self.mutation = GABitStrMutation(self.config)

    def test_point_mutation(self):
        index = random.randint(0, len(self.bitstr.genome) - 1)

        bitstr_before = list(self.bitstr.genome)
        print "BEFORE MUTATION:", bitstr_before
        print "MUTATION INDEX:", index

        self.mutation.point_mutation(self.bitstr, index)

        bitstr_after = list(self.bitstr.genome)
        print "AFTER MUTATION:", bitstr_after

        # assert
        self.assertFalse(bitstr_before == bitstr_after)

if __name__ == '__main__':
    unittest.main()
