#!/usr/bin/env python
from playground.functions import EvaluationError
from playground.gp_tree.tree_node import TreeNode
from playground.gp_tree.tree_node import TreeNodeType


def gen_term_node(node, row, config):
    try:
        value = config["data"][node.name][row]
        term_node = TreeNode(TreeNodeType.TERM, value=value)
        return term_node
    except KeyError:
        print node.name, row


def eval_node(node, stack, functions, config, data_row=None):
    try:
        if node.is_terminal():
            stack.append(node)

        if node.is_input():
            term_node = gen_term_node(node, data_row, config)
            stack.append(term_node)

        elif node.is_function():
            # get input values from stack
            input_values = [stack.pop().value for i in xrange(node.arity)]

            # execute function
            function = functions.get_function(node.name)
            result_value = function(*input_values)
            result = TreeNode(TreeNodeType.TERM, value=result_value)

            # push result back to stack
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

        for i in xrange(rows):
            # evaluate program
            for node in tree.program:
                eval_node(node, stack, functions, config, i)

            # calculate score
            node = stack.pop()
            sse += pow(node.value - response_data[i], 2)
            score = sse + (tree_size * 0.1)

            # reset stack
            del stack[:]

        return score

    except EvaluationError:
        return None


def evaluate(trees, functions, config, results, **kwargs):
    recorder = kwargs.get("recorder", None)
    evaluator_config = config.get("evaluator", None)
    cache = {}
    match_cached = 0
    cached = 0

    # evaluate trees
    if evaluator_config.get("use_cache"):
        for tree in trees:
            if str(tree) not in cache:
                score = eval_program(tree, tree.size, functions, config)

                if score is not None:
                    tree.score = score
                    results.append(tree)

                cache[str(tree)] = score
                cached += 1

            else:
                score = cache[str(tree)]

                if score is not None:
                    tree.score = score
                    results.append(tree)

                match_cached += 1
    else:
        for tree in trees:
            score = eval_program(tree, tree.size, functions, config)
            if score is not None:
                tree.score = score
                results.append(tree)

    # record evaluation statistics
    if recorder:
        if evaluator_config.get("use_cache"):
            eval_stats = {
                "cache": cache,
                "cache_size": cached,
                "match_cached": match_cached,
                "evaluated": (len(trees) - match_cached)
            }
        else:
            eval_stats = {
                "evaluated": len(trees)
            }
        recorder.record_evaluation(eval_stats)

