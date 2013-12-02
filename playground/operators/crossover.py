#1/usr/bin/env python
from random import random
from random import sample


class TreeCrossover(object):
    def __init__(self, config):
        self.config = config

    def point_crossover(self, tree_1, tree_2, crossover_index=None):
        # get the nodes to swap
        func_node_1 = sample(tree_1.func_nodes, 1)[0]
        func_node_2 = sample(tree_2.func_nodes, 1)[0]

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
