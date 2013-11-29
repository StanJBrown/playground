#1/usr/bin/env python
from random import randint


class TreeCrossover(object):

    def _symetric_crossover_index(self, tree_1, tree_2):
        t_1_len = len(tree_1.func_nodes)
        t_2_len = len(tree_1.func_nodes)

        start = 0
        end = 0
        if t_1_len > t_2_len:
            end = t_2_len - 1
        else:
            end = t_1_len - 1

        return randint(start, end)

    def one_point_crossover(self, tree_1, tree_2, crossover_index=None):
        # check crossover index
        if crossover_index is None:
            crossover_index = self._symetric_crossover_index(tree_1, tree_2)

        # get the nodes to swap
        func_node_1 = tree_1.func_nodes[crossover_index]
        func_node_2 = tree_2.func_nodes[crossover_index]

        # swap
        tree_1.replace_node(func_node_1, func_node_2)
        tree_2.replace_node(func_node_2, func_node_1)
