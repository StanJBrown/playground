#!/usr/bin/env python
import playground.gp.functions as functions


class CartesianEvaluator(object):
    def __init__(self):
        self.genotype_table = []
        self.prog_inputs = 4
        self.prog_outputs = 4

        self.lookup_table = {}
        self.lookup_table[0] = functions.add_function
        self.lookup_table[1] = functions.sub_function
        self.lookup_table[2] = functions.mul_function
        self.lookup_table[3] = functions.div_function

    def get_arity(self, node):
        return len(node) - 1

    def eval_node(self, node, conn_genes, data):
        arity = len(node[1:])
        function = self.lookup_table[node[0]]

        # prep input data
        node_input = []
        for i in range(arity):
            node_input.append(data[conn_genes[i]])

        # evaluate
        node_output = []
        for data_row in zip(*node_input):
            node_output.append(function(*data_row))

        return node_output

    def traverse_backwards(self, cartesian, node_index, output, visited):
        if node_index >= self.prog_inputs:
            node = cartesian.graph[node_index]

            # check arity
            conn_genes = node[1:]
            for conn in conn_genes:
                self.traverse_backwards(cartesian, conn, output, visited)

            if node_index not in visited:
                # evaluate function with data
                node_output = self.eval_node(node, conn_genes, output)

                # record node output and append node index to visited
                output[node_index] = node_output
                visited.append(node_index)

    def evaluate(self, cartesian):
        visited = []
        results = []
        output = {}

        # prep output with input data
        for i in range(len(cartesian.input_nodes)):
            output[i] = cartesian.input_nodes[i]

        # for output_node in output_nodes:
        for node_index in cartesian.output_nodes:
            self.traverse_backwards(cartesian, node_index, output, visited)
            results.append(output[node_index])

        return results
