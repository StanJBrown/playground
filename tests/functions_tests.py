#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
from playground.functions import FunctionRegistry

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/initializer.json")


class InitializerTests(unittest.TestCase):
    def setUp(self):
        self.config_file = config.load_config(config_fp)
        self.function = FunctionRegistry()

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
