#!/usr/bin/env python


class Cartesian(object):
    def __init__(self):
        self.cartesian_id = None
        self.score = None

        self.matrix = []
        self.func_nodes = []
        self.input_nodes = []
        self.output_nodes = []
        self.rows = 0
        self.columns = 0
        self.levels_back = 0

        self.cartesian_decoder = None
