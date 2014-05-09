#!/usr/bin/env python2
from sympy import simplify

from playground.gp.tree import TreeNode
from playground.gp.tree import TreeNodeType
from playground.gp.tree.parser import TreeParser
from playground.gp.functions import EvaluationError


def print_func(population, generation):
    # display best individual
    parser = TreeParser()
    best_individuals = population.find_best_individuals()
    best = None
    if len(best_individuals):
        best = best_individuals[0]

    print "generation:", generation
    if best:
        print "best_score:", str(best.score)
        print "tree_size:", str(best.size)
    else:
        print "No valid trees in this generation"

    # best individual
    if best:
        print "best:", parser.parse_equation(best.root)
        if best.score < 20.0:
            eq = parser.parse_equation(best.root)
            if best.size < 20:
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

        # population diversity
        p = []
        for i in population.individuals:
            p.append(str(i))
        p = set(p)
        diversity = (len(p) / float(len(population.individuals))) * 100
        diversity = round(diversity, 2)
        print "population diversity:", str(diversity) + "%"
    print ""


def default_stop_func(popualtion, stats, config):
    max_gen = config["max_generation"]
    stale_limit = config.get("stale_limit", 10)
    stop_score = config.get("stop_score", None)
    curr_best = stats["all_time_best"]
    curr_best_score = None if curr_best is None else curr_best.score
    stop = False

    if stats["generation"] >= max_gen:
        stop = True

    if stats["stale_counter"] >= stale_limit:
        stop = True

    if stop_score is not None:
        if curr_best_score is not None and stop_score >= curr_best_score:
            stop = True

    return stop


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
        response_var = config["response_variables"][0]["name"]
        response_data = config["data"][response_var]
        rows = len(response_data)
        result = []

        # pre-check
        if len(config["response_variables"]) > 1:
            err = "Tree evaluation only supports 1 response variable!"
            raise RuntimeError(err)

        # evaluate tree
        for i in xrange(rows):
            # evaluate program
            for node in tree.program:
                eval_node(node, stack, functions, config, i)

            # calculate score
            node = stack.pop()
            result.append(node.value)
            err += pow(response_data[i] - node.value, 2)

            # reset stack
            del stack[:]

        # calculate fitness score
        score = err + (tree_size * 0.1)

        return score, result

    except EvaluationError:
        return None, None

    except OverflowError:
        return None, None


def record_eval(recorder, **kwargs):
    use_cache = kwargs["use_cache"]
    cache = kwargs.get("cache", None)
    cache_size = kwargs.get("cache_size", None)
    match_cached = kwargs.get("match_cached", None)
    trees_evaluated = kwargs.get("trees_evaluated", None)
    tree_nodes_evaluated = kwargs.get("tree_nodes_evaluated", None)
    diversity = kwargs.get("diversity", None)

    if use_cache:
        eval_stats = {
            "cache": cache,
            "cache_size": cache_size,
            "match_cached": match_cached,
            "trees_evaluated": trees_evaluated,
            "tree_nodes_evaluated": tree_nodes_evaluated,
            "diversity": diversity
        }
    else:
        eval_stats = {
            "trees_evaluated": trees_evaluated,
            "tree_nodes_evaluated": tree_nodes_evaluated
        }
    recorder.record_evaluation(eval_stats)


def filter_trees(trees):
    result = []
    min_size = 2
    max_size = 50
    min_inputs = 1

    for tree in trees:
        valid_tree = True

        if tree.size < min_size:
            valid_tree = False

        if tree.size > max_size:
            valid_tree = False

        if len(tree.input_nodes) < min_inputs:
            valid_tree = False

        if valid_tree:
            result.append(tree)

    return result


def evaluate(trees, functions, config, results, cache={}, recorder=None):
    evaluator_config = config.get("evaluator", None)
    use_cache = evaluator_config.get("use_cache", False)

    best_score = None
    best_result = None
    trees_evaluated = 0
    nodes_evaluated = 0
    match_cached = 0

    # evaluate trees
    for tree in filter_trees(trees):
        score = None
        res = None

        # use cahce?
        if use_cache:
            if str(tree) not in cache:
                score, res = eval_program(
                    tree,
                    tree.size,
                    functions,
                    config
                )
                nodes_evaluated += tree.size
                trees_evaluated += 1
            else:
                score = cache[str(tree)]
                match_cached += 1

        else:
            score, res = eval_program(
                tree,
                tree.size,
                functions,
                config)
            nodes_evaluated += tree.size

        # check result
        if score is not None:
            tree.score = score
            results.append(tree)

            if score < best_score or best_score is None:
                best_score = score
                best_result = res

        # cache tree
        cache[str(tree)] = score

    if recorder:
        # calculate tree diversity
        tree_strings = set([str(tree) for tree in trees])
        diversity = len(tree_strings) / float(len(trees))

        # record evaluation statistics
        record_eval(
            recorder,
            use_cache=use_cache,
            cache=cache,
            cache_size=len(cache),
            match_cached=match_cached,
            trees_evaluated=trees_evaluated,
            tree_nodes_evaluated=nodes_evaluated,
            diversity=diversity
        )

    return best_result
