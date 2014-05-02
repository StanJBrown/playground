#!/usr/bin/env python2.7
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.ga.bit_string_generator import BitStringGenerator


class BitStringTests(unittest.TestCase):
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
        self.bitstr_1 = generator.generate_random_bitstr()
        self.bitstr_2 = generator.generate_random_bitstr()

    def test_valid(self):
        print "BITSTR 1:", self.bitstr_1.genome
        print "BITSTR 2:", self.bitstr_2.genome

        self.assertFalse(self.bitstr_1.equals(self.bitstr_2))
        self.assertTrue(self.bitstr_1.equals(self.bitstr_1))

    def test_to_dict(self):
        bitstr_dict = self.bitstr_1.to_dict()
        print "BITSTR 1 DICT:", bitstr_dict

        self.assertTrue(bitstr_dict is not None)


if __name__ == '__main__':
    unittest.main()
