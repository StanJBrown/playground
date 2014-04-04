#!/usr/bin/env python
from random import randint
from random import random
from random import sample

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

    def random_crossover_index(self, t1, t2):
        i1 = randint(0, len(t1.program) - 1)
        i2 = randint(0, len(t2.program) - 1)

        # keep looping if index points to a tree root
        while (t1.program[i1] is t1.root or t2.program[i2] is t2.root):
            i1 = randint(0, len(t1.program) - 1)
            i2 = randint(0, len(t2.program) - 1)

        return [i1, i2]

    def point_crossover(self, t1, t2, crossover_index=None):
        # get the nodes to swap
        if crossover_index:
            self.index = crossover_index
        else:
            self.index = self.random_crossover_index(t1, t2)

        node_1 = t1.program[self.index[0]]
        node_2 = t2.program[self.index[1]]

        # swap
        t1.replace_node(node_1, node_2)
        t2.replace_node(node_2, node_1)

        self.crossovered = True

    def find_common_regions(self, t1, t2):
        common_region = []
        t1_queue = list(t1.root.branches)
        t2_queue = list(t2.root.branches)

        while len(t1_queue) and len(t2_queue):
            n1 = t1_queue.pop(0)
            n2 = t2_queue.pop(0)

            if n1.is_function() and n2.is_function():
                if n1.arity == n2.arity:
                    common_region.append([n1, n2])

                    for i in range(n1.arity):
                        t1_queue.append(n1.branches[i])
                        t2_queue.append(n2.branches[i])

        return common_region

    def random_common_index(self, common_regions, t1, t2):
        selected_node = sample(common_regions, 1)[0]
        indices = []

        # find index of selected node from tree 1
        index = 0
        for node in t1.program:
            if node is selected_node[0]:
                indices.append(index)
                break
            else:
                index += 1

        # find index of selected node from tree 2
        index = 0
        for node in t2.program:
            if node is selected_node[1]:
                indices.append(index)
                break
            else:
                index += 1

        return indices

    def common_region_point_crossover(self, t1, t2, crossover_index=None):
        common_regions = self.find_common_regions(t1, t2)

        if len(common_regions):
            self.index = self.random_common_index(common_regions, t1, t2)
            self.point_crossover(t1, t2, self.index)

    def crossover(self, t1, t2):
        self.method = self.config["crossover"]["method"]
        self.crossover_probability = self.config["crossover"]["probability"]
        self.random_probability = random()
        self.crossovered = False
        self.before_crossover = []
        self.after_crossover = []

        # record before crossover
        self.before_crossover.append(t1.to_dict()["program"])
        self.before_crossover.append(t2.to_dict()["program"])

        # pre-checks
        if len(t1.func_nodes) < 1 or len(t2.func_nodes) < 1:
            self.random_probability = 1.1  # i.e. do not crossover

        # crossover
        if self.crossover_probability >= self.random_probability:
            if self.method == "POINT_CROSSOVER":
                self.point_crossover(t1, t2)
            elif self.method == "COMMON_REGION_POINT_CROSSOVER":
                self.common_region_point_crossover(t1, t2)
            else:
                raise RuntimeError("Undefined crossover method!")

        # record after crossover
        self.after_crossover.append(t1.to_dict()["program"])
        self.after_crossover.append(t2.to_dict()["program"])

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
