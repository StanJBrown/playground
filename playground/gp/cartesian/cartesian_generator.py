#!/usr/bin/env python2
from random import randint
from random import sample

from playground.gp.cartesian.cartesian import Cartesian
from playground.population import Population


class CartesianGenerator(object):
    def __init__(self, config):
        self.config = config
        self.address_grid = self.build_address_grid()

    def build_address_grid(self):
        grid = []
        cols = self.config["cartesian"]["columns"]
        rows = self.config["cartesian"]["rows"]

        grid += [range(self.config["cartesian"]["num_inputs"])]

        addr_counter = self.config["cartesian"]["num_inputs"]
        for c in range(cols):
            column = [addr_counter + r for r in range(rows)]
            addr_counter += rows
            grid.append(column)

        return grid

    def calculate_column_level(self, node_addr):
        cols = self.config["cartesian"]["columns"]
        rows = self.config["cartesian"]["rows"]
        num_inputs = self.config["cartesian"]["num_inputs"]

        # pre-check
        if node_addr >= (cols * rows) + num_inputs:
            err = "Error! Invalid address [{0}]!".format(node_addr)
            raise RuntimeError(err)

        elif node_addr < num_inputs:
            err = "Error! calculate_column_level() not for input addresses!"
            raise RuntimeError(err)

        # calculate which level the address belongs
        for col_index in range(1, len(self.address_grid)):
            for addr in self.address_grid[col_index]:
                if node_addr == addr:
                    return col_index - 1

    def get_valid_addresses(self, from_level):
        cols = self.config["cartesian"]["columns"]
        l_back = self.config["cartesian"]["levels_back"]

        # pre-check
        if from_level > (cols - 1) or from_level < 0:
            err = "Error! Invalid level [{0}]!".format(from_level)
            raise RuntimeError(err)

        if from_level == 0:
            return self.address_grid[0]

        else:
            min_level = 0 if from_level - l_back < 0 else from_level - l_back
            max_level = from_level + 1

            valid_addrs = []
            for level in self.address_grid[min_level:max_level]:
                for addr in level:
                    valid_addrs.append(addr)

            return valid_addrs

    def gen_random_conn_gene(self, from_addr, target_node="FUNC_NODE"):
        if target_node == "FUNC_NODE":
            col_level = self.calculate_column_level(from_addr)
            valid_addrs = self.get_valid_addresses(col_level)
            gene = sample(valid_addrs, 1)[0]

            return gene

        elif target_node == "OUTPUT_NODE":
            cols = self.config["cartesian"]["columns"]
            rows = self.config["cartesian"]["rows"]
            num_inputs = self.config["cartesian"]["num_inputs"]
            max_addr = ((cols * rows) + num_inputs) - 1

            gene = randint(0, max_addr)

            return gene

        else:
            err = "Error! Invalid target node [{0}]!".format(target_node)
            raise RuntimeError(err)

    def gen_random_func_gene(self):
        gene = randint(0, len(self.config["function_nodes"]) - 1)
        return gene

    def gen_random_func_node(self, node_addr):
        func_index = randint(0, len(self.config["function_nodes"]) - 1)
        arity = self.config["function_nodes"][func_index]["arity"]
        conns = [self.gen_random_conn_gene(node_addr) for i in range(arity)]

        return [func_index] + conns

    def gen_random_output_node(self):
        rows = self.config["cartesian"]["rows"]
        columns = self.config["cartesian"]["columns"]
        max_addr = rows * columns - 1

        return self.gen_random_conn_gene(max_addr, "OUTPUT_NODE")

    def prep_input_nodes(self):
        inputs = self.config["input_variables"]

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

        num_inputs = self.config["cartesian"]["num_inputs"]
        num_outputs = self.config["cartesian"]["num_outputs"]
        num_funcs = (rows * columns)

        # function nodes
        func_nodes = []
        for i in range(num_funcs):
            func_nodes.append(self.gen_random_func_node(i + num_inputs))

        # output nodes
        output_nodes = []
        for i in range(num_outputs):
            output_nodes.append(self.gen_random_output_node())

        # input nodes
        input_nodes = self.prep_input_nodes()

        # create new cartesian obj
        return Cartesian(
            config=self.config,
            rows=self.config["cartesian"]["rows"],
            columns=self.config["cartesian"]["columns"],
            levels_back=self.config["cartesian"]["levels_back"],
            func_nodes=func_nodes,
            input_nodes=input_nodes,
            output_nodes=output_nodes
        )

    def init(self):
        pop = Population(self.config)
        max_pop = self.config["max_population"]

        # create cartesians
        for i in range(max_pop):
            pop.individuals.append(self.generate_new_cartesian())

        return pop
