#!/usr/bin/env python
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeParser
from playground.functions import FunctionExecutionError


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
            score = self.eval_program(tree.program, tree.size)
            tree.score = score

        except EvaluationError:
            raise
