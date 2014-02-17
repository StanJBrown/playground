#!/usr/bin/env python
from sympy import simplify

from playground.functions import EvaluationError
from playground.gp.tree.tree_node import TreeNode
from playground.gp.tree.tree_node import TreeNodeType
from playground.gp.tree.tree_parser import TreeParser


def print_func(population, generation):
    # display best individual
    tree_parser = TreeParser()
    best = population.find_best_individuals()[0]
    print "generation: ", generation
    print "best_score: " + str(best.score)
    print "tree_size: " + str(best.size)
    print ""

    if best.score < 20.0:
        eq = tree_parser.parse_equation(best.root)
        if best.size < 50:
            print simplify(eq)
        print ""


def default_stop_func(general_stats, config):
    max_gen = config["max_generation"]
    stale_limit = config.get("stale_limit", 30)

    if general_stats["generation"] >= max_gen:
        return True
    elif general_stats["stale_counter"] >= stale_limit:
        return True

    return False


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

        elif node.is_input():
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


def record_eval(recorder, **kwargs):
    use_cache = kwargs["use_cache"]
    cache = kwargs.get("cache", None)
    cache_size = kwargs.get("cache_size", None)
    match_cached = kwargs.get("match_cached", None)
    trees_evaluated = kwargs.get("trees_evaluated", None)
    tree_nodes_evaluated = kwargs.get("tree_nodes_evaluated", None)

    if use_cache:
        eval_stats = {
            "cache": cache,
            "cache_size": cache_size,
            "match_cached": match_cached,
            "trees_evaluated": trees_evaluated,
            "tree_nodes_evaluated": tree_nodes_evaluated
        }
    else:
        eval_stats = {
            "trees_evaluated": trees_evaluated,
            "tree_nodes_evaluated": tree_nodes_evaluated
        }
    recorder.record_evaluation(eval_stats)


def evaluate(trees, functions, config, results, recorder=None):
    evaluator_config = config.get("evaluator", None)
    use_cache = evaluator_config.get("use_cache", False)
    cache = {}
    cache_size = 0
    match_cached = 0
    nodes_evaluated = 0

    # evaluate trees
    for tree in trees:
        if use_cache:
            if str(tree) not in cache:
                score = eval_program(tree, tree.size, functions, config)
                if score is not None:
                    tree.score = score
                    results.append(tree)
                cache[str(tree)] = score
                cache_size += 1
                nodes_evaluated += tree.size

            else:
                score = cache[str(tree)]
                if score is not None:
                    tree.score = score
                    results.append(tree)
                match_cached += 1
                nodes_evaluated += tree.size

        else:
            score = eval_program(tree, tree.size, functions, config)
            if score is not None:
                tree.score = score
                results.append(tree)
                nodes_evaluated += tree.size

    # record evaluation statistics
    if recorder:
        record_eval(
            recorder,
            use_cache=use_cache,
            cache=cache,
            cache_size=cache_size,
            match_cached=match_cached,
            trees_evaluated=len(trees) - match_cached,
            tree_nodes_evaluated=len(trees)
        )
