#!/usr/bin/env python2.7
import os
import sys
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.climbing.climbers import hill_climbing
# from playground.climbing.climbers import steepest_ascent_hill_climbing
from playground.climbing.utils import check_iterations
from playground.climbing.utils import check_time
from playground.climbing.utils import check_score
from playground.climbing.utils import stop_function


class ClimbersTests(unittest.TestCase):

    def setUp(self):
        self.solution = "helloworld"
        self.candidate = "abcdefghij"

        self.config = {
            "debug": False,

            "tweak_function": self.tweak_function,
            "eval_function": self.eval_function,
            "stop_function": stop_function,

            "candidate": self.candidate,
            "max_iterations": 1000,
            "target_score": 1000,

            "comparator": self.int_cmp
        }

    def tearDown(self):
        pass

    def eval_function(self, candidate):
        solution = list("helloworld")
        test = list(candidate)

        # calcuate character difference between two strings
        dist_err = 0
        for i in range(len(test)):
            dist_err += abs(ord(test[i]) - ord(solution[i]))

        return 1000 - dist_err

    def tweak_function(self, candidate):
        # make a copy of candidate to be tweaked
        tweak_candidate = list(candidate)

        # randomly select a character to be tweak
        index = random.randint(0, len(candidate) - 1)

        # randomly tweak up or down
        if random.random() > 0.5:
            tweak_candidate[index] = chr(ord(candidate[index]) + 1)
        else:
            tweak_candidate[index] = chr(ord(candidate[index]) - 1)

        return "".join(tweak_candidate)

    def int_cmp(self, num_1, num_2):
        if num_1 > num_2:
            return 1
        elif num_1 < num_2:
            return -1
        else:
            return 0

    def test_check_iterations(self):
        self.assertFalse(check_iterations(100, 0))
        self.assertTrue(check_iterations(100, 100))
        self.assertRaises(RuntimeError, check_iterations, None, 100)
        self.assertRaises(RuntimeError, check_iterations, 100, None)

    def test_check_time(self):
        self.assertFalse(check_time(100, 0))
        self.assertTrue(check_time(100, 100))
        self.assertRaises(RuntimeError, check_time, None, 100)
        self.assertRaises(RuntimeError, check_time, 100, None)

    def test_check_score(self):
        self.assertFalse(check_score(100, 0, self.int_cmp))
        self.assertTrue(check_score(100, 100, self.int_cmp))
        self.assertRaises(RuntimeError, check_score, None, 100, self.int_cmp)
        self.assertRaises(RuntimeError, check_score, 100, None, self.int_cmp)
        self.assertRaises(RuntimeError, check_score, 100, 100, None)

    def test_hill_climbing(self):
        # run hill climbing
        result = hill_climbing(self.config)

        # assert
        self.assertEquals(result[0], self.solution)
        self.assertEquals(result[1], 1000)

    # def test_steepest_ascent_hill_climbing(self):
    #     # run hill climbing
    #     self.config["tweaks"] = 10
    #     result = steepest_ascent_hill_climbing(self.config)

    #     # assert
    #     self.assertEquals(result[0], self.solution)
    #     self.assertEquals(result[1], 1000)

if __name__ == "__main__":
    unittest.main()
