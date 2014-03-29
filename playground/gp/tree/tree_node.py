#!/usr/bin/env python


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
