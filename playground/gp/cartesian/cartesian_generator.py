#!/usr/bin/env python
from playground.gp.functions import FunctionRegistry


class CartesianGenerator(object):
    def __init__(self):
        self.functions = FunctionRegistry()

    def generate_new_node(self, random_arity=True):
        pass
