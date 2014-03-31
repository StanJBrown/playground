#!/usr/bin/env python
from random import randint
from random import random

from playground.recorder.record_type import RecordType


class TreeCrossover(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.recorder = kwargs.get("recorder", None)

        self.method = None
        self.index = None
        self.crossover_probability = None
        self.random_probability = None
        self.crossovered = False
        self.before_crossover = None
        self.after_crossover = None

    def _crossover_index(self, t1, t2):
        end = min(t1.size, t2.size) - 1
        index = randint(0, end)

        # keep looping if index points to a tree root
        while (t1.program[index] is t1.root or t2.program[index] is t2.root):
            index = randint(0, end)

        return index

    def point_crossover(self, tree_1, tree_2, crossover_index=None):
        # get the nodes to swap
        self.index = self._crossover_index(tree_1, tree_2)
        node_1 = tree_1.program[self.index]
        node_2 = tree_2.program[self.index]

        # swap
        tree_1.replace_node(node_1, node_2)
        tree_2.replace_node(node_2, node_1)

    def crossover(self, tree_1, tree_2):
        self.method = self.config["crossover"]["method"]
        self.crossover_probability = self.config["crossover"]["probability"]
        self.random_probability = random()
        self.crossovered = False
        self.before_crossover = []
        self.after_crossover = []

        # record before crossover
        self.before_crossover.append(tree_1.to_dict()["program"])
        self.before_crossover.append(tree_2.to_dict()["program"])

        # pre-checks
        if len(tree_1.func_nodes) < 1 or len(tree_2.func_nodes) < 1:
            self.random_probability = 1.1  # i.e. do not crossover

        # crossover
        if self.crossover_probability >= self.random_probability:
            if self.method == "POINT_CROSSOVER":
                self.point_crossover(tree_1, tree_2)
                self.crossovered = True
            else:
                raise RuntimeError("Undefined crossover method!")

        # record after crossover
        self.after_crossover.append(tree_1.to_dict()["program"])
        self.after_crossover.append(tree_2.to_dict()["program"])

        # record
        if self.recorder is not None:
            self.recorder.record(RecordType.CROSSOVER, self)

    def to_dict(self):
        self_dict = {
            "method": self.method,
            "index": self.index,
            "crossover_probability": self.crossover_probability,
            "random_probability": self.random_probability,
            "crossovered": self.crossovered,
            "before_crossover": self.before_crossover,
            "after_crossover": self.after_crossover
        }

        return self_dict
