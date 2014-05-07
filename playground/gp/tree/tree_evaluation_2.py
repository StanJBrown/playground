#!/usr/bin/env python2
import math


def generate_eq_function(tree, functions, config):
    eq = str(tree)

    # replace function node names with python equivalents
    for key, val in functions.items():
        eq = eq.replace(key, val)

    # prep input variables
    input_vars = []
    for var in config["input_variables"]:
        input_vars.append(var["name"])

    # prep evaluation string
    eval_str = "lambda " + ", ".join(input_vars) + ": " + eq

    return eval(eval_str)


def eval_tree(tree, functions, config):
    eq_func = generate_eq_function(tree, functions, config)
    data = config["data"]

    response_var = config["response_variables"][0]["name"]
    response_data = config["data"][response_var]
    input_vars = [i["name"] for i in config["input_variables"]]
    rows = len(response_data)
    residual = []

    # pre-check
    if len(config["response_variables"]) > 1:
        err = "Tree evaulation only supports 1 response varaiable!"
        raise RuntimeError(err)

    # evaluate tree
    try:
        for i in xrange(rows):
            # get expected output and input
            expected_output = response_data[i]
            args = [data[var][i] for var in input_vars]

            # evaluate
            eq_output = float(eq_func(*args))
            residual.append(eq_output - expected_output)

        # sum of squared errors
        sse = sum([pow(r, 2) for r in residual])
        score = sse + (tree.size * 0.1)

        return score

    except:
        return None


def filter_trees(trees):
    result = []
    min_size = 2
    max_size = 50

    for tree in trees:
        if tree.size > min_size and tree.size < max_size:
            result.append(tree)

    return result


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


def evaluate(trees, functions, config, results, cache={}, recorder=None):
    evaluator_config = config.get("evaluator", None)
    use_cache = evaluator_config.get("use_cache", False)

    best_score = None
    trees_evaluated = 0
    nodes_evaluated = 0
    match_cached = 0

    # evaluate trees
    for tree in filter_trees(trees):
        score = None

        # use cahce?
        if use_cache:
            if str(tree) not in cache:
                score = eval_tree(tree, functions, config)
                nodes_evaluated += tree.size
                trees_evaluated += 1
            else:
                score = cache[str(tree)]
                match_cached += 1

        else:
            score = eval_tree(tree, functions, config)
            nodes_evaluated += tree.size

        # update result
        if score is not None:
            tree.score = score
            results.append(tree)

            # update best_score
            if score < best_score or best_score is None:
                best_score = score

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
