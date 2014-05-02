#!/usr/bin/env python2.7
import random

from playground.ga.bit_string import BitString
from playground.population import Population


class BitStringGenerator(object):
    def __init__(self, config):
        self.config = config
        self.bitstr_config = self.config["bitstring_generation"]
        self.codons = self.config["codons"]

    def generate_random_codon(self):
        codon = random.sample(self.codons, 1)[0]
        return codon

    def generate_random_bitstr(self):
        bitstr = BitString()
        genome_len = self.bitstr_config["genome_length"]

        for i in range(genome_len):
            code = self.generate_random_codon()
            bitstr.genome.append(code)
            bitstr.length += 1

        return bitstr

    def init(self):
        population = Population(self.config)

        for i in xrange(self.config["max_population"]):
            bit_str = self.generate_random_bitstr()
            population.individuals.append(bit_str)

        return population
