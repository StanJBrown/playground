#!/usr/bin/env python2.7
import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import playground.parameter_setter.racing as racing


# SETTINGS
script_path = os.path.dirname(__file__)


class RacingTests(unittest.TestCase):
    def setUp(self):
        self.data1 = [
            [16, 13, 12],
            [10, 5, 2],
            [7, 8, 9],
            [13, 11, 5],
            [17, 2, 6],
            [10, 7, 9],
            [11, 6, 7]
        ]

        self.data2 = [
            [16, 17, 11],
            [10, 5, 2],
            [7, 8, 0],
            [13, 9, 5],
            [17, 2, 2],
            [10, 10, 9],
            [11, 6, 5]
        ]

    def test_rank(self):
        result = racing.rank_data(self.data1)
        self.assertEquals(
            result,
            [
                [3, 2, 1],
                [3, 2, 1],
                [1, 2, 3],
                [3, 2, 1],
                [3, 1, 2],
                [3, 1, 2],
                [3, 1, 2]
            ]
        )

        result = racing.rank_data(self.data2)
        self.assertEquals(
            result,
            [
                [2, 3, 1],
                [3, 2, 1],
                [2, 3, 1],
                [3, 2, 1],
                [3, 1.5, 1.5],
                [2.5, 2.5, 1],
                [3, 2, 1]
            ]
        )

    def test_sum_ranks(self):
        ranked_data = racing.rank_data(self.data1)
        result = racing.sum_col_ranks(ranked_data)
        self.assertEquals(result, [19, 11, 12])

        ranked_data = racing.rank_data(self.data2)
        result = racing.sum_col_ranks(ranked_data)
        self.assertEquals(result, [18.5, 16, 7.5])

    def test_friedman_test_no_ties(self):
        result = racing.friedman_test_no_ties(self.data1)
        print result


if __name__ == "__main__":
    unittest.main()
