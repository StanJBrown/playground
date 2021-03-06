#!/usr/bin/env python2
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

import playground.gp.tree.editor as editor
from playground.gp.functions import GPFunctionRegistry
from playground.gp.tree import Tree
from playground.gp.tree import Node
from playground.gp.tree import NodeType


class TreeEditorTests(unittest.TestCase):
    def setUp(self):
        self.functions = GPFunctionRegistry("SYMBOLIC_REGRESSION")

        term_node_1 = Node(NodeType.CONSTANT, value=0.0)
        term_node_2 = Node(NodeType.CONSTANT, value=1.0)
        func_node_1 = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[term_node_1, term_node_2]
        )

        term_node_3 = Node(NodeType.CONSTANT, value=2.0)
        term_node_4 = Node(NodeType.INPUT, name="x")
        func_node_2 = Node(
            NodeType.FUNCTION,
            name="MUL",
            arity=2,
            branches=[term_node_3, term_node_4]
        )

        self.tree = Node(
            NodeType.FUNCTION,
            name="DIV",
            arity=2,
            branches=[func_node_1, func_node_2]
        )

    def print_tree(self, node):
        if node is not None:
            if node.is_function():
                for child in node.branches:
                    self.print_tree(child)

            print node

    def test_analyze_children_terminals_only(self):
        term_node_1 = Node(NodeType.CONSTANT, value=0.0)
        term_node_2 = Node(NodeType.CONSTANT, value=1.0)
        func_node = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[term_node_1, term_node_2]
        )

        result = editor.analyze_children(func_node)
        self.assertEquals(result, (True, False, False, True))

    def test_analyze_children_inputs_and_terminals(self):
        term_node_1 = Node(NodeType.INPUT, name="x")
        term_node_2 = Node(NodeType.CONSTANT, value=1.0)
        func_node = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[term_node_1, term_node_2]
        )

        result = editor.analyze_children(func_node)
        self.assertEquals(result, (False, True, False, False))

    def test_analyze_children_inputs_only(self):
        term_node_1 = Node(NodeType.INPUT, name="x")
        term_node_2 = Node(NodeType.INPUT, name="y")
        func_node = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[term_node_1, term_node_2]
        )

        result = editor.analyze_children(func_node)
        self.assertEquals(result, (False, False, True, False))

    def test_analyze_children_contains_zero(self):
        term_node_1 = Node(NodeType.CONSTANT, value=0.0)
        term_node_2 = Node(NodeType.CONSTANT, value=1.0)
        func_node = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[term_node_1, term_node_2]
        )

        result = editor.analyze_children(func_node)
        self.assertEquals(result, (True, False, False, True))

    def test_edit_tree_zero_only(self):
        # TEST CONTAINS ZERO
        term_node_1 = Node(NodeType.CONSTANT, value=0.0)
        term_node_2 = Node(NodeType.CONSTANT, value=1.0)
        func_node = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[term_node_1, term_node_2]
        )

        print "BEFORE:", func_node
        tree = Tree()
        tree.root = func_node
        tree.depth = 3
        editor.edit_tree(tree, tree.root, self.functions)
        print "AFTER:", func_node
        print

        self.assertEquals(func_node.value, 1.0)

    def test_edit_tree_terminals_only(self):
        # TEST TERMINALS ONLY
        term_node_1 = Node(NodeType.CONSTANT, value=2.0)
        term_node_2 = Node(NodeType.CONSTANT, value=1.0)
        func_node = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[term_node_1, term_node_2]
        )

        print "BEFORE:", func_node
        tree = Tree()
        tree.root = func_node
        tree.depth = 3
        editor.edit_tree(tree, tree.root, self.functions)
        print "AFTER:", func_node
        print

        self.assertEquals(func_node.value, 3.0)

    def test_edit_tree_inputs_and_terminals(self):
        # TEST INPUTS AND TERMINALS
        term_node_1 = Node(NodeType.CONSTANT, value=2.0)
        term_node_2 = Node(NodeType.INPUT, name="x")
        func_node = Node(
            NodeType.FUNCTION,
            name="ADD",
            arity=2,
            branches=[term_node_1, term_node_2]
        )

        print "BEFORE:", func_node
        tree = Tree()
        tree.root = func_node
        tree.depth = 3
        editor.edit_tree(tree, tree.root, self.functions)
        print "AFTER:", func_node
        print

    def test_edit_tree_prune(self):
        # TEST PRUNE
        term_node_1 = Node(NodeType.CONSTANT, value=0.0)
        term_node_2 = Node(NodeType.INPUT, name="x")
        func_node = Node(
            NodeType.FUNCTION,
            name="MUL",
            arity=2,
            branches=[term_node_1, term_node_2]
        )

        print "BEFORE:", func_node
        tree = Tree()
        tree.root = func_node
        tree.depth = 3
        editor.edit_tree(tree, tree.root, self.functions)
        print "AFTER:", func_node
        print

        self.assertEquals(func_node.node_type, NodeType.CONSTANT)
        self.assertIsNone(func_node.name)
        self.assertEquals(func_node.value, 0)


if __name__ == "__main__":
    unittest.main()
