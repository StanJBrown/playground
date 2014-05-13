#!/usr/bin/env python2
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.gp.functions as funcs
from playground.gp.functions import GPFunctionRegistry
from playground.gp.functions import EvaluationError


class FunctionsTests(unittest.TestCase):
    def setUp(self):
        self.function = GPFunctionRegistry("SYMBOLIC_REGRESSION")

    def test_symbolic_regression_functions(self):
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

        # SQ
        func = self.function.get_function("SQ")
        result = func(4.0)
        self.assertEquals(result, 16.0)
        self.assertRaises(EvaluationError, func, "A")

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

        # EXP
        func = self.function.get_function("EXP")
        result = func(0)
        self.assertEquals(result, 1.0)
        self.assertRaises(EvaluationError, func, "A")

    def test_logic_functions(self):
        # ADD
        self.assertEquals(0, funcs.and_function(0, 0))
        self.assertEquals(0, funcs.and_function(1, 0))
        self.assertEquals(0, funcs.and_function(0, 1))
        self.assertEquals(1, funcs.and_function(1, 1))

        # OR
        self.assertEquals(0, funcs.or_function(0, 0))
        self.assertEquals(1, funcs.or_function(1, 0))
        self.assertEquals(1, funcs.or_function(0, 1))
        self.assertEquals(1, funcs.or_function(1, 1))

        # NOT
        self.assertEquals(1, funcs.not_function(0))
        self.assertEquals(0, funcs.not_function(1))

        # NAND
        self.assertEquals(1, funcs.nand_function(0, 0))
        self.assertEquals(1, funcs.nand_function(1, 0))
        self.assertEquals(1, funcs.nand_function(0, 1))
        self.assertEquals(0, funcs.nand_function(1, 1))

        # NOR
        self.assertEquals(1, funcs.nor_function(0, 0))
        self.assertEquals(0, funcs.nor_function(1, 0))
        self.assertEquals(0, funcs.nor_function(0, 1))
        self.assertEquals(0, funcs.nor_function(1, 1))

        # XOR
        self.assertEquals(0, funcs.xor_function(0, 0))
        self.assertEquals(1, funcs.xor_function(1, 0))
        self.assertEquals(1, funcs.xor_function(0, 1))
        self.assertEquals(0, funcs.xor_function(1, 1))

        # XNOR
        self.assertEquals(1, funcs.xnor_function(0, 0))
        self.assertEquals(0, funcs.xnor_function(1, 0))
        self.assertEquals(0, funcs.xnor_function(0, 1))
        self.assertEquals(1, funcs.xnor_function(1, 1))

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
