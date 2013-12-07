#!/usr/bin/env python
from random import randint
from random import random

from playground.recorder.record_type import RecordType


class GPTreeCrossover(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.recorder = kwargs.get("recorder", None)

        self.method = None
        self.index = None
        self.crossover_probability = None
        self.random_probability = None
        self.crossovered = False

    def _symetric_crossover_index(self, tree_1, tree_2):
        t_1_len = len(tree_1.func_nodes)
        t_2_len = len(tree_2.func_nodes)

        start = 0
        end = 0
        if t_1_len > t_2_len:
            end = t_2_len - 1
        else:
            end = t_1_len - 1

        return randint(start, end)

    def point_crossover(self, tree_1, tree_2, crossover_index=None):
        # get the nodes to swap
        index = self._symetric_crossover_index(tree_1, tree_2)
        func_node_1 = tree_1.func_nodes[index]
        func_node_2 = tree_2.func_nodes[index]

        # swap
        tree_1.replace_node(func_node_1, func_node_2)
        tree_2.replace_node(func_node_2, func_node_1)

    def crossover(self, tree_1, tree_2):
        self.method = self.config["crossover"]["method"]
        self.crossover_probability = self.config["crossover"]["probability"]
        self.random_probability = random()
        self.crossovered = False

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

        # record
        if self.recorder is not None:
            self.recorder.record(RecordType.CROSSOVER, self)
