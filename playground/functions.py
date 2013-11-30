#!/usr/bin/env python
import math


def add_function(left, right):
    return left + right


def sub_function(left, right):
    return left - right


def mul_function(left, right):
    return left * right


def div_function(left, right):
    return left / right


def cos_function(value):
    return math.cos(value)


def sin_function(value):
    return math.sin(value)


class FunctionRegistry(object):
    def __init__(self, override_defaults=False):
        self.functions = {}

        if override_defaults is False:
            self.register("ADD", add_function)
            self.register("SUB", sub_function)
            self.register("MUL", mul_function)
            self.register("DIV", div_function)
            self.register("COS", cos_function)
            self.register("SIN", sin_function)

    def register(self, function_name, function):
        self.functions[function_name] = function

    def unregister(self, function_name):
        del self.functions[function_name]

    def get_function(self, function_name):
        return self.functions[function_name]
