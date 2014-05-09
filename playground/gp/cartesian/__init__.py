#!/usr/bin/env python2


class Cartesian(object):
    def __init__(self, **kwargs):
        self.cartesian_id = None
        self.score = None

        self.config = kwargs["config"]

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

    def traverse(self, node_addr):
        tree_str = ""

        # pre-check edge cases
        if node_addr < len(self.input_nodes):
            input_name = self.program()[node_addr]
            return input_name

        # get node details
        node = self.program()[node_addr]
        conn_genes = node[1:]
        arity = len(conn_genes)

        # print node children and root
        tree_str += "("
        if arity == 2:
            tree_str += self.traverse(conn_genes.pop())
            tree_str += " "
            tree_str += self.config["function_nodes"][node[0]]["name"]
            tree_str += " "
            tree_str += self.traverse(conn_genes.pop())

        elif arity == 1:
            tree_str += self.config["function_nodes"][node[0]]["name"]
            tree_str += " "
            tree_str += self.traverse(conn_genes.pop())
        tree_str += ")"

        return tree_str

    def __str__(self):
        return self.traverse(self.output_nodes[0])

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
