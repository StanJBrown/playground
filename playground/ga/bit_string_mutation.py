#!/usr/bin/env python2.7
from random import randint
from random import random
from random import sample

from playground.ga.bit_string_generator import BitStringGenerator
from playground.recorder.record_type import RecordType


class BitStringMutation(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.recorder = kwargs.get("recorder", None)
        self.generator = BitStringGenerator(self.config)

        # mutation stats
        self.method = None
        self.index = None
        self.mutation_probability = None
        self.random_probability = None
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

    def point_mutation(self, bitstr, index=None):
        # mutate node
        if index is None:
            index = randint(0, len(bitstr.genome) - 1)
            self.index = index
        else:
            self.index = index

        new_codon = self.generator.generate_random_codon()
        bitstr.genome[index] = new_codon
        self.mutated = True

    def mutate(self, bitstr):
        self.method = sample(self.config["mutation"]["method"], 1)[0]
        self.mutation_probability = self.config["mutation"]["probability"]
        self.random_probability = random()
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

        # record before mutation
        self.before_mutation = "".join(bitstr.genome)

        # mutate
        if self.mutation_probability >= self.random_probability:
            if self.method == "POINT_MUTATION":
                self.point_mutation(bitstr)
            else:
                raise RuntimeError(
                    "Undefined mutation method [{0}]".format(self.method)
                )

        # record after mutation
        self.after_mutation = "".join(bitstr.genome)

        # record
        if self.recorder is not None:
            self.recorder.record(RecordType.MUTATION, self)

    def to_dict(self):
        self_dict = {
            "method": self.method,
            "mutation_probability": self.mutation_probability,
            "random_probability": self.random_probability,
            "mutated": self.mutated,
            "before_mutation": self.before_mutation,
            "after_mutation": self.after_mutation
        }

        return self_dict
