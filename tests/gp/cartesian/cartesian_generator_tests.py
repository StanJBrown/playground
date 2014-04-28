#!/usr/bin/env python
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
                "columns": 4,
                "levels_back": 10,

                "num_inputs": 1,
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

            "data_file" : "tests/data/sine.dat",

            "response_variable": {
                "name": "y"
            },

            "input_variables" : [
                { "type": "INPUT", "name": "x" }
            ]
        }
        load_data(self.config)

        self.generator = CartesianGenerator(self.config)

    def test_gen_random_gene(self):
        # test function gene
        num_functions = len(self.config["function_nodes"])
        for i in range(100):
            res = self.generator.gen_random_gene("FUNC")

            # asserts
            self.assertTrue(res >= 0 and res <= num_functions - 1)

        # test connection gene
        rows = self.config["cartesian"]["rows"]
        columns = self.config["cartesian"]["columns"]
        max_addr = (rows * columns) - 1
        for i in range(100):
            res = self.generator.gen_random_gene("CONN")

            # asserts
            self.assertTrue(res >= 0 and res <= max_addr)

    def test_gen_new_random_gene(self):
        # test function gene
        num_functions = len(self.config["function_nodes"])
        for i in range(100):
            old = random.randint(0,  num_functions - 1)
            res = self.generator.gen_new_random_gene("FUNC", old,)

            # asserts
            self.assertTrue(res != old)
            self.assertTrue(res >= 0 and res <= num_functions - 1)

        # test connection gene
        rows = self.config["cartesian"]["rows"]
        columns = self.config["cartesian"]["columns"]
        max_addr = (rows * columns) - 1
        for i in range(100):
            old = random.randint(0, max_addr)
            res = self.generator.gen_new_random_gene("CONN", old)

            # asserts
            self.assertTrue(res != old)
            self.assertTrue(res >= 0 and res <= max_addr)

    def test_gen_random_func_node(self):
        for i in range(100):
            func_node = self.generator.gen_random_func_node()
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
        rows = self.config["cartesian"]["rows"]
        columns = self.config["cartesian"]["columns"]
        max_addr = (rows * columns) - 1
        for i in range(100):
            res = self.generator.gen_random_output_node()

            # asserts
            self.assertTrue(res >= 0 and res <= max_addr)

    def test_prep_input_nodes(self):
        input_nodes = self.generator.prep_input_nodes()
        self.assertEquals(input_nodes, ["x"])

    def test_generate_new_cartesian(self):
        cartesian = self.generator.generate_new_cartesian()
        cart_dict = cartesian.to_dict()

        # import pprint
        # pprint.pprint(cartesian.to_dict())

        # asserts
        rows = self.config["cartesian"]["rows"]
        columns = self.config["cartesian"]["columns"]
        levels_back = self.config["cartesian"]["levels_back"]
        max_addr = (rows * columns) - 1

        # assert graph config
        self.assertEquals(cartesian.rows, rows)
        self.assertEquals(cartesian.columns, columns)
        self.assertEquals(cartesian.levels_back, levels_back)

        # assert graph elements
        num_func_nodes = rows * columns - self.config["cartesian"]["num_inputs"]
        self.assertEquals(len(cartesian.func_nodes), num_func_nodes)
        self.assertEquals(cart_dict["func_nodes_len"], num_func_nodes)

        # num_input_nodes = self.config["cartesian"]["num_inputs"]
        # self.assertEquals(len(cartesian.input_nodes), num_input_nodes)
        # self.assertEquals(cart_dict["input_nodes_len"], num_input_nodes)

        num_output_nodes = self.config["cartesian"]["num_outputs"]
        self.assertEquals(len(cartesian.output_nodes), num_output_nodes)
        self.assertEquals(cart_dict["output_nodes_len"], num_output_nodes)



if __name__ == "__main__":
    unittest.main()
