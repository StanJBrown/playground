#!/usr/bin/env python
import os
import sys
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from playground.ga.bit_string_generator import BitStringGenerator
from playground.ga.bit_string_mutation import BitStringMutation


class BitStrMutationTests(unittest.TestCase):
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
            ]
        }
        generator = BitStringGenerator(self.config)
        self.bitstr = generator.generate_random_bitstr()
        self.mutation = BitStringMutation(self.config)

    def test_point_mutation(self):
        index = random.randint(0, len(self.bitstr.genome) - 1)

        bitstr_before = list(self.bitstr.genome)
        print "BEFORE MUTATION:", bitstr_before
        print "MUTATION INDEX:", index

        self.mutation.point_mutation(self.bitstr, index)

        bitstr_after = list(self.bitstr.genome)
        print "AFTER MUTATION:", bitstr_after

        # assert
        self.assertFalse(bitstr_before == bitstr_after)

if __name__ == '__main__':
    random.seed(0)
    unittest.main()
