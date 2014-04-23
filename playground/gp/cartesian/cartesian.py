#!/usr/bin/env python


class CartesianNode(object):
    def __init__(self):
        self.arity = None
        self.active = False

        self.function = None
        self.connection_genes = []
        self.genotype = []


class Cartesian(object):
    def __init__(self):
        self.cartesian_id = None
        self.score = None

        # graph config
        self.rows = 0
        self.columns = 0
        self.levels_back = 0

        # graph elements
        self.func_nodes = []
        self.input_nodes = []
        self.output_nodes = []
        self.graph = [
            self.input_nodes,
            self.func_nodes,
            self.out_nodes
        ]

        # utils
        self.cartesian_decoder = None
