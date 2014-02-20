#!/usr/bin/env python


class BitString(object):
    def __init__(self):
        self.bit_string_id = None
        self.score = None

        self.genome = []
        self.length = 0

    def valid(self):
        raise RuntimeError("Not Implemented!")

    def equals(self, target):
        if target.genome == self.genome:
            return True
        else:
            return False

    def to_dict(self):
        self_dict = {
            "id": id(self),
            "score": self.score,

            "genome": self.genome,
            "length": self.length
        }
        return self_dict
