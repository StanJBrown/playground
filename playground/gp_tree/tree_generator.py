#!/usr/bin/env python
from random import sample
from random import random
from random import randint

from playground.gp_tree.tree import Tree
from playground.gp_tree.tree_node import TreeNode
from playground.gp_tree.tree_node import TreeNodeType
from playground.gp_tree.tree_parser import TreeParser
from playground.population import Population


class TreeGenerator(object):
    def __init__(self, config):
        self.config = config
        self.tree_parser = TreeParser()

    def _gen_random_func_node(self, tree):
        index = randint(0, len(self.config["function_nodes"]) - 1)
        node = self.config["function_nodes"][index]
        func_node = TreeNode(node["type"], name=node["name"])

        if node["type"] == TreeNodeType.BINARY_OP:
            tree.branches += 1
            tree.open_branches += 1

        return func_node

    def _gen_random_term_node(self, tree):
        index = randint(0, len(self.config["terminal_nodes"]) - 1)
        node = self.config["terminal_nodes"][index]

        term_node = TreeNode(
            node["type"],
            name=node.get("name", None),
            value=node.get("value", None)
        )
        tree.open_branches -= 1

        return term_node

    def _gen_input_node(self, index):
        node = self.config["input_variables"][index]
        input_node = TreeNode(TreeNodeType.INPUT, name=node.get("name", None))
        return input_node

    def _build_tree(self, node, tree, depth, node_generator):
        if node.node_type == TreeNodeType.UNARY_OP:
            # value
            value_node = node_generator(tree, depth)
            node.value_branch = value_node

            self._build_tree(value_node, tree, depth + 1, node_generator)

        elif node.node_type == TreeNodeType.BINARY_OP:
            # left
            left_node = node_generator(tree, depth)
            node.left_branch = left_node

            self._build_tree(left_node, tree, depth + 1, node_generator)

            # right
            right_node = node_generator(tree, depth)
            node.right_branch = right_node

            self._build_tree(right_node, tree, depth + 1, node_generator)

    def _add_input_nodes(self, tree):
        index = 0
        inputs = len(self.config["input_variables"])
        term_nodes = sample(tree.term_nodes, inputs)

        for term_node in term_nodes:
            input_node = self._gen_input_node(index)

            tree.replace_node(term_node, input_node)

            # increment index
            index += 1
            if index == len(self.config["input_variables"]) - 1:
                index = 0

            # increment inputs modified
            inputs -= 1

    def _full_method_node_gen(self, tree, depth):
        if depth + 1 == self.config["max_depth"]:
                term_node = self._gen_random_term_node(tree)
                tree.term_nodes.append(term_node)
                tree.size += 1
                tree.depth = self.config["max_depth"]
                return term_node
        else:
                func_node = self._gen_random_func_node(tree)
                tree.func_nodes.append(func_node)
                tree.size += 1
                return func_node

    def full_method(self):
        while True:
            # setup
            tree = Tree()
            tree.root = self._gen_random_func_node(tree)

            # build tree
            self._build_tree(tree.root, tree, 0, self._full_method_node_gen)
            tree.update_program()

            # add input nodes
            if len(tree.term_nodes) > len(self.config["input_variables"]):
                self._add_input_nodes(tree)
                return tree

        return tree

    def _grow_method_node_gen(self, tree, depth):
        if depth + 1 == self.config["max_depth"]:
            term_node = self._gen_random_term_node(tree)
            tree.term_nodes.append(term_node)
            tree.size += 1
            tree.depth = self.config["max_depth"]
            return term_node
        else:
            prob = random()
            node = None
            if tree.open_branches == 1:
                node = self._gen_random_func_node(tree)
                tree.func_nodes.append(node)
            elif prob < 0.5:
                node = self._gen_random_func_node(tree)
                tree.func_nodes.append(node)
            else:
                node = self._gen_random_term_node(tree)
                tree.term_nodes.append(node)
            tree.size += 1
            return node

    def grow_method(self):
        while True:
            # setup
            tree = Tree()
            tree.root = self._gen_random_func_node(tree)

            # build tree
            self._build_tree(tree.root, tree, 0, self._grow_method_node_gen)
            tree.update()

            # add input nodes
            if len(tree.term_nodes) > len(self.config["input_variables"]):
                self._add_input_nodes(tree)
                return tree

        return tree

    def generate_tree(self):
        if self.config["tree_init_method"] == "FULL_METHOD":
            tree = self.full_method()
        elif self.config["tree_init_method"] == "GROW_METHOD":
            tree = self.grow_method()
        else:
            raise RuntimeError("Tree init method not defined!")

        return tree

    def init(self):
        population = Population(self.config)

        if self.config["tree_init_method"] == "FULL_METHOD":
            for i in range(self.config["max_population"]):
                tree = self.full_method()
                population.individuals.append(tree)
        elif self.config["tree_init_method"] == "GROW_METHOD":
            for i in range(self.config["max_population"]):
                tree = self.grow_method()
                population.individuals.append(tree)
        else:
            raise RuntimeError("Tree init method not defined!")

        return population
