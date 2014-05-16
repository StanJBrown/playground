#!/usr/bin/env python2
from playground.gp.tree.parser import TreeParser


class NodeType(object):
    FUNCTION = "FUNCTION"
    CLASS_FUNCTION = "CLASS_FUNCTION"

    CONSTANT = "CONSTANT"
    RANDOM_CONSTANT = "RANDOM_CONSTANT"

    INPUT = "INPUT"


class Node(object):
    def __init__(self, node_type, **kwargs):
        self.node_type = node_type

        # FUNCTION node specific
        if node_type == NodeType.FUNCTION:
            self.name = kwargs.get("name", None)
            self.arity = kwargs.get("arity", None)
            self.branches = kwargs.get("branches", None)

        # CLASS_FUNCTION node specific
        if node_type == NodeType.CLASS_FUNCTION:
            self.name = kwargs.get("name", None)
            self.class_attribute = kwargs.get("class_attribute", None)
            self.arity = kwargs.get("arity", None)
            self.branches = kwargs.get("branches", None)
            self.value = kwargs.get("value", None)

        # CONSTANT node specific
        if node_type == NodeType.CONSTANT:
            self.name = kwargs.get("name", None)
            self.value = kwargs.get("value", None)

        # INPUT node specific
        elif node_type == NodeType.INPUT:
            self.name = kwargs.get("name", None)

    def has_value_node(self, node):
        if self.is_function() or self.is_class_function():
            index = 0
            for value in self.branches:
                if value is node:
                    return index
                else:
                    index += 1

            return False

        else:
            return False

    def is_function(self):
        if self.node_type == NodeType.FUNCTION:
            return True
        else:
            return False

    def is_class_function(self):
        if self.node_type == NodeType.CLASS_FUNCTION:
            return True
        else:
            return False

    def is_constant(self):
        if self.node_type == NodeType.CONSTANT:
            return True
        else:
            return False

    def is_input(self):
        if self.node_type == NodeType.INPUT:
            return True
        else:
            return False

    def is_terminal(self):
        if self.is_input() or self.is_constant():
            return True
        else:
            return False

    def equals(self, node):
        if self.node_type == node.node_type:

            if node.is_function() or node.is_class_function():
                if self.name == node.name:
                    return True
                else:
                    return False

            elif node.is_constant():
                if self.value == node.value:
                    return True
                else:
                    return False

            elif node.is_input():
                if self.name == node.name:
                    return True
                else:
                    return False
        else:
            return False

    def __str__(self):
        obj_str = self.node_type + " "

        if self.is_function():
            obj_str += "name: " + self.name + " "
            obj_str += "address: " + str(id(self))

        elif self.is_class_function():
            obj_str += "name: " + self.name + " "
            obj_str += "address: " + str(id(self))

        elif self.is_constant():
            if self.name is not None:
                obj_str += "name: " + self.name + " "
                obj_str += "value: " + str(self.value) + " "
                obj_str += "address: " + str(id(self))
            else:
                obj_str += "value: " + str(self.value) + " "
                obj_str += "address: " + str(id(self))

        elif self.is_input():
            obj_str += "name: " + self.name + " "
            obj_str += "address: " + str(id(self))

        return obj_str


class Tree(object):
    def __init__(self):
        self.tree_id = None
        self.score = None
        self.tree_type = None

        self.root = None
        self.depth = 0
        self.size = 0

        self.program = []
        self.func_nodes = []
        self.term_nodes = []
        self.input_nodes = []

        self.parser = TreeParser()

    def valid(self, config_input_nodes):
        # convert config input nodes from dict to list of Nodes
        check_list = []
        for node in config_input_nodes:
            check_list.append(node["name"])

        # convert tree input nodes
        tree_input_nodes = []
        for node in self.input_nodes:
            tree_input_nodes.append(node.name)

        result = set(check_list) - set(tree_input_nodes)
        if len(list(result)) == 0:
            return True
        else:
            return False

    def get_linked_node(self, target_node):
        try:
            index = self.program.index(target_node) + 1

            for node in self.program[index:]:
                if node.has_value_node(target_node) is not False:
                    return node
        except ValueError:
            return None

    def replace_node(self, target_node, replace_with, override_update=False):
        linked_node = self.get_linked_node(target_node)
        branch_index = linked_node.has_value_node(target_node)
        linked_node.branches[branch_index] = replace_with

        if override_update is False:
            self.update()

    def equals(self, tree):
        if len(self.program) != len(tree.program):
            return False

        index = 0
        for node in self.program:
            equals = node.equals(tree.program[index])
            if equals is False:
                return False
            index += 1

        return True

    def update_program(self):
        del self.program[:]
        self.program = self.parser.post_order_traverse(self.root)

    def update_func_nodes(self):
        del self.func_nodes[:]
        for node in self.program:
            if node.is_function():
                if node is not self.root:
                    self.func_nodes.append(node)

    def update_term_nodes(self):
        del self.term_nodes[:]
        for node in self.program:
            if node.is_terminal():
                self.term_nodes.append(node)

    def update_input_nodes(self):
        del self.input_nodes[:]
        for node in self.program:
            if node.is_input():
                self.input_nodes.append(node)

    def update_tree_info(self):
        self.size = len(self.program)
        self.branches = len(self.term_nodes) + len(self.input_nodes)

    def update(self):
        self.program = self.parser.parse_tree(self, self.root)

    def __str__(self):
        if self.tree_type == "CLASSIFICATION_TREE":
            return self.parser.parse_classification_tree(self.root)
        else:
            return self.parser.parse_equation(self.root)

    def to_dict(self):
        self_dict = {
            "id": id(self),
            "score": self.score,

            "size": self.size,
            "depth": self.depth,

            "func_nodes_len": len(self.func_nodes),
            "term_nodes_len": len(self.term_nodes),
            "input_nodes_len": len(self.input_nodes),

            "func_nodes": [str(node) for node in self.func_nodes],
            "term_nodes": [str(node) for node in self.term_nodes],
            "input_nodes": [str(node) for node in self.input_nodes],

            "program": str(self)
        }
        return self_dict
