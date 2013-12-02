#1/usr/bin/env python
from random import randint
from random import random


class TreeCrossover(object):
    def __init__(self, config):
        self.config = config

    def _crossover_index(self, tree_1, tree_2):
        t_1_len = len(tree_1.func_nodes)
        t_2_len = len(tree_1.func_nodes)

        start = 0
        end = 0
        if t_1_len > t_2_len:
            end = t_2_len - 1
        else:
            end = t_1_len - 1

        return randint(start, end)

    def point_crossover(self, tree_1, tree_2, crossover_index=None):
        # get the nodes to swap
        func_node_1 = tree_1.func_nodes[self._crossover_index(tree_1, tree_2)]
        func_node_2 = tree_2.func_nodes[self._crossover_index(tree_1, tree_2)]

        # swap
        tree_1.replace_node(func_node_1, func_node_2)
        tree_2.replace_node(func_node_2, func_node_1)

    def crossover(self, tree_1, tree_2):
        method = self.config["crossover"]["method"]
        crossover_prob = self.config["crossover"]["probability"]
        prob = random()

        if crossover_prob >= prob:
            if method == "POINT_CROSSOVER":
                self.point_crossover(tree_1, tree_2)
            else:
                raise RuntimeError("Undefined crossover method!")
