#!/usr/bin/env python
import copy
from random import randint
from random import random
from random import sample

from playground.recorder.record_type import RecordType


class CartesianMutation(object):
    def __init__(self, config):
        self.config = config
        self.recorder = config.get("recorder", None)

        # mutation stats
        self.method = None
        self.mutation_probability = None
        self.random_probability = None
        self.mutated = False
        self.before_mutation = None
        self.after_mutation = None

    def gen_random_gene(self, gene_type, old_gene, cartesian):
        new_gene = old_gene
        retry = 0
        retry_limit = 10

        # pick random function gene or connection gene
        while new_gene == old_gene and retry < retry_limit:
            if gene_type == "FUNC":
                new_gene = randint(0, len(self.config["function_nodes"]) - 1)

            elif gene_type == "CONN":
                new_gene = randint(0, len(cartesian.graph) - 1)

            retry += 1

        if retry == retry_limit:
            return None
        else:
            return new_gene

    def mutate_function_node(self, node_addr, cartesian):
        # pick random function gene
        node = cartesian.graph[node_addr]
        gene_index = randint(0, len(node) - 1)
        new_gene = None

        # mutate function gene
        if gene_index == 0:
            old_gene = node[gene_index]
            new_gene = self.gen_random_gene("FUNC", old_gene, cartesian)

        # mutate connection gene
        else:
            old_gene = node[gene_index]
            new_gene = self.gen_random_gene("CONN", old_gene, cartesian)

        # return
        if new_gene is not None:
            cartesian.graph[node_addr][gene_index] = new_gene
            return gene_index
        else:
            return None

    def mutate_output_node(self, node_index, cartesian):
        old_node_addr = cartesian.output_nodes[node_index]
        new_node_addr = old_node_addr
        retry = 0
        retry_limit = 10

        # pick random input node or func node
        while new_node_addr == old_node_addr and retry < retry_limit:
            new_node_addr = randint(0, len(cartesian.graph) - 1)
            retry += 1

        # mutate output node
        cartesian.output_nodes[node_index] = new_node_addr

        if retry == retry_limit:
            return None
        else:
            return new_node_addr

    def point_mutation(self, cartesian):
        # chose random node
        node_pool = cartesian.func_nodes + cartesian.output_nodes
        index = randint(0, len(node_pool) - 2)
        result = None

        # mutate function node
        if index < (len(node_pool) - len(cartesian.output_nodes) - 1):
            # convert index to node_addr in cartesian graph and mutate
            node_addr = index + len(cartesian.input_nodes)
            gene_index = self.mutate_function_node(node_addr, cartesian)
            result = {
                "mutated_node": "FUNC_NODE",
                "node_addr": node_addr,
                "gene_index": gene_index
            }

        # mutate output node
        else:
            # convert index to output node index and mutate
            node_index = index - (len(cartesian.func_nodes) - 1)
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
