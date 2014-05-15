#!/usr/bin/env python2
import math
import pylab as plt


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


def plot_func(play, stats):
    x_axis = play.config["live_plot"]["x-axis"]
    y_axis = play.config["live_plot"]["y-axis"]
    generation = stats["generation"]
    every = play.config["live_plot"].get("every", 100)

    if generation == 0:
        plt.figure(figsize=(10, 8))

    if (generation % every) == 0:
        # obtain data
        x_data = play.config["data"][x_axis]
        y_data = play.config["data"][y_axis]

        # plot graph
        plt.clf()
        plt.plot(x_data, y_data)
        plt.plot(x_data, stats["best_output"])
        plt.draw()
        plt.pause(0.0001)  # very important else plot won't be displayed


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
    output = []
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
            output.append(eq_output)
            residual.append(eq_output - expected_output)

        # sum of squared errors
        sse = sum([pow(r, 2) for r in residual])
        score = sse + (tree.size * 0.1)

        return score, output

    except:
        return None, None


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
    best_output = None

    trees_evaluated = 0
    nodes_evaluated = 0
    match_cached = 0

    # evaluate trees
    for tree in filter_trees(trees):
        score = None
        output = None

        # use cahce?
        if use_cache:
            if str(tree) not in cache:
                score, output = eval_tree(tree, functions, config)
                nodes_evaluated += tree.size
                trees_evaluated += 1
            else:
                cached_record = cache[str(tree)]
                score = cached_record["score"]
                output = cached_record["output"]
                match_cached += 1

        else:
            score, output = eval_tree(tree, functions, config)
            nodes_evaluated += tree.size

        # update result
        if score is not None:
            tree.score = score
            results.append(tree)

            # update best_score
            if score < best_score or best_score is None:
                best_score = score
                best_output = output

        # cache tree
        cache[str(tree)] = {"score": score, "output": output}

    if recorder:
        # calculate tree diversity
        tree_strings = set([str(tree) for tree in trees])
        diversity = len(tree_strings) / float(len(trees))

        # clean up cache
        cache_copy = dict(cache)
        for key in cache_copy:
            score = None

            if "score" in cache_copy[key]:
                score = cache_copy[key]["score"]

            cache_copy[key] = score

        # record evaluation statistics
        record_eval(
            recorder,
            use_cache=use_cache,
            cache=cache_copy,
            cache_size=len(cache_copy),
            match_cached=match_cached,
            trees_evaluated=trees_evaluated,
            tree_nodes_evaluated=nodes_evaluated,
            diversity=diversity
        )

    return best_output
