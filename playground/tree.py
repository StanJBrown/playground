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
        if (node_type == TreeNodeType.UNARY_OP):
            self.name = kwargs.get("name", None)
            self.value_branch = kwargs.get("value_branch", None)
        elif (node_type == TreeNodeType.BINARY_OP):
            self.name = kwargs.get("name", None)
            self.left_branch = kwargs.get("left_branch", None)
            self.right_branch = kwargs.get("right_branch", None)

        # terminal node specific
        if (node_type == TreeNodeType.TERM):
            self.name = kwargs.get("name", None)
            self.value = kwargs.get("value", None)
        elif (node_type == TreeNodeType.INPUT):
            self.name = kwargs.get("name", None)

    def has_value_node(self, node):
        if (self.node_type == TreeNodeType.UNARY_OP):
            if self.value_branch is node:
                return TreeNodeBranch.VALUE
            else:
                return False
        elif (self.node_type == TreeNodeType.BINARY_OP):
            if self.left_branch is node:
                return TreeNodeBranch.LEFT
            elif self.right_branch is node:
                return TreeNodeBranch.RIGHT
            else:
                return False
        else:
            return False


class Tree(object):
    def __init__(self):
        self.root = None
        self.depth = 0
        self.size = 0

        self.program = []
        self.func_nodes = []
        self.term_nodes = []
        self.input_nodes = []

        self.tree_parser = TreeParser()

    def valid(self, config_input_nodes):
        # convert config input nodes from dict to list of TreeNodes
        check_list = []
        for node in config_input_nodes:
            if node["type"] == TreeNodeType.INPUT:
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

    def update_program(self):
        self.program = self.tree_parser.post_order_traverse(self.root)

    def update_func_nodes(self):
        for node in self.program:
            t = node.node_type
            if t == TreeNodeType.UNARY_OP or t == TreeNodeType.BINARY_OP:
                self.func_nodes.append(node)

    def update_term_nodes(self):
        for node in self.program:
            if node.node_type == TreeNodeType.TERM:
                self.term_nodes.append(node)

    def update_input_nodes(self):
        for node in self.program:
            if node.node_type == TreeNodeType.INPUT:
                self.input_nodes.append(node)


class TreeParser(object):
    def _print_node(self, node):
        if hasattr(node, "name") and node.name is None:
            print('"{0}{1}"'.format(node.value, id(node)))
        else:
            print('"{0}{1}"'.format(node.name, id(node)))

    def _print_node_label(self, node):
        if hasattr(node, "name") and node.name is None:
            print('{0}{1}[label="{0}"];'.format(node.value, id(node)))
        else:
            print('{0}{1}[label="{0}"];'.format(node.name, id(node)))

    def _print_relation(self, from_node, to_node, node_list):
        from_node_id = None
        to_node_id = None

        if from_node.name is None:
            from_node_id = from_node.value
        else:
            from_node_id = from_node.name

        if to_node.name is None:
            to_node_id = to_node.value
        else:
            to_node_id = to_node.name

        print(
            '"{0}{1}" -> "{2}{3}";'.format(
                from_node_id,
                id(from_node),
                to_node_id,
                id(to_node)
            )
        )

        node_list.append(to_node)

    def _print_tree_structure(self, node, node_list):
        if node.node_type == TreeNodeType.UNARY_OP:
            # value
            self._print_relation(node, node.value_branch, node_list)
            self._print_tree_structure(node.value_branch, node_list)
        elif node.node_type == TreeNodeType.BINARY_OP:
            # left
            self._print_relation(node, node.left_branch, node_list)
            self._print_tree_structure(node.left_branch, node_list)

            # right
            self._print_relation(node, node.right_branch, node_list)
            self._print_tree_structure(node.right_branch, node_list)

    def print_tree(self, root_node):
        node_list = []
        node_list.append(root_node)
        self._print_tree_structure(root_node, node_list)

        for node in node_list:
            self._print_node_label(node)

    def post_order_traverse(self, node, stack=None):
        stack = stack if stack is not None else []
        n_type = node.node_type

        if n_type == TreeNodeType.TERM or n_type == TreeNodeType.INPUT:
            stack.append(node)
        elif n_type == TreeNodeType.UNARY_OP:
            self.post_order_traverse(node.value_branch, stack)
            stack.append(node)
        elif n_type == TreeNodeType.BINARY_OP:
            self.post_order_traverse(node.left_branch, stack)
            self.post_order_traverse(node.right_branch, stack)
            stack.append(node)

        return stack
