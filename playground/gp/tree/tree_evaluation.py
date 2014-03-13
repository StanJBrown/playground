#!/usr/bin/env python
from sympy import simplify

from playground.gp.functions import EvaluationError
from playground.gp.tree.tree_node import TreeNode
from playground.gp.tree.tree_node import TreeNodeType
from playground.gp.tree.tree_parser import TreeParser


def print_func(population, generation):
    # display best individual
    tree_parser = TreeParser()
    best = population.find_best_individuals()[0]
    print "generation:", generation
    print "best_score:", str(best.score)
    print "tree_size:", str(best.size)

    print "best:", tree_parser.parse_equation(best.root)
    if best.score < 20.0:
        eq = tree_parser.parse_equation(best.root)
        if best.size < 50:
            eq = eq.replace("ADD", "+")
            eq = eq.replace("SUB", "-")
            eq = eq.replace("MUL", "*")
            eq = eq.replace("DIV", "/")
            eq = eq.replace("POW", "**")
            eq = eq.replace("SIN", "sin")
            eq = eq.replace("COS", "cos")
            eq = eq.replace("RAD", "rad")
            eq = eq.replace("LN", "ln")
            eq = eq.replace("LOG", "log")
            print "EQ SIMPLIFIED:", simplify(eq)
    print


def default_stop_func(popualtion, general_stats, config):
    max_gen = config["max_generation"]
    stale_limit = config.get("stale_limit", 100)

    if general_stats["generation"] >= max_gen:
        return True

    elif general_stats["stale_counter"] >= stale_limit:
        return True

    elif config.get("stop_score", None):
        if config["stop_score"] <= general_stats["best"].score:
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
        err = 0.0  # sum squared error
        score = 0.0
        response_var = config["response_variable"]["name"]
        response_data = config["data"][response_var]
        rows = len(response_data)
        result = []

        for i in xrange(rows):
            # evaluate program
            for node in tree.program:
                eval_node(node, stack, functions, config, i)

            # calculate score
            node = stack.pop()
            result.append(node.value)
            err += abs(response_data[i] - node.value)

            # reset stack
            del stack[:]

        score = (err / rows) + (tree_size * 0.1)
        return score, result

    except EvaluationError:
        # print "FAILED TO EVAL[EVALERR]:", tree
        return None, None

    except OverflowError:
        # print "FAILED TO EVAL[OVERFLOW]:", tree

        # import traceback
        # traceback.print_exc()

        # import sys
        # sys.exit(-1)

        return None, None


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


def evaluate(trees, functions, config, results, cache={}, recorder=None):
    evaluator_config = config.get("evaluator", None)
    use_cache = evaluator_config.get("use_cache", False)
    nodes_evaluated = 0
    match_cached = 0

    best_score = None
    best_result = None

    # evaluate trees
    for tree in trees:
        score = None
        res = None

        # use cahce?
        if use_cache:
            if str(tree) not in cache:
                score, res = eval_program(tree, tree.size, functions, config)
                nodes_evaluated += tree.size
            else:
                score = cache[str(tree)]
        else:
            score, res = eval_program(tree, tree.size, functions, config)
            nodes_evaluated += tree.size

        # check result
        if score is not None:
            tree.score = score
            results.append(tree)

            if score < best_score or best_score is None:
                best_score = score
                best_result = res

        cache[str(tree)] = score

    # record evaluation statistics
    if recorder:
        record_eval(
            recorder,
            use_cache=use_cache,
            cache=cache,
            cache_size=len(cache),
            match_cached=match_cached,
            trees_evaluated=len(trees) - match_cached,
            tree_nodes_evaluated=len(trees)
        )

    return best_result
