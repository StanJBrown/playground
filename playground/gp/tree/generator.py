#!/usr/bin/env python2
from random import sample
from random import random
from random import uniform

from playground.gp.tree import Tree
from playground.gp.tree import TreeNode
from playground.gp.tree import NodeType
from playground.gp.tree.parser import TreeParser
from playground.population import Population


class TreeGenerator(object):
    def __init__(self, config):
        self.config = config
        self.gen_config = config["tree_generation"]
        self.max_depth = self.gen_config.get("initial_max_depth", 0)
        self.parser = TreeParser()

    def create_random_constant(self, node_details):
        # generate random floating point
        lower_bound = node_details["lower_bound"]
        upper_bound = node_details["upper_bound"]
        constant = uniform(lower_bound, upper_bound)

        decimal_places = node_details.get("decimal_places", None)
        if decimal_places is not None:
            constant = round(constant, decimal_places)

        return constant

    def resolve_random_constant(self, node_details):
        # pre-check
        node_type = node_details["type"]
        if node_type != NodeType.RANDOM_CONSTANT:
            err = "Invalid NodeType -> [{0}]".format(node_details)
            raise RuntimeError(err)

        # create new node details
        constant = self.create_random_constant(node_details["data_range"])
        new_node_details = {
            "type": NodeType.CONSTANT,
            "value": float(constant)
        }

        return new_node_details

    def resolve_class_function(self, node_details):
        # pre-check
        node_type = node_details["type"]
        if node_type != NodeType.CLASS_FUNCTION:
            err = "Invalid NodeType -> [{0}]".format(node_details)
            raise RuntimeError(err)

        # create new node details
        new_node_details = dict(node_details)
        constant = self.create_random_constant(node_details["data_range"])
        if node_details["data_type"] == "INTEGER":
            new_node_details["value"] = int(constant)

        elif node_details["data_type"] == "FLOAT":
            new_node_details["value"] = float(constant)

        return new_node_details

    def generate_func_node(self, random=True):
        node = None
        if random:
            node = sample(self.config["function_nodes"], 1)[0]

        tree_type = self.gen_config.get("tree_type", "SYMBOLIC_REGRESSION")
        if tree_type == "SYMBOLIC_REGRESSION":
            func_node = TreeNode(
                NodeType.FUNCTION,
                name=node["name"],
                arity=node["arity"],
                branches=[]
            )
        elif tree_type == "CLASSIFICATION_TREE":
            node = self.resolve_class_function(node)
            func_node = TreeNode(
                NodeType.CLASS_FUNCTION,
                name=node["name"],
                class_attribute=node["class_attribute"],
                arity=node["arity"],
                branches=[],
                data_type=node["data_type"],
                value=node["value"]
            )
        else:
            err = "Unrecognised tree generation type"
            raise RuntimeError(err)

        return func_node

    def generate_term_node(self, random=True, index=None):
        node_details = None
        # get random terminal node details
        if random:
            node_details = sample(self.config["terminal_nodes"], 1)[0]
        else:
            node_details = self.config["terminal_nodes"][index]

        # resolve if random constant
        if node_details["type"] == NodeType.RANDOM_CONSTANT:
            node_details = self.resolve_random_constant(node_details)

        term_node = TreeNode(
            node_details["type"],
            name=node_details.get("name", None),
            value=node_details.get("value", None)
        )

        return term_node

    def add_func_node_to_tree(self, tree, parent_node, func_node):
        parent_node.branches.append(func_node)
        tree.func_nodes.append(func_node)
        tree.size += 1

    def add_term_node_to_tree(self, tree, parent_node, term_node):
        parent_node.branches.append(term_node)
        tree.size += 1

        if term_node.is_input():
            tree.input_nodes.append(term_node)
        elif term_node.is_constant():
            tree.term_nodes.append(term_node)
        else:
            err = "Unrecognised node type [{0}]!".format(term_node)
            raise RuntimeError(err)

    def grow_method_build_tree(self, tree, node, depth):
        for branch_index in range(node.arity):
            prob = random()

            if prob > 0.5 or depth + 1 == self.max_depth:
                term_node = self.generate_term_node()
                self.add_term_node_to_tree(tree, node, term_node)

            else:
                func_node = self.generate_func_node()
                self.add_func_node_to_tree(tree, node, func_node)
                self.full_method_build_tree(tree, func_node, depth + 1)

    def grow_method(self):
        # initialize tree
        tree = Tree()
        tree.size = 1
        tree.depth = self.max_depth
        tree.root = self.generate_func_node()

        # build tree via full method
        self.full_method_build_tree(tree, tree.root, 0)
        tree.update()

        return tree

    def full_method_build_tree(self, tree, node, depth):
        for branch_index in range(node.arity):
            # create terminal node
            if depth + 1 == self.max_depth:
                term_node = self.generate_term_node()
                self.add_term_node_to_tree(tree, node, term_node)

            # create function node
            else:
                func_node = self.generate_func_node()
                self.add_func_node_to_tree(tree, node, func_node)
                self.full_method_build_tree(tree, func_node, depth + 1)

    def full_method(self):
        # initialize tree
        tree = Tree()
        tree.size = 1
        tree.depth = self.max_depth
        tree.root = self.generate_func_node()

        # build tree via full method
        self.full_method_build_tree(tree, tree.root, 0)
        tree.update()

        return tree

    def ramped_half_and_half_method(self):
        if random() < 0.5:
            tree = self.grow_method()
        else:
            tree = self.full_method()

        return tree

    def generate_tree(self):
        if self.gen_config["method"] == "FULL_METHOD":
            tree = self.full_method()
        elif self.gen_config["method"] == "GROW_METHOD":
            tree = self.grow_method()
        elif self.gen_config["method"] == "RAMPED_HALF_AND_HALF_METHOD":
            self.max_depth = 2
            tree = self.ramped_half_and_half_method()
        else:
            raise RuntimeError("Tree init method not defined!")

        return tree

    def generate_tree_from_dict(self, tree_dict):
        tree = Tree()
        stack = []

        tree.tree_id = tree_dict["id"]
        for node_dict in tree_dict["program"]:
            node_type = node_dict["type"]
            node = None

            if node_type == NodeType.INPUT:
                node = TreeNode(
                    NodeType.INPUT,
                    name=node_dict.get("name", None)
                )

                tree.program.append(node)
                stack.append(node)

            elif node_type == NodeType.CONSTANT:
                node = TreeNode(
                    NodeType.CONSTANT,
                    name=node_dict.get("name", None),
                    value=node_dict.get("value", None)
                )

                tree.program.append(node)
                stack.append(node)

            elif node_type == NodeType.FUNCTION:
                value_nodes = []
                for i in xrange(node_dict["arity"]):
                    value_nodes.append(stack.pop())

                node = TreeNode(
                    NodeType.FUNCTION,
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
        pop = Population(self.config)
        max_pop = self.config["max_population"]
        methods = {
            "FULL_METHOD": self.full_method,
            "GROW_METHOD": self.grow_method,
            "RAMPED_HALF_AND_HALF_METHOD": self.ramped_half_and_half_method,
        }

        # check if there is a range for depth of trees
        ranges = []
        sizes = []
        range_mode = False
        if self.gen_config.get("depth_ranges", False):
            limit = 0
            range_mode = True
            for depth_range in self.gen_config["depth_ranges"]:
                ranges.append(depth_range["size"])

                limit += max_pop * depth_range["percentage"]
                sizes.append(limit)

            sizes.pop()

        # create trees
        for i in range(max_pop):
            if range_mode:
                if i == 0:
                    self.max_depth = ranges.pop(0)
                if len(sizes) > 0 and i == sizes[0]:
                    self.max_depth = ranges.pop(0)
                    sizes.pop(0)

            gen_method = methods[self.gen_config["method"]]
            pop.individuals.append(gen_method())

        return pop
