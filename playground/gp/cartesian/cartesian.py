#!/usr/bin/env python


class Cartesian(object):
    def __init__(self, **kwargs):
        self.cartesian_id = None
        self.score = None

        # graph config
        self.rows = kwargs["rows"]
        self.columns = kwargs["cols"]
        self.levels_back = kwargs["levels_back"]

        # graph elements
        self.func_nodes = kwargs["func_nodes"]
        self.input_nodes = kwargs["input_nodes"]
        self.output_nodes = kwargs["output_nodes"]
        self.graph = self.input_nodes + self.func_nodes
