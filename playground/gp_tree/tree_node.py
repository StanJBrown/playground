#!/usr/bin/env python


class TreeNodeType(object):
    UNARY_OP = "UNARY_OP"
    BINARY_OP = "BINARY_OP"
    TERM = "TERM"
    INPUT = "INPUT"


class TreeNodeBranch(object):
    VALUE = "VALUE"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class TreeNode(object):
    def __init__(self, node_type, **kwargs):
        self.node_type = node_type

        # function node specific
        if node_type == TreeNodeType.UNARY_OP:
            self.name = kwargs.get("name", None)
            self.value_branch = kwargs.get("value_branch", None)
        elif node_type == TreeNodeType.BINARY_OP:
            self.name = kwargs.get("name", None)
            self.left_branch = kwargs.get("left_branch", None)
            self.right_branch = kwargs.get("right_branch", None)

        # terminal node specific
        if node_type == TreeNodeType.TERM:
            self.name = kwargs.get("name", None)
            self.value = kwargs.get("value", None)
        elif node_type == TreeNodeType.INPUT:
            self.name = kwargs.get("name", None)

    def has_value_node(self, node):
        if self.node_type == TreeNodeType.UNARY_OP:
            if self.value_branch is node:
                return TreeNodeBranch.VALUE
            else:
                return False
        elif self.node_type == TreeNodeType.BINARY_OP:
            if self.left_branch is node:
                return TreeNodeBranch.LEFT
            elif self.right_branch is node:
                return TreeNodeBranch.RIGHT
            else:
                return False
        else:
            return False

    def is_function(self):
        function_node_types = [TreeNodeType.UNARY_OP, TreeNodeType.BINARY_OP]
        if self.node_type in function_node_types:
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
            t = node.node_type

            if t == TreeNodeType.UNARY_OP or t == TreeNodeType.BINARY_OP:
                if self.name == node.name:
                    return True
                else:
                    return False
            elif t == TreeNodeType.TERM:
                if self.name == node.name and self.value == node.value:
                    return True
                else:
                    return False
            elif t == TreeNodeType.INPUT:
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
