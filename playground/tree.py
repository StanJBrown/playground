#!/usr/bin/env python
from playground.functions import FunctionExecutionError


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


class Tree(object):
    def __init__(self):
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

    def replace_node(self, target_node, replace_with, override_update=False):
        linked_node = self.get_linked_node(target_node)
        branch = linked_node.has_value_node(target_node)

        if branch == TreeNodeBranch.VALUE:
            linked_node.value_branch = replace_with
        elif branch == TreeNodeBranch.LEFT:
            linked_node.left_branch = replace_with
        elif branch == TreeNodeBranch.RIGHT:
            linked_node.right_branch = replace_with

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
            t = node.node_type
            if t == TreeNodeType.UNARY_OP or t == TreeNodeType.BINARY_OP:
                if node is not self.root:
                    self.func_nodes.append(node)

    def update_term_nodes(self):
        del self.term_nodes[:]
        for node in self.program:
            if node.node_type == TreeNodeType.TERM:
                self.term_nodes.append(node)

    def update_input_nodes(self):
        del self.input_nodes[:]
        for node in self.program:
            if node.node_type == TreeNodeType.INPUT:
                self.input_nodes.append(node)

    def update_tree_info(self):
        self.size = len(self.program)
        self.branches = len(self.term_nodes) + len(self.input_nodes)

    def update(self):
        self.program = self.tree_parser.parse_tree(self, self.root)

    def __str__(self):
        return self.tree_parser.parse_equation(self.root)


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

    def parse_tree(self, tree, node, depth=None, stack=None):
        if depth is None and stack is None:
            depth = 0
            stack = []

            tree.size = 0
            tree.depth = 0
            tree.branches = 1
            tree.open_branches = 1
            del tree.func_nodes[:]
            del tree.term_nodes[:]
            del tree.input_nodes[:]

        if node.node_type == TreeNodeType.TERM:
            tree.size += 1
            tree.open_branches -= 1
            tree.term_nodes.append(node)

            stack.append(node)

        elif node.node_type == TreeNodeType.INPUT:
            tree.size += 1
            tree.open_branches -= 1
            tree.input_nodes.append(node)

            stack.append(node)

        elif node.node_type == TreeNodeType.UNARY_OP:
            self.parse_tree(tree, node.value_branch, depth + 1, stack)

            tree.size += 1
            if node is not tree.root:
                tree.func_nodes.append(node)

            stack.append(node)

        elif node.node_type == TreeNodeType.BINARY_OP:
            self.parse_tree(tree, node.left_branch, depth + 1, stack)
            self.parse_tree(tree, node.right_branch, depth + 1, stack)

            tree.size += 1
            tree.branches += 1
            tree.open_branches += 1
            if node is not tree.root:
                tree.func_nodes.append(node)

            stack.append(node)

        tree.depth = depth if depth > tree.depth else tree.depth
        return stack

    def parse_equation(self, node, eq_str=None):
        eq_str = eq_str if eq_str is not None else ""
        n_type = node.node_type

        if n_type == TreeNodeType.TERM or n_type == TreeNodeType.INPUT:
            if node.name is not None:
                eq_str += node.name
            else:
                eq_str += str(node.value)

        elif n_type == TreeNodeType.UNARY_OP:
            eq_str += "("
            eq_str += node.name
            eq_str += "("
            eq_str = self.parse_equation(node.value_branch, eq_str)
            eq_str += ")"
            eq_str += ")"

        elif n_type == TreeNodeType.BINARY_OP:
            eq_str += "("
            eq_str = self.parse_equation(node.left_branch, eq_str)
            eq_str += " " + node.name + " "
            eq_str = self.parse_equation(node.right_branch, eq_str)
            eq_str += ")"

        eq_str = eq_str.replace("ADD", "+")
        eq_str = eq_str.replace("SUB", "-")
        eq_str = eq_str.replace("MUL", "*")
        eq_str = eq_str.replace("DIV", "/")
        eq_str = eq_str.replace("COS", "cos")
        eq_str = eq_str.replace("SIN", "sin")

        return eq_str


class EvaluationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class TreeEvaluator(object):
    def __init__(self, config, function_registry):
        self.config = config
        self.functions = function_registry
        self.tree_parser = TreeParser()

        evaluator_config = config.get("evaluator", None)
        if evaluator_config is not None:
            self.use_cache = evaluator_config.get("use_cache", False)
            self.cache = {}

        self.match_cached = 0

    def _gen_term_node(self, node, row):
        try:
            value = self.config["data"][node.name][row]
            term_node = TreeNode(TreeNodeType.TERM, value=value)
            return term_node
        except KeyError:
            print node.name, row

    def eval_func(self, variables, data):
        node = variables.get("node", None)
        response_data = variables.get("response_data", None)
        tree_size = variables.get("tree_size", None)
        rows = len(response_data)

        sse = 0.0
        score = 0.0
        for i in range(rows):
            sse += pow(node.value - response_data[i], 2)
            score = sse + (tree_size * 0.1)

        return score

    def eval_node(self, node, stack):
        try:
            if node.node_type == TreeNodeType.TERM:
                stack.append(node)

            elif node.node_type == TreeNodeType.UNARY_OP:
                value = stack.pop()

                function = self.functions.get_function(node.name)
                result_value = function(value.value)
                result = TreeNode(TreeNodeType.TERM, value=result_value)

                stack.append(result)

            elif node.node_type == TreeNodeType.BINARY_OP:
                left = stack.pop()
                right = stack.pop()

                function = self.functions.get_function(node.name)
                result_value = function(left.value, right.value)
                result = TreeNode(TreeNodeType.TERM, value=result_value)

                stack.append(result)

        except FunctionExecutionError as e:
            raise EvaluationError(e.message)

    def eval_program(self, program, tree_size):
        try:
            stack = []
            sse = 0.0  # squared sum error
            score = 0.0
            response_var = self.config["response_variable"]["name"]
            response_data = self.config["data"][response_var]
            rows = len(response_data)

            for i in range(rows):
                for node in program:
                    if node.node_type == TreeNodeType.INPUT:
                        term_node = self._gen_term_node(node, i)
                        self.eval_node(term_node, stack)
                    else:
                        self.eval_node(node, stack)

                # calculate score
                node = stack.pop()
                sse += pow(node.value - response_data[i], 2)
                score = sse + (tree_size * 0.1)

                # reset stack
                del stack[:]

            return score

        except EvaluationError:
            raise

    def eval_sub_tree(self, node, overall_tree_size):
        sub_program = self.tree_parser.post_order_traverse(node)
        score = self.eval_program(sub_program, overall_tree_size)
        return score

    def evaluate(self, tree):
        try:
            if self.use_cache:
                if str(tree) not in self.cache:
                    score = self.eval_program(tree.program, tree.size)
                    tree.score = score
                    self.cache[str(tree)] = score
                else:
                    tree.score = self.cache[str(tree)]
                    self.match_cached += 1
            else:
                tree.score = self.eval_program(tree.program, tree.size)

        except EvaluationError:
            raise
