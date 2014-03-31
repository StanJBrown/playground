#!/usr/bin/env python
import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from playground.gp.tree.tree import Tree
from playground.gp.tree.tree import TreeNode
from playground.gp.tree.tree import TreeNodeType
from playground.gp.tree.tree_parser import TreeParser
from playground.gp.tree.tree_generator import TreeGenerator
from playground.gp.functions import GPFunctionRegistry

# SETTINGS
cwd = os.path.dirname(__file__)


class TreeGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "max_population": 10,

            "tree_generation": {
                "method": "RAMPED_HALF_AND_HALF_METHOD",
                "initial_max_depth": 4
            },

            "function_nodes": [
                {
                    "type": "FUNCTION",
                    "arity": 2,
                    "name": "ADD"
                },
                {
                    "type": "FUNCTION",
                    "arity": 2,
                    "name": "SUB"
                },
                {
                    "type": "FUNCTION",
                    "arity": 2,
                    "name": "MUL"
                },
                {
                    "type": "FUNCTION",
                    "arity": 2,
                    "name": "DIV"
                },
                {
                    "type": "FUNCTION",
                    "arity": 1,
                    "name": "COS"
                },
                {
                    "type": "FUNCTION",
                    "arity": 1,
                    "name": "SIN"
                }
            ],

            "terminal_nodes": [
                {
                    "type": "TERM",
                    "value": 1.0
                },
                {
                    "type": "TERM",
                    "value": 2.0
                },
                {
                    "type": "TERM",
                    "value": 2.0
                },
                {
                    "type": "TERM",
                    "value": 3.0
                },
                {
                    "type": "TERM",
                    "value": 4.0
                },
                {
                    "type": "TERM",
                    "value": 5.0
                },
                {
                    "type": "TERM",
                    "value": 6.0
                },
                {
                    "type": "TERM",
                    "value": 7.0
                },
                {
                    "type": "TERM",
                    "value": 8.0
                },
                {
                    "type": "TERM",
                    "value": 9.0
                },
                {
                    "type": "TERM",
                    "value": 10.0
                }
            ],

            "input_variables": [
                {
                    "name": "x"
                },
                {
                    "name": "y"
                }
            ]
        }

        self.functions = GPFunctionRegistry()
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
            TreeNodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[left_node, right_node]
        )
        # create tree
        tree = Tree()
        tree.root = add_func
        tree.update()

        # add input nodes
        self.tree_generator._add_input_nodes(tree)
        self.assertTrue(len(tree.input_nodes) == 2)

    def test_full_method(self):
        tests = 1000

        for i in xrange(tests):
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
            init_max = self.config["tree_generation"]["initial_max_depth"]
            self.assertEquals(tree.depth, init_max)
            self.assertTrue(tree.size > init_max)
            self.assertTrue(tree.branches > 0)
            self.assertEquals(tree.open_branches, 0)
            self.assertTrue(
                len(tree.input_nodes) >= len(self.config["input_variables"])
            )

    def test_grow_method(self):
        tests = 1000

        for i in xrange(tests):
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
            init_max = self.config["tree_generation"]["initial_max_depth"]
            self.assertEquals(tree.depth, init_max)
            self.assertTrue(tree.size > init_max)
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
