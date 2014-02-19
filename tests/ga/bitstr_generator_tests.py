#!/usr/bin/env python
import unittest

from playground.ga.bitstr_generator import BitStrGenerator


class BitStrGeneratorTests(unittest.TestCase):
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
        self.generator = BitStrGenerator(self.config)

    def test_generate_random_codon(self):
        codon = self.generator.generate_random_codon()

        self.assertTrue(len(codon) > 0)
        self.assertTrue(codon in self.config["codons"])

    def test_generate_random_bitstr(self):
        bitstr = self.generator.generate_random_bitstr()

        self.assertTrue(len(bitstr.genome) > 0)
        self.assertEquals(bitstr.length, 10)
        self.assertEquals(bitstr.score, None)

    def test_init(self):
        population = self.generator.init()

        self.assertEquals(len(population.individuals), 10)


if __name__ == "__main__":
    unittest.main()
