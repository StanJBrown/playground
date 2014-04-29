#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

from playground.gp.cartesian.cartesian import Cartesian
from playground.gp.cartesian.cartesian_evaluator import CartesianEvaluator


class CartesianDecoderTests(unittest.TestCase):
    def setUp(self):
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
            columns=14,
            levels_back=0,
            func_nodes=self.chromosome,
            input_nodes=self.data,
            output_nodes=self.output_nodes
        )

        self.evaluator = CartesianEvaluator()

    def tearDown(self):
        pass

    def test_decode(self):
        output = self.evaluator.evaluate(self.cartesian)
        self.assertIsNotNone(output)


if __name__ == "__main__":
    unittest.main()
