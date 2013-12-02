#!/usr/bin/env python
from playground.tree import TreeNode
from playground.tree import TreeNodeType
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

    def _gen_term_node(self, node, row):
        value = self.config["data"][node.name][row]
        term_node = TreeNode(TreeNodeType.TERM, value=value)
        return term_node

    def _eval_node(self, node, stack):
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

    def eval_program(self, tree):
        try:
            stack = []
            sse = 0.0  # squared sum error
            response_var = self.config["response_variable"]["name"]
            response_data = self.config["data"][response_var]
            rows = len(response_data)

            for i in range(rows):
                for node in tree.program:
                    if node.node_type == TreeNodeType.INPUT:
                        term_node = self._gen_term_node(node, i)
                        self._eval_node(term_node, stack)
                    else:
                        self._eval_node(node, stack)

                # accumulate squared sum error
                node = stack.pop()
                sse += pow(node.value - response_data[i], 2)

                # reset stack
                del stack[:]

            return sse

        except EvaluationError:
            raise

    def evaluate(self, tree):
        try:
            sse = self.eval_program(tree)
            tree.score = sse

        except EvaluationError:
            raise
