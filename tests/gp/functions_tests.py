#!/usr/bin/env python2
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.config as config
from playground.gp.functions import GPFunctionRegistry
from playground.gp.functions import EvaluationError

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

    def test_functions(self):
        # ADD
        func = self.function.get_function("ADD")
        result = func(1, 2)
        self.assertEquals(result, 3)
        self.assertRaises(EvaluationError, func, 0, "A")

        # SUB
        func = self.function.get_function("SUB")
        result = func(2, 1)
        self.assertEquals(result, -1)
        self.assertRaises(EvaluationError, func, 0, "A")

        # MUL
        func = self.function.get_function("MUL")
        result = func(2, 1)
        self.assertEquals(result, 2)
        self.assertRaises(EvaluationError, func, "B", "A")

        # DIV
        func = self.function.get_function("DIV")
        result = func(4.0, 2.0)
        self.assertEquals(result, 0.5)
        self.assertRaises(EvaluationError, func, 0.0, 2.0)

        # POW
        func = self.function.get_function("POW")
        result = func(2.0, 2.0)
        self.assertEquals(result, 4.0)
        self.assertRaises(EvaluationError, func, "A", 2.0)

        # COS
        func = self.function.get_function("COS")
        result = func(0)
        self.assertEquals(result, 1)
        self.assertRaises(EvaluationError, func, "A")

        # SIN
        func = self.function.get_function("SIN")
        result = func(0)
        self.assertEquals(result, 0)
        self.assertRaises(EvaluationError, func, "A")

        # RAD
        func = self.function.get_function("RAD")
        result = func(0)
        self.assertEquals(result, 0)
        self.assertRaises(EvaluationError, func, "A")

        # LN
        func = self.function.get_function("LN")
        result = func(1)
        self.assertEquals(result, 0.0)
        self.assertRaises(EvaluationError, func, "A")

        # LOG
        func = self.function.get_function("LOG")
        result = func(1)
        self.assertEquals(result, 0.0)
        self.assertRaises(EvaluationError, func, "A")

    def test_get_function(self):
        # ADD
        func = self.function.get_function("ADD")
        result = func(1, 2)
        self.assertEquals(result, 3)
        self.assertRaises(EvaluationError, func, 0, "A")

    def test_unregister(self):
        self.function.unregister("ADD")
        result = self.function.get_function("ADD")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
