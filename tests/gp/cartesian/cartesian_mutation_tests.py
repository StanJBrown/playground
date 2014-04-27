#!/usr/bin/env python
import os
import sys
import copy
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

from playground.gp.cartesian.cartesian import Cartesian
from playground.gp.cartesian.cartesian_mutation import CartesianMutation


class CartesianMutationTests(unittest.TestCase):
    def setUp(self):
        # config and mutation
        self.config = {
            "function_nodes": [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1},
                {"type": "FUNCTION", "name": "RAD", "arity": 1}
            ]
        }
        self.mutator = CartesianMutation(self.config)

        # make cartesian
        self.data = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ]
        self.chromosome = [
            [0, 0, 2],
            [0, 0, 3],
            [3, 4, 5],
            [0, 1, 2],
            [0, 1, 3],
            [2, 5, 7],
            [2, 6, 9],
            [0, 5, 7],
            [2, 11, 8],
            [0, 11, 8]
        ]
        self.output_nodes = [4, 9, 12, 13]
        self.cartesian = Cartesian(
            rows=1,
            cols=14,
            levels_back=0,
            func_nodes=self.chromosome,
            input_nodes=self.data,
            output_nodes=self.output_nodes
        )

    def test_generate_random_gene(self):
        # test function gene
        num_functions = len(self.config["function_nodes"])
        for i in range(100):
            old = random.randint(0,  num_functions - 1)
            res = self.mutator.gen_random_gene("FUNC", old, self.cartesian)

            # asserts
            self.assertTrue(res != old)
            self.assertTrue(res >= 0 and res <= num_functions - 1)

        # test connection gene
        num_nodes = len(self.cartesian.graph)
        for i in range(100):
            old = random.randint(0, num_nodes - 1)
            res = self.mutator.gen_random_gene("CONN", old, self.cartesian)

            # asserts
            self.assertTrue(res != old)
            self.assertTrue(res >= 0 and res <= num_nodes - 1)

    def test_mutate_function_node(self):
        num_input_nodes = len(self.cartesian.input_nodes)
        num_nodes = len(self.cartesian.graph)

        for i in range(100):
            n_addr = random.randint(num_input_nodes, num_nodes - 1)

            # before
            graph_before = copy.deepcopy(self.cartesian.graph)
            # print "BEFORE:", self.cartesian.graph

            # mutate
            g_index = self.mutator.mutate_function_node(n_addr, self.cartesian)

            # after
            graph_after = copy.deepcopy(self.cartesian.graph)
            # print "AFTER:", self.cartesian.graph

            gene_before = graph_before[n_addr][g_index]
            gene_after = graph_after[n_addr][g_index]

            # asserts
            self.assertNotEquals(graph_before, graph_after)
            self.assertNotEquals(gene_before, gene_after)

    def test_mutate_output_node(self):
        num_output_nodes = len(self.cartesian.output_nodes)
        for i in range(100):
            index = random.randint(0, num_output_nodes - 1)
            old_addr = self.cartesian.output_nodes[index]
            new_addr = self.mutator.mutate_output_node(index, self.cartesian)

            self.assertNotEquals(old_addr, new_addr)
            self.assertNotEquals(old_addr, self.cartesian.output_nodes[index])

    def test_point_mutation(self):
        for i in range(100):
            # before
            output_before = copy.deepcopy(self.cartesian.output_nodes)
            graph_before = copy.deepcopy(self.cartesian.graph)
            # print "BEFORE:", graph_before

            # mutate
            self.mutator.point_mutation(self.cartesian)

            # after
            output_after = copy.deepcopy(self.cartesian.output_nodes)
            graph_after = copy.deepcopy(self.cartesian.graph)
            # print "AFTER:", graph_after

            # asserts
            if self.mutator.index["mutated_node"] == "FUNC_NODE":
                self.assertNotEquals(graph_before, graph_after)
            elif self.mutator.index["mutated_node"] == "OUTPUT_NODE":
                index = self.mutator.index["output_node"]
                num_outputs = len(self.cartesian.output_nodes)
                self.assertNotEquals(output_before, output_after)
                self.assertTrue(index >= 0 and index <= num_outputs - 1)


if __name__ == "__main__":
    unittest.main()
