#!/usr/bin/env python
from random import randint

from playground.gp.cartesian.cartesian import Cartesian


class CartesianGenerator(object):
    def __init__(self, config):
        self.config = config

    def gen_random_gene(self, gene_type):
        gene = None
        rows = self.config["cartesian"]["rows"]
        columns = self.config["cartesian"]["columns"]
        max_addr = (rows * columns) - 1

        # generate random function gene or connection gene
        if gene_type == "FUNC":
            gene = randint(0, len(self.config["function_nodes"]) - 1)
        elif gene_type == "CONN":
            gene = randint(0, max_addr)

        return gene

    def gen_new_random_gene(self, gene_type, old_gene):
        new_gene = old_gene
        retry = 0
        retry_limit = 10

        # pick random function gene or connection gene
        while new_gene == old_gene and retry < retry_limit:
            new_gene = self.gen_random_gene(gene_type)
            retry += 1

        if retry == retry_limit:
            return None
        else:
            return new_gene

    def gen_random_func_node(self):
        func_index = randint(0, len(self.config["function_nodes"]) - 1)
        arity = self.config["function_nodes"][func_index]["arity"]
        conns = [self.gen_random_gene("CONN") for i in range(arity)]

        return [func_index] + conns

    def gen_random_output_node(self):
        return self.gen_random_gene("CONN")

    def prep_input_nodes(self):
        inputs = self.config["input_variables"]
        data = self.config["data"]

        if len(inputs) != self.config["cartesian"]["num_inputs"]:
            err = "Number of inputs in data and cartesian don't match!"
            raise RuntimeError(err)

        input_nodes = []
        for input_var in inputs:
            input_nodes.append(input_var["name"])

        return input_nodes


    def generate_new_cartesian(self):
        # cartesian details
        rows = self.config["cartesian"]["rows"]
        columns = self.config["cartesian"]["columns"]
        total_nodes =  rows * columns

        num_funcs = total_nodes - self.config["cartesian"]["num_inputs"]
        num_outputs = self.config["cartesian"]["num_outputs"]

        # nodes
        func_nodes = [self.gen_random_func_node() for i in range(num_funcs)]
        out_nodes = [self.gen_random_output_node() for i in range(num_outputs)]
        in_nodes = self.prep_input_nodes()

        # create new cartesian obj
        return Cartesian(
            rows=self.config["cartesian"]["rows"],
            columns=self.config["cartesian"]["columns"],
            levels_back=self.config["cartesian"]["levels_back"],
            func_nodes=func_nodes,
            input_nodes=in_nodes,
            output_nodes=out_nodes
        )
