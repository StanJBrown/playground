#!/usr/bin/env python2.7
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

from playground.gp.cartesian.cartesian import Cartesian
from playground.gp.cartesian.cartesian_evaluator import evaluate_cartesian
import playground.gp.functions as functions

from playground.config import load_data


class CartesianEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "cartesian": {
                "rows": 1,
                "columns": 4,
                "levels_back": 4,

                "num_inputs": 12,
                "num_outputs": 1
            },

            "input_variables": [
                {"type": "INPUT", "name": "x"},
                {"type": "CONSTANT", "name": "0.0"},
                {"type": "CONSTANT", "name": "1.0"},
                {"type": "CONSTANT", "name": "2.0"},
                {"type": "CONSTANT", "name": "3.0"},
                {"type": "CONSTANT", "name": "4.0"},
                {"type": "CONSTANT", "name": "5.0"},
                {"type": "CONSTANT", "name": "6.0"},
                {"type": "CONSTANT", "name": "7.0"},
                {"type": "CONSTANT", "name": "8.0"},
                {"type": "CONSTANT", "name": "9.0"},
                {"type": "CONSTANT", "name": "10.0"}
            ],

            "function_nodes": [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "SIN", "arity": 1},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "RAD", "arity": 1}
            ],

            "response_variable": {
                "name": "y"
            },

            "response_variables": [
                {"name": "y"}
            ],

            "data_file": "../../data/sine.dat",

        }
        script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        load_data(self.config, script_path)

        # add constants
        rows = len(self.config["data"]["y"])
        for i in range(11):
            i = float(i)
            self.config["data"][str(i) + ".0"] = [i for j in range(rows)]

        self.functions = [
            functions.add_function,
            functions.sub_function,
            functions.mul_function,
            functions.div_function,
            functions.sin_function,
            functions.cos_function,
            functions.rad_function
        ]

        self.input_nodes = [
            "x",
            "0.0", "1.0", "2.0", "3.0", "4.0", "5.0",
            "6.0", "7.0", "8.0", "9.0", "10.0"
        ]
        self.func_nodes = [
            [2, 11, 11],    # 12
            [6, 0],         # 13
            [2, 12, 13],    # 14
            [4, 14],        # 15
        ]
        self.output_nodes = [15]

        self.cartesian = Cartesian(
            config={},
            rows=1,
            columns=4,
            levels_back=4,
            func_nodes=self.func_nodes,
            input_nodes=self.input_nodes,
            output_nodes=self.output_nodes
        )

    def tearDown(self):
        pass

    def test_evaluate_cartesian(self):
        print self.cartesian.program()
        result, outputs = evaluate_cartesian(
            self.cartesian,
            self.functions,
            self.config
        )
        print result
        # self.assertIsNotNone(result)
        # self.assertIsNotNone(outputs)

    # def test_evaluate(self):
    #     output = evaluate_cartesian(self.cartesian, self.config)
    #     self.assertIsNotNone(output)


if __name__ == "__main__":
    unittest.main()
