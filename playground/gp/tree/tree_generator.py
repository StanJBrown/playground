#!/usr/bin/env python
from random import sample
from random import random
from random import randint

from playground.gp.tree.tree import Tree
from playground.gp.tree.tree_node import TreeNode
from playground.gp.tree.tree_node import TreeNodeType
from playground.gp.tree.tree_parser import TreeParser
from playground.population import Population


class TreeGenerator(object):
    def __init__(self, config):
        self.config = config
        self.tree_gen_config = config["tree_generation"]
        self.tree_parser = TreeParser()

    def _gen_func_node(self, tree, random=True):
        node = None
        if random:
            node = sample(self.config["function_nodes"], 1)[0]

        func_node = TreeNode(
            TreeNodeType.FUNCTION,
            name=node["name"],
            arity=node["arity"],
            branches=[]
        )
        tree.branches += (func_node.arity - 1)
        tree.open_branches += (func_node.arity - 1)

        return func_node

    def _gen_term_node(self, tree, random=True, index=None):
        node = None
        if random:
            node = sample(self.config["terminal_nodes"], 1)[0]
        else:
            node = self.config["terminal_nodes"][index]

        term_node = TreeNode(
            TreeNodeType.TERM,
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
        if node.is_function():
            for i in xrange(node.arity):
                value_node = node_generator(tree, depth)
                node.branches.append(value_node)
                self._build_tree(value_node, tree, depth + 1, node_generator)

    def _add_input_nodes(self, tree, mode="ALL"):
        # determine mode
        inputs = 0
        if mode == "ALL":
            inputs = len(self.config["input_variables"])
        else:
            inputs = randint(0, len(self.config["input_variables"]))

        # add input nodes
        index = 0
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
        if depth + 1 == self.tree_gen_config["initial_max_depth"]:
                term_node = self._gen_term_node(tree)
                tree.term_nodes.append(term_node)
                tree.size += 1
                tree.depth = self.tree_gen_config["initial_max_depth"]
                return term_node
        else:
                func_node = self._gen_func_node(tree)
                tree.func_nodes.append(func_node)
                tree.size += 1
                return func_node

    def full_method(self, input_nodes=True):
        while True:
            # setup
            tree = Tree()
            tree.root = self._gen_func_node(tree)

            # build tree
            self._build_tree(tree.root, tree, 0, self._full_method_node_gen)
            tree.update_program()

            # add input nodes
            if input_nodes:
                if len(tree.term_nodes) > len(self.config["input_variables"]):
                    self._add_input_nodes(tree)
                    return tree

        return tree

    def _grow_method_node_gen(self, tree, depth):
        if depth + 1 == self.tree_gen_config["initial_max_depth"]:
            term_node = self._gen_term_node(tree)
            tree.term_nodes.append(term_node)
            tree.size += 1
            tree.depth = self.tree_gen_config["initial_max_depth"]
            return term_node
        else:
            prob = random()
            node = None
            if tree.open_branches == 1:
                node = self._gen_func_node(tree)
                tree.func_nodes.append(node)
            elif prob < 0.5:
                node = self._gen_func_node(tree)
                tree.func_nodes.append(node)
            else:
                node = self._gen_term_node(tree)
                tree.term_nodes.append(node)
            tree.size += 1
            return node

    def grow_method(self, input_nodes=True):
        while True:
            # setup
            tree = Tree()
            tree.root = self._gen_func_node(tree)

            # build tree
            self._build_tree(tree.root, tree, 0, self._grow_method_node_gen)
            tree.update()

            # add input nodes
            if input_nodes:
                if len(tree.term_nodes) > len(self.config["input_variables"]):
                    self._add_input_nodes(tree)
                    return tree

        return tree

    def generate_tree(self):
        if self.tree_gen_config["method"] == "FULL_METHOD":
            tree = self.full_method()
        elif self.tree_gen_config["method"] == "GROW_METHOD":
            tree = self.grow_method()
        else:
            raise RuntimeError("Tree init method not defined!")

        return tree

    def generate_tree_from_dict(self, tree_dict):
        tree = Tree()
        stack = []

        tree.tree_id = tree_dict["id"]
        for node_dict in tree_dict["program"]:
            n_type = node_dict["type"]
            node = None

            if n_type == TreeNodeType.INPUT:
                node = TreeNode(
                    TreeNodeType.INPUT,
                    name=node_dict.get("name", None)
                )

                tree.program.append(node)
                stack.append(node)

            elif n_type == TreeNodeType.TERM:
                node = TreeNode(
                    TreeNodeType.TERM,
                    name=node_dict.get("name", None),
                    value=node_dict.get("value", None)
                )

                tree.program.append(node)
                stack.append(node)

            elif n_type == TreeNodeType.FUNCTION:
                value_nodes = []
                for i in xrange(node_dict["arity"]):
                    value_nodes.append(stack.pop())

                node = TreeNode(
                    TreeNodeType.FUNCTION,
                    name=node_dict["name"],
                    arity=node_dict["arity"],
                    branches=value_nodes
                )

                tree.program.append(node)
                stack.append(node)

                if node_dict.get("root", False):
                    tree.root = node

        return tree

    def init(self):
        population = Population(self.config)

        if self.tree_gen_config["method"] == "FULL_METHOD":
            for i in xrange(self.config["max_population"]):
                tree = self.full_method()
                population.individuals.append(tree)
        elif self.tree_gen_config["method"] == "GROW_METHOD":
            for i in xrange(self.config["max_population"]):
                tree = self.grow_method()
                population.individuals.append(tree)
        else:
            raise RuntimeError("Tree init method not defined!")

        return population
