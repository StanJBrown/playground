#!/usr/bin/env python
from random import random
from random import sample

from playground.gp.tree.tree import TreeNode
from playground.gp.tree.tree import TreeNodeType
from playground.gp.tree.tree_generator import TreeGenerator
from playground.recorder.record_type import RecordType


class TreeMutation(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.recorder = kwargs.get("recorder", None)
        self.tree_generator = TreeGenerator(self.config)

        # mutation stats
        self.method = None
        self.index = None
        self.mutation_probability = None
        self.random_probability = None
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

    def _gen_new_node(self, details):
        if details["type"] == TreeNodeType.FUNCTION:
            return TreeNode(
                TreeNodeType.FUNCTION,
                name=details["name"],
                arity=details["arity"],
                branches=[]
            )

        elif details["type"] == TreeNodeType.INPUT:
            return TreeNode(
                TreeNodeType.INPUT,
                name=details["name"]
            )

        elif details["type"] == TreeNodeType.TERM:
            return TreeNode(
                TreeNodeType.TERM,
                name=details.get("name", None),
                value=details["value"]
            )

    def _get_new_node(self, node):
        # determine what kind of node it is
        nodes = []
        if node.is_function():
            tmp = list(self.config["function_nodes"])
            tmp = [n for n in tmp if n["arity"] == node.arity]
            nodes.extend(tmp)
        elif node.is_terminal() or node.is_input():
            nodes.extend(self.config["terminal_nodes"])
            nodes.extend(self.config["input_variables"])

        # check the node and return
        while True:
            new_node_details = sample(nodes, 1)[0]
            new_node = self._gen_new_node(new_node_details)

            if node.equals(new_node) is False:
                return new_node_details

    def point_mutation(self, tree, mutation_index=None):
        # mutate node
        node = sample(tree.program, 1)[0]
        new_node = self._get_new_node(node)

        if node.is_function():
            node.name = new_node["name"]
        elif node.is_terminal() or node.is_input():
            node.node_type = new_node.get("type")
            node.name = new_node.get("name", None)
            node.value = new_node.get("value", None)

    def hoist_mutation(self, tree, mutation_index=None):
        # new indivdiaul generated from subtree
        node = None
        if mutation_index is None:
            node = sample(tree.program, 1)[0]
        else:
            node = tree.program[mutation_index]

        tree.root = node
        tree.update()

    def subtree_mutation(self, tree, mutation_index=None):
        # subtree exchanged against external random subtree
        node = None
        if mutation_index is None:
            node = sample(tree.program, 1)[0]
            while node is tree.root:
                node = sample(tree.program, 1)[0]
        else:
            node = tree.program[mutation_index]

        sub_tree = self.tree_generator.generate_tree()
        tree.replace_node(node, sub_tree.root)
        tree.update()

    def shrink_mutation(self, tree, mutation_index=None):
        # replace subtree with terminal
        if len(tree.func_nodes):
            node = None
            if mutation_index is None:
                node = sample(tree.func_nodes, 1)[0]
                while node is tree.root:
                    node = sample(tree.func_nodes, 1)[0]
            else:
                node = tree.program[mutation_index]

            candidate_nodes = tree.term_nodes
            candidate_nodes.extend(tree.input_nodes)
            new_node_detail = sample(candidate_nodes, 1)[0]
            node_details = self._get_new_node(new_node_detail)
            new_node = self._gen_new_node(node_details)

            tree.replace_node(node, new_node)
            tree.update()

    def expansion_mutation(self, tree, mutation_index=None):
        # terminal exchanged against external random subtree
        node = None
        if mutation_index is None:
            prob = random()

            if prob > 0.5 and len(tree.term_nodes) > 0:
                node = sample(tree.term_nodes, 1)[0]
            elif prob < 0.5 and len(tree.input_nodes) > 0:
                node = sample(tree.input_nodes, 1)[0]
            elif len(tree.term_nodes) > 0:
                node = sample(tree.term_nodes, 1)[0]
            elif len(tree.input_nodes) > 0:
                node = sample(tree.input_nodes, 1)[0]

        else:
            node = tree.program[mutation_index]

        sub_tree = self.tree_generator.generate_tree()
        tree.replace_node(node, sub_tree.root)
        tree.update()

    def mutate(self, tree):
        mutation_methods = {
            "POINT_MUTATION": self.point_mutation,
            "HOIST_MUTATION": self.hoist_mutation,
            "SUBTREE_MUTATION": self.subtree_mutation,
            "SHRINK_MUTATION": self.shrink_mutation,
            "EXPAND_MUTATION": self.expansion_mutation
        }

        self.method = sample(self.config["mutation"]["methods"], 1)[0]
        self.mutation_probability = self.config["mutation"]["probability"]
        self.random_probability = random()
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

        # record before mutation
        self.before_mutation = tree.to_dict()["program"]

        # mutate
        if self.mutation_probability >= self.random_probability:
            mutation_func = mutation_methods[self.method]
            mutation_func(tree)
            self.mutated = True

        # record after mutation
        self.after_mutation = tree.to_dict()["program"]

        # record
        if self.recorder is not None:
            self.recorder.record(RecordType.MUTATION, self)

    def to_dict(self):
        self_dict = {
            "method": self.method,
            "mutation_probability": self.mutation_probability,
            "random_probability": self.random_probability,
            "mutated": self.mutated,
            "before_mutation": self.before_mutation,
            "after_mutation": self.after_mutation
        }

        return self_dict
