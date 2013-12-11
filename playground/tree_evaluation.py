#!/usr/bin/env python
from playground.functions import EvaluationError
from playground.tree import TreeNode
from playground.tree import TreeNodeType


def gen_term_node(node, row, config):
    try:
        value = config["data"][node.name][row]
        term_node = TreeNode(TreeNodeType.TERM, value=value)
        return term_node
    except KeyError:
        print node.name, row


def eval_node(node, stack, functions, config):
    try:
        if node.node_type == TreeNodeType.TERM:
            stack.append(node)

        elif node.node_type == TreeNodeType.UNARY_OP:
            value = stack.pop()

            function = functions.get_function(node.name)
            result_value = function(value.value)
            result = TreeNode(TreeNodeType.TERM, value=result_value)

            stack.append(result)

        elif node.node_type == TreeNodeType.BINARY_OP:
            left = stack.pop()
            right = stack.pop()

            function = functions.get_function(node.name)
            result_value = function(left.value, right.value)
            result = TreeNode(TreeNodeType.TERM, value=result_value)

            stack.append(result)

    except EvaluationError:
        raise


def eval_program(tree, tree_size, functions, config):
    try:
        stack = []
        sse = 0.0  # squared sum error
        score = 0.0
        response_var = config["response_variable"]["name"]
        response_data = config["data"][response_var]
        rows = len(response_data)

        for i in range(rows):
            for node in tree.program:
                if node.node_type == TreeNodeType.INPUT:
                    term_node = gen_term_node(node, i, config)
                    eval_node(term_node, stack, functions, config)
                else:
                    eval_node(node, stack, functions, config)

            # calculate score
            node = stack.pop()
            sse += pow(node.value - response_data[i], 2)
            score = sse + (tree_size * 0.1)

            # reset stack
            del stack[:]

        return score

    except EvaluationError:
        return None


def evaluate(trees, functions, config, cache, results):
    try:
        evaluator_config = config["evaluator"]
        match_cached = 0
        cached = 0

        if evaluator_config["use_cache"]:
            for tree in trees:
                if str(tree) not in cache:
                    score = eval_program(tree, tree.size, functions, config)
                    results[str(id(tree))] = score
                    cache[str(tree)] = score
                    cached += 1
                else:
                    score = cache[str(tree)]
                    results[str(id(tree))] = score
                    match_cached += 1
        else:
            for tree in trees:
                eval_program(tree, tree.size, functions, config, results)

    except EvaluationError:
        pass
