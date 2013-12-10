#!/usr/bin/env python
import math


class EvaluationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


def add_function(left, right):
    return left + right


def sub_function(left, right):
    return left - right


def mul_function(left, right):
    return left * right


def div_function(left, right):
    try:
        result = left / right
        return result
    except ZeroDivisionError as e:
        raise EvaluationError(e.message)


def pow_function(left, right):
    try:
        return math.pow(left, right)
    except:
        raise EvaluationError("Opps!")


def cos_function(value):
    return math.cos(value)


def sin_function(value):
    return math.sin(value)


def rad_function(value):
    try:
        return math.radians(value)
    except:
        raise EvaluationError("Opps!")


def ln_function(value):
    try:
        return math.log(value)
    except:
        raise EvaluationError("Opps!")


def fact_function(value):
    return math.factorial(value)


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
            self.register("RAD", rad_function)
            self.register("LN", ln_function)

    def register(self, function_name, function):
        def tryFunc(*args):
            try:
                return function(*args)
            except:
                raise EvaluationError("Opps!")

        self.functions[function_name] = tryFunc

    def unregister(self, function_name):
        del self.functions[function_name]

    def get_function(self, function_name):
        return self.functions[function_name]
