#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

from playground.gp.cartesian.cartesian import Cartesian
from playground.gp.cartesian.cartesian_evaluator import evaluate_cartesian
import playground.gp.functions as functions


class CartesianEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "cartesian": {
                "rows": 4,
                "columns": 4,
                "levels_back": 2,

                "num_inputs": 4,
                "num_outputs": 4
            },

            "input_variables": [
                {"name": "a"},
                {"name": "b"},
                {"name": "c"},
                {"name": "d"}
            ],

            "response_variables": [
                {"name": "y"}
            ],

            "data": {
                "a": [1, 2, 3, 4],
                "b": [1, 2, 3, 4],
                "c": [1, 2, 3, 4],
                "d": [1, 2, 3, 4]
            },

        }
        self.functions = [
            functions.add_function,
            functions.sub_function,
            functions.mul_function,
            functions.div_function,
        ]

        self.input_nodes = ["a", "b", "c", "d"]
        self.func_nodes = [
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
            func_nodes=self.func_nodes,
            input_nodes=self.input_nodes,
            output_nodes=self.output_nodes
        )

    def tearDown(self):
        pass

    def test_evaluate_cartesian(self):
        result, outputs = evaluate_cartesian(
            self.cartesian,
            self.functions,
            self.config
        )
        self.assertIsNotNone(result)
        self.assertIsNotNone(outputs)

    # def test_evaluate(self):
    #     output = evaluate_cartesian(self.cartesian, self.config)
    #     self.assertIsNotNone(output)


if __name__ == "__main__":
    unittest.main()
