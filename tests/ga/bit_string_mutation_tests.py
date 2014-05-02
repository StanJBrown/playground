#!/usr/bin/env python2.7
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
            ],

            "mutation": {
                "method": [
                    "POINT_MUTATION"
                ],
                "probability": 1.0
            }
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

    def test_mutation(self):
        bitstr_before = list(self.bitstr.genome)
        print "BEFORE MUTATION:", bitstr_before

        self.mutation.mutate(self.bitstr)

        bitstr_after = list(self.bitstr.genome)
        print "AFTER MUTATION:", bitstr_after

        # assert
        self.assertFalse(bitstr_before == bitstr_after)

        self.config["mutation"]["method"] = "RANDOM_MUTATION"
        self.assertRaises(RuntimeError, self.mutation.mutate, self.bitstr)

    def test_to_dict(self):
        self.mutation.mutate(self.bitstr)
        mut_dict = self.mutation.to_dict()

        self.assertEquals(mut_dict["method"], "POINT_MUTATION")
        self.assertIsNotNone(mut_dict["mutation_probability"])
        self.assertIsNotNone(mut_dict["random_probability"])
        self.assertEquals(mut_dict["mutated"], True)
        self.assertIsNotNone(mut_dict["before_mutation"])
        self.assertIsNotNone(mut_dict["after_mutation"])


if __name__ == '__main__':
    random.seed(0)
    unittest.main()
