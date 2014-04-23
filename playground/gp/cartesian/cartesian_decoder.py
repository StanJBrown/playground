#!/usr/bin/env python
import playground.gp.functions as functions
# Ln - Maximum nodes in a graph
# Ln = n_c * n_r
# L_g - Total number of genes in the genotype
#
# n_u - Number of nodes used/active
# n_i - Number of program inputs
# n_o - Number of program outputs
# O_i - Number of output genes
# f_i - Function integer addresses
# C_ij - Connection genes C_ij
#
# G[L_g] - Genotype array
#
#
# M = L_n + n_i


class CartesianDecoder(object):
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

    def find_active_nodes(self, chromosome, node_used):
        # mark all chromosome nodes in-active
        node_used.extend([False for i in range(len(chromosome))])

        # mark nodes connected to output nodes active
        for i in range(len(chromosome) - self.prog_outputs, len(chromosome)):
            node_used[chromosome[i][0]] = True

        # find active nodes - by starting from the end of the chromosome
        for i in range(len(chromosome) - 1, -1, -1):
            if node_used[i]:
                # write connection genes for node into array node_genes
                node_genes = []
                node_arity = self.get_arity(chromosome[i])
                for j in range(0, node_arity):
                    node_genes.append(chromosome[i][j + 1])

                # mark nodes pointed by connection genes active
                for j in range(0, node_arity):
                    # if conn-gene points within graph we are looking at
                    if node_genes[j] <= i:
                        node_used[node_genes[j]] = True

    def eval_node(self, node, conn_genes, output):
        arity = len(node[1:])
        function = self.lookup_table[node[0]]
        input_data = [output[i] for i in conn_genes]

        node_output = []
        for row in range(len(input_data[0])):
            row_data = [input_data[col][row] for col in range(arity)]
            node_output.append(function(*row_data))

        return node_output

    def traverse_backwards(self, chromosome, node_index, output, visited):
        if node_index >= self.prog_inputs:
            node = chromosome[node_index]

            # check arity
            conn_genes = node[1:]
            for conn in conn_genes:
                self.traverse_backwards(chromosome, conn, output, visited)

            if node_index not in visited:
                # evaluate function with data
                node_output = self.eval_node(node, conn_genes, output)

                # record node output and append node index to visited
                output[node_index] = node_output
                visited.append(node_index)

    def decode(self, chromosome, node_used, data):
        visited = []
        output = dict(zip(range(len(data)), data))

        # for output_node in output_nodes:
        for output_node in chromosome[-(self.prog_outputs):]:
            node_index = output_node[0]
            self.traverse_backwards(chromosome, node_index, output, visited)

        print output
