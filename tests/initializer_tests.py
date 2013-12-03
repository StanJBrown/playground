#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
from playground.initializer import TreeInitializer
from playground.functions import FunctionRegistry
from playground.evaluator import TreeEvaluator
from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeParser

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/initializer.json")


class InitializerTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        self.t_parser = TreeParser()

    def tearDown(self):
        del self.config
        del self.tree_initializer
        del self.t_parser

    def test_tree_add_input_nodes(self):
        # setup
        # create nodes
        left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node = TreeNode(TreeNodeType.TERM, value=2.0)
        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=left_node,
            right_branch=right_node
        )
        # create tree
        tree = Tree()
        tree.root = add_func
        tree.update_program()
        tree.update_func_nodes()
        tree.update_term_nodes()

        # add input nodes
        self.tree_initializer._add_input_nodes(tree)
        self.assertTrue(len(tree.input_nodes) == 2)

    def test_full_method(self):
        tests = 1000

        for i in range(tests):
            tree = self.tree_initializer.full_method()

            # # func nodes
            # print("FUNCTION NODES!")
            # for func_node in tree.func_nodes:
            #     self.t_parser._print_node(func_node)

            # # term nodes
            # print("\nTERMINAL NODES!")
            # for term_node in tree.term_nodes:
            #     self.t_parser._print_node(term_node)

            # program
            # print("\nPROGRAM STACK!")
            # for block in tree.program:
            #     self.t_parser._print_node(block)

            # # dot graph
            # print("\nDOT GRAPH!")
            # self.t_parser.print_tree(tree.root)

            # asserts
            self.assertEquals(tree.depth, self.config["max_depth"])
            self.assertTrue(tree.size > self.config["max_depth"])
            self.assertTrue(tree.branches > 0)
            self.assertEquals(tree.open_branches, 0)
            self.assertTrue(
                len(tree.input_nodes) >= len(self.config["input_nodes"])
            )

    def test_grow_method(self):
        tests = 1000

        for i in range(tests):
            tree = self.tree_initializer.grow_method()

            # # func nodes
            # print("FUNCTION NODES!")
            # for func_node in tree.func_nodes:
            #     self.t_parser._print_node(func_node)

            # # term nodes
            # print("\nTERMINAL NODES!")
            # for term_node in tree.term_nodes:
            #     self.t_parser._print_node(term_node)

            # # program
            # print("\nPROGRAM STACK!")
            # for block in tree.program:
            #     self.t_parser._print_node(block)

            # dot graph
            # print("\nDOT GRAPH!")
            # self.t_parser.print_tree(tree.root)

            # asserts
            self.assertEquals(tree.depth, self.config["max_depth"])
            self.assertTrue(tree.size > self.config["max_depth"])
            self.assertTrue(tree.branches > 0)
            self.assertEquals(tree.open_branches, 0)
            self.assertTrue(
                len(tree.input_nodes) >= len(self.config["input_nodes"])
            )

    def test_init(self):
        population = self.tree_initializer.init()
        self.assertEquals(len(population.individuals), 10)


if __name__ == '__main__':
    unittest.main()
