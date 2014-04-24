#!/usr/bin/env python
# from random import randint
# from random import random
# from random import sample

from playground.recorder.record_type import RecordType


class CartesianMutation(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.recorder = kwargs.get("recorder", None)

        # mutation stats
        self.method = None
        self.index = None
        self.mutation_probability = None
        self.random_probability = None
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

    def point_mutation(self):
        pass

    def mutate(self, tree):
        mutation_methods = {
            "POINT_MUTATION": self.point_mutation
        }

        self.method = sample(self.config["mutation"]["methods"], 1)[0]
        self.index = None
        self.mutation_probability = self.config["mutation"]["probability"]
        self.random_probability = random()
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

        # record before mutation
        self.before_mutation = tree.to_dict()["program"]

        # mutate
        if self.mutation_probability >= self.random_probability:
            mutation_func = mutation_methods[self.method]
            mutation_func(tree)

        # record after mutation
        self.after_mutation = tree.to_dict()["program"]

        # record
        if self.recorder is not None:
            self.recorder.record(RecordType.MUTATION, self)

    def to_dict(self):
        self_dict = {
            "method": self.method,
            "mutation_index": self.index,
            "mutation_probability": self.mutation_probability,
            "random_probability": self.random_probability,
            "mutated": self.mutated,
            "before_mutation": self.before_mutation,
            "after_mutation": self.after_mutation
        }

        return self_dict
