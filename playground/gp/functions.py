#!/usr/bin/env python
import math
import decimal


class EvaluationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


def add_function(right, left):
    try:
        return left + right
    except:
        raise EvaluationError("Opps!")


def sub_function(right, left):
    try:
        return left - right
    except:
        raise EvaluationError("Opps!")


def mul_function(right, left):
    try:
        return left * right
    except:
        raise EvaluationError("Opps!")


def div_function(right, left):
    try:
        result = left / right
        return result
    except ZeroDivisionError as e:
        raise EvaluationError(e.message)


def pow_function(right, left):
    try:
        return math.pow(left, right)
    except:
        raise EvaluationError("Opps!")


def cos_function(value):
    try:
        return math.cos(value)
    except:
        raise EvaluationError("Opps!")


def sin_function(value):
    try:
        return math.sin(value)
    except:
        raise EvaluationError("Opps!")


def rad_function(value):
    try:
        return math.radians(value)
    except:
        raise EvaluationError("Opps!")


def ln_function(value):
    try:
        return float(decimal.Decimal(value).ln())
    except:
        raise EvaluationError("Opps!")


def log_function(value):
    try:
        return math.log(value, 10)
    except:
        raise EvaluationError("Opps!")


def exp_function(value):
    try:
        return math.exp(value)
    except:
        raise EvaluationError("Opps!")


def fact_function(value):
    return math.factorial(value)


class GPFunctionRegistry(object):
    def __init__(self, override_defaults=False):
        self.functions = {}

        if override_defaults is False:
            self.register("ADD", add_function)
            self.register("SUB", sub_function)
            self.register("MUL", mul_function)
            self.register("DIV", div_function)
            self.register("POW", pow_function)
            self.register("LOG", ln_function)

            self.register("COS", cos_function)
            self.register("SIN", sin_function)
            self.register("RAD", rad_function)
            self.register("LN", ln_function)
            self.register("EXP", exp_function)

    def register(self, function_name, function):
        self.functions[function_name] = function

    def unregister(self, function_name):
        del self.functions[function_name]

    def get_function(self, function_name):
        return self.functions[function_name]
