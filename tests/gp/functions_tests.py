#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
from playground.gp.functions import GPFunctionRegistry

# SETTINGS
script_path = os.path.dirname(__file__)
config_file = "../config/initializer.json"
config_fp = os.path.join(script_path, config_file)


class FunctionsTests(unittest.TestCase):
    def setUp(self):
        self.config_file = config.load_config(config_fp)
        self.function = GPFunctionRegistry()

    def tearDown(self):
        del self.config_file

    def test_get_function(self):
        add = self.function.get_function("ADD")
        result = add(1, 2)
        self.assertEquals(result, 3)

        sub = self.function.get_function("SUB")
        result = sub(2, 1)
        self.assertEquals(result, 1)

        mul = self.function.get_function("MUL")
        result = mul(2, 1)
        self.assertEquals(result, 2)

        div = self.function.get_function("DIV")
        result = div(4, 2)
        self.assertEquals(result, 2)

        cos = self.function.get_function("COS")
        result = cos(0)
        self.assertEquals(result, 1)

        sin = self.function.get_function("SIN")
        result = sin(0)
        self.assertEquals(result, 0)


if __name__ == '__main__':
    unittest.main()
