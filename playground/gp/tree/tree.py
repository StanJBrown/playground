#!/usr/bin/env python
from playground.gp.tree.tree_parser import TreeParser


class TreeNodeType(object):
    FUNCTION = "FUNCTION"
    TERM = "TERM"
    INPUT = "INPUT"


class TreeNode(object):
    def __init__(self, node_type, **kwargs):
        self.node_type = node_type

        # function node specific
        if node_type == TreeNodeType.FUNCTION:
            self.name = kwargs.get("name", None)
            self.arity = kwargs.get("arity", None)
            self.branches = kwargs.get("branches", None)

        # terminal node specific
        if node_type == TreeNodeType.TERM:
            self.name = kwargs.get("name", None)
            self.value = kwargs.get("value", None)

        elif node_type == TreeNodeType.INPUT:
            self.name = kwargs.get("name", None)

    def has_value_node(self, node):
        if self.is_function():
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
        if self.node_type == TreeNodeType.FUNCTION:
            return True
        else:
            return False

    def is_terminal(self):
        if self.node_type == TreeNodeType.TERM:
            return True
        else:
            return False

    def is_input(self):
        if self.node_type == TreeNodeType.INPUT:
            return True
        else:
            return False

    def equals(self, node):
        if self.node_type == node.node_type:

            if node.is_function():
                if self.name == node.name:
                    return True
                else:
                    return False

            elif node.is_terminal():
                if self.name == node.name and self.value == node.value:
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
        elif self.is_terminal():
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
#
#     def __dict__(self):
#         node_dict = {}
#
#         node_dict["node_type"] = self.node_type
#
#         # function node specific
#         if self.node_type == TreeNodeType.UNARY_OP:
#             node_dict["name"] = self.name
#             node_dict["value_branch"] = self.value_branch.__dict__()
#         elif self.node_type == TreeNodeType.BINARY_OP:
#             node_dict["name"] = self.name
#             node_dict["left_branch"] = self.left_branch.__dict__()
#             node_dict["right_branch"] = self.right_branch.__dict__()
#
#         # terminal node specific
#         if self.node_type == TreeNodeType.TERM:
#             node_dict["name"] = self.name
#             node_dict["value"] = self.value
#         elif self.node_type == TreeNodeType.INPUT:
#             node_dict["name"] = self.name
#
#         return node_dict


class Tree(object):
    def __init__(self):
        self.tree_id = None
        self.score = None

        self.root = None
        self.depth = 0
        self.size = 0

        self.branches = 1
        self.open_branches = 1

        self.program = []
        self.func_nodes = []
        self.term_nodes = []
        self.input_nodes = []

        self.tree_parser = TreeParser()

    def valid(self, config_input_nodes):
        # convert config input nodes from dict to list of TreeNodes
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
        self.program = self.tree_parser.post_order_traverse(self.root)

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
        self.program = self.tree_parser.parse_tree(self, self.root)

    def __str__(self):
        return self.tree_parser.parse_equation(self.root)

    def to_dict(self):
        self_dict = {
            "id": id(self),
            "score": self.score,

            "size": self.size,
            "depth": self.depth,
            "branches": self.branches,

            "func_nodes_len": len(self.func_nodes),
            "term_nodes_len": len(self.term_nodes),
            "input_nodes_len": len(self.input_nodes),

            "func_nodes": [str(node) for node in self.func_nodes],
            "term_nodes": [str(node) for node in self.term_nodes],
            "input_nodes": [str(node) for node in self.input_nodes],

            "program": str(self)
        }
        return self_dict
