#!/usr/bin/env python
from playground.gp_tree.tree_node import TreeNode
from playground.gp_tree.tree_node import TreeNodeType
from playground.gp_tree.tree_node import TreeNodeBranch
from playground.gp_tree.tree_parser import TreeParser
from playground.functions import EvaluationError


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

        except EvaluationError:
            raise

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
