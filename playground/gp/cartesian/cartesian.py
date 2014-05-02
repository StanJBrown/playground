#!/usr/bin/env python2.7


class Cartesian(object):
    def __init__(self, **kwargs):
        self.cartesian_id = None
        self.score = None

        # graph config
        self.rows = kwargs["rows"]
        self.columns = kwargs["columns"]
        self.levels_back = kwargs["levels_back"]

        # graph elements
        self.func_nodes = kwargs["func_nodes"]
        self.input_nodes = kwargs["input_nodes"]
        self.output_nodes = kwargs["output_nodes"]

    def total_genes(self):
        total_genes = len([gene for node in self.func_nodes for gene in node])
        total_genes += len(self.input_nodes)

        return total_genes

    def program(self):
        return self.input_nodes + self.func_nodes + self.output_nodes

    def graph(self):
        return self.input_nodes + self.func_nodes

    def to_dict(self):
        self_dict = {
            "id": id(self),
            "score": self.score,

            "rows": self.rows,
            "columns": self.columns,
            "levels_back": self.levels_back,

            "func_nodes_len": len(self.func_nodes),
            "input_nodes_len": len(self.input_nodes),
            "output_nodes_len": len(self.output_nodes),

            "func_nodes": self.func_nodes,
            "input_nodes": self.input_nodes,
            "output_nodes": self.output_nodes,

            "program": self.program()
        }
        return self_dict
