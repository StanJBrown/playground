#!/usr/bin/env python
from random import random
from random import sample

from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.initializer import TreeInitializer


class TreeMutation(object):
    def __init__(self, config):
        self.config = config
        self.tree_generator = TreeInitializer(self.config, None)

    def _gen_func_node(self, func_type, name):
        func_node = TreeNode(
            func_type,
            name=name
        )
        return func_node

    def _gen_term_node(self, name, value):
        if name is not None:
            term_node = TreeNode(
                TreeNodeType.TERM,
                name=name,
                value=value
            )
        else:
            term_node = TreeNode(
                TreeNodeType.TERM,
                value=value
            )
        return term_node

    def _gen_input_node(self, name):
        input_node = TreeNode(
            TreeNodeType.INPUT,
            name=name
        )
        return input_node

    def _gen_new_node(self, details):
        if details["type"] == TreeNodeType.UNARY_OP:
            return self._gen_func_node(details["type"], details["name"])
        elif details["type"] == TreeNodeType.BINARY_OP:
            return self._gen_func_node(details["type"], details["name"])
        elif details["type"] == TreeNodeType.TERM:
            name = details.get("name", None)
            value = details.get("value", None)
            return self._gen_term_node(name, value)
        elif details["type"] == TreeNodeType.INPUT:
            return self._gen_input_node(details["name"])

    def _get_new_node(self, node):
        # determine what kind of node it is
        t = node.node_type
        nodes = []
        if t == TreeNodeType.UNARY_OP:
            tmp = list(self.config["function_nodes"])
            tmp = [n for n in tmp if n["type"] == TreeNodeType.UNARY_OP]
            nodes.extend(tmp)
        if t == TreeNodeType.BINARY_OP:
            tmp = list(self.config["function_nodes"])
            tmp = [n for n in tmp if n["type"] == TreeNodeType.BINARY_OP]
            nodes.extend(tmp)
        elif t == TreeNodeType.TERM or t == TreeNodeType.INPUT:
            nodes.extend(self.config["terminal_nodes"])
            nodes.extend(self.config["input_nodes"])

        # check the node and return
        while True:

            # obtain a new node
            new_node_details = sample(nodes, 1)[0]
            new_node = self._gen_new_node(new_node_details)

            if node.equals(new_node) is False:
                return new_node_details

    def point_mutation(self, tree, mutation_index=None):
        # mutate node
        node = sample(tree.program, 1)[0]
        new_node = self._get_new_node(node)

        t = node.node_type
        if t == TreeNodeType.UNARY_OP or t == TreeNodeType.BINARY_OP:
            node.name = new_node["name"]
        elif t == TreeNodeType.TERM or t == TreeNodeType.INPUT:
            node.node_type = new_node["type"]
            node.name = new_node.get("name", None)
            node.value = new_node.get("value", None)

    def hoist_mutation(self, tree, mutation_index=None):
        # new indivdiaul generated from subtree
        new_root = None
        if mutation_index is None:
            new_root = sample(tree.func_nodes, 1)[0]
        else:
            new_root = tree.program[mutation_index]

        tree.root = new_root
        tree.update()

    def subtree_mutation(self, tree, mutation_index=None):
        # subtree exchanged against external random subtree
        func_node = None
        if mutation_index is None:
            func_node = sample(tree.func_nodes, 1)[0]
        else:
            func_node = tree.program[mutation_index]

        sub_tree = self.tree_generator.generate_tree()
        tree.replace_node(func_node, sub_tree.root)
        tree.update()

    def expansion_mutation(self, tree, mutation_index=None):
        # terminal exchanged against external random subtree
        term_node = None
        if mutation_index is None:
            term_node = sample(tree.term_nodes, 1)[0]
        else:
            term_node = tree.program[mutation_index]

        sub_tree = self.tree_generator.generate_tree()
        tree.replace_node(term_node, sub_tree.root)
        tree.update()

    def shrink_mutation(self, tree, mutation_index=None):
        # subtree exchanged against terminal
        func_node = None
        if mutation_index is None:
            func_node = sample(tree.func_nodes, 1)[0]
        else:
            func_node = tree.program[mutation_index]

        term_node = None
        if len(tree.term_nodes) > 0:
            node_details = self._get_new_node(sample(tree.term_nodes, 1)[0])
            term_node = self._gen_new_node(node_details)
        else:
            node_details = self._get_new_node(sample(tree.input_nodes, 1)[0])
            term_node = self._gen_new_node(node_details)

        tree.replace_node(func_node, term_node)
        tree.update()

    def mutate(self, tree):
        method = self.config["mutation"]["method"]
        mutation_prob = self.config["mutation"]["probability"]
        prob = random()

        if mutation_prob >= prob:
            if method == "POINT_MUTATION":
                self.point_mutation(tree)
            else:
                raise RuntimeError("Undefined mutation method!")
