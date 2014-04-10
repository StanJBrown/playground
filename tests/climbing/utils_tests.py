#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.climbing.utils import default_stop_function


class UtilsTests(unittest.TestCase):
    def int_cmp(self, num_1, num_2):
        if num_1 > num_2:
            return 1
        elif num_1 < num_2:
            return -1
        else:
            return 0

    def test_default_stop_function_with_iteration(self):
        # iteration - do not stop test
        details = {
            "max_iterations": 10,
            "iteration": 0
        }
        result = default_stop_function(details)
        self.assertFalse(result)

        # iteration - stop test
        details = {
            "max_iterations": 10,
            "iteration": 10
        }
        result = default_stop_function(details)
        self.assertTrue(result)

        # iteration - assert raises: missing iteration
        details = {
            "max_iterations": 10,
        }
        self.assertRaises(RuntimeError, default_stop_function, details)

    def test_defalt_stop_function_with_time(self):
        # time - do not stop test
        details = {
            "max_time": 100,
            "time": 0
        }
        result = default_stop_function(details)
        self.assertFalse(result)

        # time - stop test
        details = {
            "max_time": 100,
            "time": 100
        }
        result = default_stop_function(details)
        self.assertTrue(result)

        # time - assert raises: missing time
        details = {
            "max_time": 100
        }
        self.assertRaises(RuntimeError, default_stop_function, details)

    def test_defalt_stop_function_with_score(self):
        # score - do not stop test
        details = {
            "target_score": 100,
            "best_score": 0,
            "comparator": self.int_cmp
        }
        result = default_stop_function(details)
        self.assertFalse(result)

        # score - stop test
        details = {
            "target_score": 100,
            "best_score": 100,
            "comparator": self.int_cmp
        }
        result = default_stop_function(details)
        self.assertTrue(result)

        # score - assert raises: missing best_score
        details = {
            "target_score": 100,
            "comparator": self.int_cmp
        }
        self.assertRaises(RuntimeError, default_stop_function, details)

        # score - assert raises: missing comparator
        details = {
            "target_score": 100,
            "best_score": 0
        }
        self.assertRaises(RuntimeError, default_stop_function, details)


if __name__ == "__main__":
    unittest.main()
