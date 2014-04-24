#!/usr/bin/env python
import sys
import os
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.ga.bit_string_generator import BitStringGenerator
from playground.ga.bit_string_crossover import BitStringCrossover


class BitStringCrossoverTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "max_population": 10,

            "bitstring_generation": {
                "genome_length": 10
            },

            "codons": [
                "0000",
                "0001",
                "0010",
                "0011",
                "0100",
                "0101",
                "0110",
                "0111",
                "1000",
                "1001",
                "1011",
                "1111"
            ],

            "crossover": {
                "method": "ONE_POINT_CROSSOVER",
                "probability": 1.0
            }
        }
        generator = BitStringGenerator(self.config)
        self.bitstr_1 = generator.generate_random_bitstr()
        self.bitstr_2 = generator.generate_random_bitstr()
        self.crossover = BitStringCrossover(self.config)

    def test_uniform_random_index(self):
        i = self.crossover.uniform_random_index(self.bitstr_1, self.bitstr_2)

        self.assertTrue(i is not None)
        self.assertTrue(i < self.bitstr_1.length)
        self.assertTrue(i < self.bitstr_2.length)

    def test_one_point_crossover(self):
        bitstr_1_before = list(self.bitstr_1.genome)
        bitstr_2_before = list(self.bitstr_2.genome)
        index = random.randint(0, self.bitstr_1.length)

        print "BITSTR 1 [BEFORE]:", self.bitstr_1.genome
        print "BITSTR 2 [BEFORE]:", self.bitstr_2.genome
        print "INDEX:", index

        self.crossover.one_point_crossover(self.bitstr_1, self.bitstr_2, index)

        bitstr_1_after = list(self.bitstr_1.genome)
        bitstr_2_after = list(self.bitstr_2.genome)

        print "BITSTR 1 [AFTER]:", self.bitstr_1.genome
        print "BITSTR 2 [AFTER]:", self.bitstr_2.genome

        # assert
        self.assertFalse(bitstr_1_before == bitstr_1_after)
        self.assertFalse(bitstr_2_before == bitstr_2_after)

        # change it back to its original form
        bstr_1_half = list(bitstr_1_after[0:index])
        bstr_2_half = list(bitstr_2_after[0:index])
        bitstr_1_after[0:index] = bstr_2_half
        bitstr_2_after[0:index] = bstr_1_half

        self.assertTrue(bitstr_1_before == bitstr_1_after)
        self.assertTrue(bitstr_2_before == bitstr_2_after)

    def test_crossover(self):
        bitstr_1_before = list(self.bitstr_1.genome)
        bitstr_2_before = list(self.bitstr_2.genome)

        print "BITSTR 1 [BEFORE]:", self.bitstr_1.genome
        print "BITSTR 2 [BEFORE]:", self.bitstr_2.genome

        self.crossover.crossover(self.bitstr_1, self.bitstr_2)

        bitstr_1_after = list(self.bitstr_1.genome)
        bitstr_2_after = list(self.bitstr_2.genome)

        print "BITSTR 1 [AFTER]:", self.bitstr_1.genome
        print "BITSTR 2 [AFTER]:", self.bitstr_2.genome

        # assert
        self.assertFalse(bitstr_1_before == bitstr_1_after)
        self.assertFalse(bitstr_2_before == bitstr_2_after)

        self.config["crossover"]["method"] = "RANDOM_CROSSOVER"
        self.assertRaises(
            RuntimeError,
            self.crossover.crossover,
            self.bitstr_1,
            self.bitstr_2
        )

    def test_to_dict(self):
        self.crossover.crossover(self.bitstr_1, self.bitstr_2)
        cross_dict = self.crossover.to_dict()

        # import pprint
        # pprint.pprint(cross_dict)

        self.assertEqual(cross_dict["method"], "ONE_POINT_CROSSOVER")
        self.assertTrue(cross_dict["index"] is not None)
        self.assertTrue(cross_dict["crossover_probability"] is not None)
        self.assertTrue(cross_dict["random_probability"] is not None)
        self.assertTrue(cross_dict["crossovered"] is not None)
        self.assertEqual(len(cross_dict["before_crossover"]), 2)
        self.assertEqual(len(cross_dict["after_crossover"]), 2)


if __name__ == '__main__':
    random.seed(0)
    unittest.main()
