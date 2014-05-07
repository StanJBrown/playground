#!/usr/bin/env python2
from random import random
from random import randint

from playground.recorder.record_type import RecordType


class BitStringCrossover(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.recorder = kwargs.get("recorder", None)

        self.method = None
        self.index = None
        self.crossover_probability = None
        self.random_probability = None
        self.crossovered = False
        self.before_crossover = None
        self.after_crossover = None

    def uniform_random_index(self, bstr_1, bstr_2):
        start = 0
        end = 0

        if bstr_1.length > bstr_2.length:
            end = bstr_2.length - 1
        else:
            end = bstr_1.length - 1

        return randint(start, end)

    def one_point_crossover(self, bstr_1, bstr_2, index=None):
        if index is None:
            self.index = self.uniform_random_index(bstr_1, bstr_2)
            index = self.index
        else:
            self.index = index

        # slice
        bstr_1_half = list(bstr_1.genome[0:index])
        bstr_2_half = list(bstr_2.genome[0:index])

        # swap
        bstr_1.genome[0:index] = bstr_2_half
        bstr_2.genome[0:index] = bstr_1_half
        self.crossovered = True

    def crossover(self, bstr_1, bstr_2):
        self.method = self.config["crossover"]["method"]
        self.crossover_probability = self.config["crossover"]["probability"]
        self.random_probability = random()
        self.crossovered = False
        self.before_crossover = []
        self.after_crossover = []

        # record before crossver
        self.before_crossover.append("".join(bstr_1.genome))
        self.before_crossover.append("".join(bstr_2.genome))

        # crossover
        if self.crossover_probability >= self.random_probability:
            if self.method == "ONE_POINT_CROSSOVER":
                self.one_point_crossover(bstr_1, bstr_2)
            else:
                raise RuntimeError("Undefined crossover method!")

        # record after crossver
        self.after_crossover.append("".join(bstr_1.genome))
        self.after_crossover.append("".join(bstr_2.genome))

        # record
        if self.recorder is not None:
            self.recorder.record(RecordType.CROSSOVER, self)

    def to_dict(self):
        self_dict = {
            "method": self.method,
            "index": self.index,
            "crossover_probability": self.crossover_probability,
            "random_probability": self.random_probability,
            "crossovered": self.crossovered,
            "before_crossover": self.before_crossover,
            "after_crossover": self.after_crossover
        }
        return self_dict
