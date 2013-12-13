#!/usr/bin/env python
import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import playground.config as config
from playground.gp_tree.tree import Tree
from playground.gp_tree.tree_node import TreeNode
from playground.gp_tree.tree_node import TreeNodeType
from playground.gp_tree.tree_parser import TreeParser
from playground.gp_tree.tree_generator import TreeGenerator
from playground.functions import FunctionRegistry

# SETTINGS
cwd = os.path.dirname(__file__)
tree_init_config = os.path.join(cwd, "../config/initializer.json")


class TreeGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(tree_init_config)

        self.functions = FunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)

        self.tree_parser = TreeParser()

    def tearDown(self):
        del self.config
        del self.tree_generator
        del self.tree_parser

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
        self.tree_generator._add_input_nodes(tree)
        self.assertTrue(len(tree.input_nodes) == 2)

    def test_full_method(self):
        tests = 1000

        for i in range(tests):
            tree = self.tree_generator.full_method()

            # # func nodes
            # print("FUNCTION NODES!")
            # for func_node in tree.func_nodes:
            #     self.tree_parser._print_node(func_node)

            # # term nodes
            # print("\nTERMINAL NODES!")
            # for term_node in tree.term_nodes:
            #     self.tree_parser._print_node(term_node)

            # program
            # print("\nPROGRAM STACK!")
            # for block in tree.program:
            #     self.tree_parser._print_node(block)

            # # dot graph
            # print("\nDOT GRAPH!")
            # self.tree_parser.print_tree(tree.root)

            # asserts
            self.assertEquals(tree.depth, self.config["max_depth"])
            self.assertTrue(tree.size > self.config["max_depth"])
            self.assertTrue(tree.branches > 0)
            self.assertEquals(tree.open_branches, 0)
            self.assertTrue(
                len(tree.input_nodes) >= len(self.config["input_variables"])
            )

    def test_grow_method(self):
        tests = 1000

        for i in range(tests):
            tree = self.tree_generator.grow_method()

            # # func nodes
            # print("FUNCTION NODES!")
            # for func_node in tree.func_nodes:
            #     self.tree_parser._print_node(func_node)

            # # term nodes
            # print("\nTERMINAL NODES!")
            # for term_node in tree.term_nodes:
            #     self.tree_parser._print_node(term_node)

            # # program
            # print("\nPROGRAM STACK!")
            # for block in tree.program:
            #     self.tree_parser._print_node(block)

            # dot graph
            # print("\nDOT GRAPH!")
            # self.tree_parser.print_tree(tree.root)

            # asserts
            self.assertEquals(tree.depth, self.config["max_depth"])
            self.assertTrue(tree.size > self.config["max_depth"])
            self.assertTrue(tree.branches > 0)
            self.assertEquals(tree.open_branches, 0)
            self.assertTrue(
                len(tree.input_nodes) >= len(self.config["input_variables"])
            )

    def test_generate_tree_from_dict(self):
        population = self.tree_generator.init()
        tree = population.individuals[0]
        tree_dict = self.tree_parser.tree_to_dict(tree, tree.root)
        tree_generated = self.tree_generator.generate_tree_from_dict(tree_dict)

        program_str = ""
        for i in tree.program:
            if i.name is not None:
                program_str += i.name
            else:
                program_str += str(i.value)

        generated_str = ""
        for i in tree_generated.program:
            if i.name is not None:
                generated_str += i.name
            else:
                generated_str += str(i.value)

        self.assertEquals(program_str, generated_str)

    def test_init(self):
        population = self.tree_generator.init()
        self.assertEquals(len(population.individuals), 10)


if __name__ == '__main__':
    unittest.main()
