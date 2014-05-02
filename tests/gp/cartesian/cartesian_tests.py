#!/usr/bin/env python2.7
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

from playground.gp.cartesian.cartesian import Cartesian


class CartesianTests(unittest.TestCase):
    def setUp(self):
        # make cartesian
        self.data = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ]
        self.chromosome = [
            [0, 0, 2],
            [0, 0, 3],
            [3, 4, 5],
            [0, 1, 2],
            [0, 1, 3],
            [2, 5, 7],
            [2, 6, 9],
            [0, 5, 7],
            [2, 11, 8],
            [0, 11, 8]
        ]
        self.output_nodes = [4, 9, 12, 13]
        self.cartesian = Cartesian(
            rows=1,
            columns=14,
            levels_back=0,
            func_nodes=self.chromosome,
            input_nodes=self.data,
            output_nodes=self.output_nodes
        )

    def test_program(self):
        solution = [
            # input nodes
            [1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16],

            # function nodes
            [0, 0, 2],
            [0, 0, 3],
            [3, 4, 5],
            [0, 1, 2],
            [0, 1, 3],
            [2, 5, 7],
            [2, 6, 9],
            [0, 5, 7],
            [2, 11, 8],
            [0, 11, 8],

            # output nodes
            4, 9, 12, 13
        ]
        program = self.cartesian.program()
        self.assertEquals(solution, program)

    def test_to_dict(self):
        solution = {
            "columns": 14,
            "func_nodes": [
                [0, 0, 2],
                [0, 0, 3],
                [3, 4, 5],
                [0, 1, 2],
                [0, 1, 3],
                [2, 5, 7],
                [2, 6, 9],
                [0, 5, 7],
                [2, 11, 8],
                [0, 11, 8]
            ],
            "func_nodes_len": 10,
            "input_nodes": [
                [1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]
            ],
            "input_nodes_len": 4,
            "levels_back": 0,
            "output_nodes": [4, 9, 12, 13],
            "output_nodes_len": 4,
            "program": [
                # input nodes
                [1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16],

                # function nodes
                [0, 0, 2],
                [0, 0, 3],
                [3, 4, 5],
                [0, 1, 2],
                [0, 1, 3],
                [2, 5, 7],
                [2, 6, 9],
                [0, 5, 7],
                [2, 11, 8],
                [0, 11, 8],

                # output nodes
                4, 9, 12, 13
            ],
            "rows": 1,
            "score": None
        }

        cartesian_dict = self.cartesian.to_dict()
        cartesian_dict.pop("id")

        import pprint
        pprint.pprint(cartesian_dict)

        self.assertEquals(cartesian_dict, solution)


if __name__ == "__main__":
    unittest.main()
