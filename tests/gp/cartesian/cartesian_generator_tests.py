#!/usr/bin/env python2.7
import os
import sys
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

from playground.config import load_data
from playground.gp.cartesian.cartesian_generator import CartesianGenerator


class CartesianGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "cartesian": {
                "rows": 4,
                "columns": 3,
                "levels_back": 1,

                "num_inputs": 4,
                "num_outputs": 1
            },

            "function_nodes": [
                {"type": "FUNCTION", "name": "ADD", "arity": 2},
                {"type": "FUNCTION", "name": "SUB", "arity": 2},
                {"type": "FUNCTION", "name": "MUL", "arity": 2},
                {"type": "FUNCTION", "name": "DIV", "arity": 2},
                {"type": "FUNCTION", "name": "COS", "arity": 1},
                {"type": "FUNCTION", "name": "SIN", "arity": 1},
                {"type": "FUNCTION", "name": "RAD", "arity": 1}
            ],

            "data_file": "tests/data/sine.dat",

            "response_variable": {
                "name": "y"
            },

            "input_variables": [
                {"type": "INPUT", "name": "a"},
                {"type": "INPUT", "name": "b"},
                {"type": "INPUT", "name": "c"},
                {"type": "INPUT", "name": "d"}
            ]
        }
        self.generator = CartesianGenerator(self.config)

    def test_build_address_grid(self):
        result = self.generator.build_address_grid()
        self.assertEquals(
            result,
            [
                [0, 1, 2, 3],
                [4, 5, 6, 7],
                [8, 9, 10, 11],
                [12, 13, 14, 15]
            ]
        )

        self.config["cartesian"]["num_inputs"] = 2
        result = self.generator.build_address_grid()
        self.assertEquals(
            result,
            [
                [0, 1],
                [2, 3, 4, 5],
                [6, 7, 8, 9],
                [10, 11, 12, 13]
            ]
        )

    def test_calculate_column_level(self):
        self.config["cartesian"]["num_inputs"] = 2
        generator = CartesianGenerator(self.config)

        self.assertEquals(generator.calculate_column_level(2), 0)
        self.assertEquals(generator.calculate_column_level(5), 0)

        self.assertEquals(generator.calculate_column_level(6), 1)
        self.assertEquals(generator.calculate_column_level(9), 1)

        self.assertEquals(generator.calculate_column_level(10), 2)
        self.assertEquals(generator.calculate_column_level(13), 2)

        self.assertRaises(
            RuntimeError,
            self.generator.calculate_column_level,
            0
        )
        self.assertRaises(
            RuntimeError,
            self.generator.calculate_column_level,
            1
        )
        self.assertRaises(
            RuntimeError,
            self.generator.calculate_column_level,
            -1
        )
        self.assertRaises(
            RuntimeError,
            self.generator.calculate_column_level,
            14
        )

    def test_get_valid_addresses(self):
        result = self.generator.get_valid_addresses(0)
        self.assertEquals(range(4), result)

        result = self.generator.get_valid_addresses(1)
        self.assertEquals(range(8), result)

        result = self.generator.get_valid_addresses(2)
        self.assertEquals(
            [4, 5, 6, 7, 8, 9, 10, 11],
            result
        )

        self.assertRaises(
            RuntimeError,
            self.generator.get_valid_addresses,
            -1
        )
        self.assertRaises(
            RuntimeError,
            self.generator.get_valid_addresses,
            3
        )

    def test_gen_random_conn_gene(self):
        for i in range(100):
            result = self.generator.gen_random_conn_gene(4)
            self.assertTrue(result >= 0, result <= 3)

    def test_gen_random_func_gene(self):
        num_funcs = len(self.config["function_nodes"])
        for i in range(100):
            result = self.generator.gen_random_func_gene()
            self.assertTrue(result >= 0, result <= num_funcs - 1)

    def test_gen_random_func_node(self):
        for i in range(100):
            node_addr = 7
            func_node = self.generator.gen_random_func_node(node_addr)
            func_index = func_node[0]
            func_conns = func_node[1:]

            # asserts
            # check number of connections
            arity = self.config["function_nodes"][func_index]["arity"]
            self.assertEquals(arity, len(func_node[1:]))

            # check what connections points to
            rows = self.config["cartesian"]["rows"]
            columns = self.config["cartesian"]["columns"]
            max_addr = (rows * columns) - 1
            for conn in func_conns:
                self.assertTrue(conn >= 0 and conn <= max_addr)

    def test_gen_random_output_node(self):
        num_inputs = self.config["cartesian"]["num_inputs"]
        rows = self.config["cartesian"]["rows"]
        columns = self.config["cartesian"]["columns"]
        num_funcs = (rows * columns)
        max_addr = (num_funcs + num_inputs) - 1

        for i in range(100):
            res = self.generator.gen_random_output_node()

            # asserts
            self.assertTrue(res >= 0 and res <= max_addr)

    def test_prep_input_nodes(self):
        input_nodes = self.generator.prep_input_nodes()
        self.assertEquals(input_nodes, ["a", "b", "c", "d"])

    def test_generate_new_cartesian(self):
        cartesian = self.generator.generate_new_cartesian()
        cart_dict = cartesian.to_dict()

        # import pprint
        # pprint.pprint(cartesian.to_dict())

        # asserts
        rows = self.config["cartesian"]["rows"]
        columns = self.config["cartesian"]["columns"]
        levels_back = self.config["cartesian"]["levels_back"]
        num_inputs = self.config["cartesian"]["num_inputs"]

        # assert graph config
        self.assertEquals(cartesian.rows, rows)
        self.assertEquals(cartesian.columns, columns)
        self.assertEquals(cartesian.levels_back, levels_back)

        # assert graph elements
        num_func_nodes = rows * columns
        self.assertEquals(len(cartesian.func_nodes), num_func_nodes)
        self.assertEquals(cart_dict["func_nodes_len"], num_func_nodes)

        self.assertEquals(len(cartesian.input_nodes), num_inputs)
        self.assertEquals(cart_dict["input_nodes_len"], num_inputs)

        num_output_nodes = self.config["cartesian"]["num_outputs"]
        self.assertEquals(len(cartesian.output_nodes), num_output_nodes)
        self.assertEquals(cart_dict["output_nodes_len"], num_output_nodes)


if __name__ == "__main__":
    unittest.main()
