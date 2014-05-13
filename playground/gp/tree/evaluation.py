#!/usr/bin/env python2

from playground.gp.tree import TreeNode
from playground.gp.tree import TreeNodeType


def print_func(population, generation):
    # display best individual
    best_individuals = population.find_best_individuals()
    if best_individuals:
        best = best_individuals[0]
        print "generation:", generation
        print "generation_best_score:", str(best.score)

        # best individual
        print "generatio_best:", str(best)

        # population diversity
        p = []
        for i in population.individuals:
            p.append(str(i.graph()))
        p = set(p)
        diversity = (len(p) / float(len(population.individuals))) * 100
        diversity = round(diversity, 2)
        print "population diversity:", str(diversity) + "%"
        print ""

    else:
        print "generation:", generation


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


def evaluate_node(node, stack, functions, config):
    try:
        if node.is_terminal():
            # obtain terminal node data and add to stack
            value = node.value
            node.value = [value for i in range(config["data"]["rows"])]
            stack.append(node)

        elif node.is_input():
            # convert input node to terminal node
            node_data = config["data"][node.name]
            term_node = TreeNode(TreeNodeType.CONSTANT, value=node_data)
            stack.append(term_node)

        elif node.is_function():
            # get input data to function from stack
            input_data = [stack.pop().value for i in xrange(node.arity)]

            # execute function
            function = functions.get_function(node.name)

            function_output = []
            for data_row in zip(*input_data):
                function_output.append(function(*data_row))

            # push result back to stack
            result_node = TreeNode(TreeNodeType.CONSTANT, value=function_output)
            stack.append(result_node)

    except:
        raise


def evaluate_tree(tree, functions, config):
    try:
        stack = []
        score = None
        sse = 0.0  # sum squared error
        response_var = config["response_variables"][0]["name"]
        response_data = config["data"][response_var]

        # pre-check
        if len(config["response_variables"]) > 1:
            err = "Tree evaluation only supports 1 response variable!"
            raise RuntimeError(err)

        # evaluate tree
        for node in tree.program:
            evaluate_node(node, stack, functions, config)

        # calculate sum squared error
        node = stack.pop()
        for i in range(config["data"]["rows"]):
            sse += pow(response_data[i] - node.value[i], 2)

        # calculate fitness score
        score = sse + (tree.size * 0.1)

        return (score, None)

    except:
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


def evaluate(trees, functions, config, results, cache={}, recorder=None):
    use_cache = True
    best_score = None
    best_output = None
    trees_evaluated = 0
    nodes_evaluated = 0
    match_cached = 0

    # evaluate trees
    for tree in trees:
        score = None
        output = None
        tree_string = str(tree)

        # use cahce?
        if use_cache:
            if str(tree) not in cache:
                score, output = evaluate_tree(tree, functions, config)
                nodes_evaluated += tree.size
                trees_evaluated += 1

            else:
                cached_record = cache[str(tree)]
                score = cached_record["score"]
                output = cached_record["output"]
                match_cached += 1

        else:
            score, output = evaluate_tree(tree, functions, config)
            nodes_evaluated += tree.size

        # check result
        if score is not None:
            tree.score = score
            results.append(tree)

            if score <= best_score or best_score is None:
                best_score = score
                best_output = output

        # cache tree
        cache[tree_string] = {"score": score, "output": output}

    if recorder:
        # calculate tree diversity
        unique_trees = set([str(tree) for tree in trees])
        diversity = len(unique_trees) / float(len(trees))

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

    return best_output
