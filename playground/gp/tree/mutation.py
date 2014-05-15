#!/usr/bin/env python2
from random import random
from random import sample
from random import randint

from playground.gp.tree import TreeNode
from playground.gp.tree import NodeType
from playground.gp.tree.generator import TreeGenerator
from playground.recorder.record_type import RecordType


class TreeMutation(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.recorder = kwargs.get("recorder", None)
        self.generator = TreeGenerator(self.config)

        # mutation stats
        self.method = None
        self.index = None
        self.mutation_probability = None
        self.random_probability = None
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

    def _gen_new_node(self, details):
        if details is None:
            return None

        elif details["type"] == NodeType.FUNCTION:
            return TreeNode(
                NodeType.FUNCTION,
                name=details["name"],
                arity=details["arity"],
                branches=[]
            )

        elif details["type"] == NodeType.INPUT:
            return TreeNode(
                NodeType.INPUT,
                name=details["name"]
            )

        elif details["type"] == NodeType.CONSTANT:
            return TreeNode(
                NodeType.CONSTANT,
                name=details.get("name", None),
                value=details["value"]
            )
        elif details["type"] == NodeType.RANDOM_CONSTANT:
            resolved_details = self.resolve_random_constant(details)
            return TreeNode(
                NodeType.CONSTANT,
                name=resolved_details.get("name", None),
                value=resolved_details["value"]
            )

    def _get_new_node(self, node):
        # determine what kind of node it is
        node_pool = []
        if node.is_function():
            tmp = list(self.config["function_nodes"])
            tmp = [n for n in tmp if n["arity"] == node.arity]
            node_pool.extend(tmp)
        elif node.is_terminal():
            node_pool.extend(self.config["terminal_nodes"])

        # check the node and return
        retry = 0
        retry_limit = 5
        while True:
            if retry == retry_limit:
                return None
            else:
                retry += 1

            n_details = sample(node_pool, 1)[0]
            if n_details["type"] == NodeType.RANDOM_CONSTANT:
                n_details = self.generator.resolve_random_constant(n_details)
            new_node = self._gen_new_node(n_details)

            if node.equals(new_node) is False:
                return n_details

    def point_mutation(self, tree, mutation_index=None):
        # mutate node
        self.index = randint(0, len(tree.program) - 1)
        node = tree.program[self.index]
        new_node = self._get_new_node(node)

        if new_node is None:
            return

        elif node.is_function():
            node.name = new_node["name"]

        elif node.is_terminal():
            node.node_type = new_node.get("type")
            node.name = new_node.get("name", None)
            node.value = new_node.get("value", None)

        tree.update()
        self.mutated = True

    def hoist_mutation(self, tree, mutation_index=None):
        # new indivdiaul generated from subtree
        node = None
        if mutation_index is None:
            self.index = randint(0, len(tree.program) - 2)
            node = tree.program[self.index]
        else:
            self.index = mutation_index
            node = tree.program[mutation_index]

        tree.root = node
        tree.update()
        self.mutated = True

    def subtree_mutation(self, tree, mutation_index=None):
        # subtree exchanged against external random subtree
        node = None
        if mutation_index is None:
            self.index = randint(0, len(tree.program) - 1)
            node = tree.program[self.index]
        else:
            self.index = mutation_index
            node = tree.program[mutation_index]

        self.generator.max_depth = randint(1, 3)
        sub_tree = self.generator.generate_tree()
        if node is not tree.root:
            tree.replace_node(node, sub_tree.root)
        else:
            tree.root = sub_tree.root
        tree.update()
        self.mutated = True

    def shrink_mutation(self, tree, mutation_index=None):
        # replace subtree with terminal
        if len(tree.func_nodes):
            node = None
            if mutation_index is None:
                self.index = randint(0, len(tree.func_nodes) - 1)
                node = tree.func_nodes[self.index]

                while node is tree.root:
                    self.index = randint(0, len(tree.func_nodes) - 1)
                    node = tree.func_nodes[self.index]
            else:
                self.index = mutation_index
                node = tree.program[mutation_index]

            candidate_nodes = tree.term_nodes
            candidate_nodes.extend(tree.input_nodes)
            new_node_detail = sample(candidate_nodes, 1)[0]
            node_details = self._get_new_node(new_node_detail)
            new_node = self._gen_new_node(node_details)

            if new_node:
                tree.replace_node(node, new_node)
                tree.update()
                self.mutated = True

    def expansion_mutation(self, tree, mutation_index=None):
        # terminal exchanged against external random subtree
        node = None
        if mutation_index is None:
            prob = random()

            if tree.size == 1:
                return

            elif prob > 0.5 and len(tree.term_nodes) > 0:
                self.index = randint(0, len(tree.term_nodes) - 1)
                node = tree.term_nodes[self.index]

            elif prob < 0.5 and len(tree.input_nodes) > 0:
                self.index = randint(0, len(tree.input_nodes) - 1)
                node = tree.input_nodes[self.index]

            elif len(tree.term_nodes) > 0:
                self.index = randint(0, len(tree.term_nodes) - 1)
                node = tree.term_nodes[self.index]

            elif len(tree.input_nodes) > 0:
                self.index = randint(0, len(tree.input_nodes) - 1)
                node = tree.input_nodes[self.index]

        else:
            self.index = mutation_index
            node = tree.program[mutation_index]

        sub_tree = self.generator.generate_tree()
        tree.replace_node(node, sub_tree.root)
        tree.update()
        self.mutated = True

    def mutate(self, tree):
        mutation_methods = {
            "POINT_MUTATION": self.point_mutation,
            "HOIST_MUTATION": self.hoist_mutation,
            "SUBTREE_MUTATION": self.subtree_mutation,
            "SHRINK_MUTATION": self.shrink_mutation,
            "EXPAND_MUTATION": self.expansion_mutation
        }

        self.method = sample(self.config["mutation"]["methods"], 1)[0]
        self.index = None
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

        # record after mutation
        self.after_mutation = tree.to_dict()["program"]

        # record
        if self.recorder is not None:
            self.recorder.record(RecordType.MUTATION, self)

    def to_dict(self):
        self_dict = {
            "method": self.method,
            "mutation_index": self.index,
            "mutation_probability": self.mutation_probability,
            "random_probability": self.random_probability,
            "mutated": self.mutated,
            "before_mutation": self.before_mutation,
            "after_mutation": self.after_mutation
        }

        return self_dict
