#!/usr/bin/env python2.7
import copy
from random import randint
from random import random
from random import sample

from playground.recorder.record_type import RecordType
from playground.gp.cartesian.cartesian_generator import CartesianGenerator


class CartesianMutation(object):
    def __init__(self, config, **kwargs):
        self.config = config
        self.record_config = config.get("recorder", None)
        self.recorder = kwargs.get("recorder", None)
        self.generator = CartesianGenerator(config)

        # mutation stats
        self.method = None
        self.mutation_probability = None
        self.random_probability = None
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

    def mutate_new_func_gene(self, old_gene):
        retry = 0
        retry_limit = 10
        new_gene = old_gene

        while new_gene == old_gene and retry < retry_limit:
            new_gene = self.generator.gen_random_func_gene()
            retry += 1

        if new_gene == old_gene:
            err = "Error! Failed to mutate new function gene!"
            raise RuntimeError(err)
        else:
            return new_gene

    def mutate_new_conn_gene(self, old_gene, node_addr):
        retry = 0
        retry_limit = 20
        new_gene = old_gene

        while new_gene == old_gene and retry < retry_limit:
            new_gene = self.generator.gen_random_conn_gene(node_addr)
            retry += 1

        if new_gene == old_gene:
            err = "Error! Failed to mutate new function gene!"
            raise RuntimeError(err)
        else:
            return new_gene

    def mutate_function_node(self, node_addr, cartesian):
        # pick random function gene
        node = cartesian.graph()[node_addr]
        gene_index = randint(0, len(node) - 1)
        new_gene = None

        # mutate function gene
        if gene_index == 0:
            old_gene = node[gene_index]
            new_gene = self.mutate_new_func_gene(old_gene)

            old_arity = self.config["function_nodes"][old_gene]["arity"]
            new_arity = self.config["function_nodes"][new_gene]["arity"]

            if old_arity < new_arity:
                for i in range(old_arity - new_arity):
                    conn_gene = self.generator.gen_random_conn_gene(node_addr)
                    cartesian.graph()[node_addr].append(conn_gene)
            else:
                for i in range(new_arity - old_arity):
                    cartesian.graph()[node_addr].pop()

        # mutate connection gene
        else:
            old_gene = node[gene_index]
            new_gene = self.mutate_new_conn_gene(old_gene, node_addr)

        # return
        cartesian.graph()[node_addr][gene_index] = new_gene
        return gene_index

    def mutate_output_node(self, node_index, cartesian):
        retry = 0
        retry_limit = 20
        old_node_addr = cartesian.output_nodes[node_index]
        new_node_addr = old_node_addr

        # pick random input node or func node
        while new_node_addr == old_node_addr and retry < retry_limit:
            new_node_addr = randint(0, len(cartesian.graph()) - 1)
            retry += 1

        # mutate output node
        cartesian.output_nodes[node_index] = new_node_addr

        if retry == retry_limit:
            return None
        else:
            return new_node_addr

    def point_mutation(self, cartesian):
        result = None
        num_inputs = self.config["cartesian"]["num_inputs"]
        num_outputs = self.config["cartesian"]["num_outputs"]
        num_funcs = len(cartesian.func_nodes)
        max_addr = num_inputs + num_funcs + num_outputs - 1

        # chose random node
        node_addr = randint(num_inputs, max_addr)

        # mutate function node
        if node_addr < num_inputs + num_funcs:
            # convert index to node_addr in cartesian graph and mutate
            gene_index = self.mutate_function_node(node_addr, cartesian)
            result = {
                "mutated_node": "FUNC_NODE",
                "node_addr": node_addr,
                "gene_index": gene_index
            }

        # mutate output node
        else:
            # convert index to output node index and mutate
            node_index = node_addr - num_inputs - num_funcs
            new_addr = self.mutate_output_node(node_index, cartesian)
            result = {
                "mutated_node": "OUTPUT_NODE",
                "output_node": node_index,
                "new_addr": new_addr
            }

        # check result
        if result is None:
            self.mutated = False
        else:
            self.mutated = True
            self.index = result

    def mutate(self, cartesian):
        mutation_methods = {
            "POINT_MUTATION": self.point_mutation
        }

        self.method = sample(self.config["mutation"]["methods"], 1)[0]
        self.index = None
        self.mutation_probability = self.config["mutation"]["probability"]
        self.random_probability = random()
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

        # record before mutation
        self.before_mutation = copy.deepcopy(cartesian.program())

        # mutate
        if self.mutation_probability >= self.random_probability:
            mutation_func = mutation_methods[self.method]
            mutation_func(cartesian)

        # record after mutation
        self.after_mutation = copy.deepcopy(cartesian.program())

        # record
        if self.recorder is not None:
            self.recorder.record(RecordType.MUTATION, self)

    def to_dict(self):
        self_dict = {
            "method": self.method,
            "mutation_probability": self.mutation_probability,
            "random_probability": self.random_probability,
            "mutated": self.mutated,
            "index": self.index,
            "before_mutation": self.before_mutation,
            "after_mutation": self.after_mutation
        }

        return self_dict
