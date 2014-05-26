#!/usr/bin/env python2
import networkx as nx
import matplotlib.pyplot as plt


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
            p.append(str(i))
        p = set(p)
        diversity = (len(p) / float(len(population.individuals))) * 100
        diversity = round(diversity, 2)
        print "population diversity:", str(diversity) + "%"
        print ""

    else:
        print "generation:", generation


def plot_process_tree(node, graph, origin=None):
    node_id = None

    if node.is_class_function():
        node_id = id(node)
        label = "{0} {1} {2}".format(
            node.class_attribute,
            node.name,
            node.value
        )
        graph.add_node(node_id, label=label)

        for child in node.branches:
            traverse_tree(child, graph, node_id)

    elif node.is_terminal():
        node_id = id(node)
        label = "{0} = {1}".format(node.name, node.value)
        graph.add_node(node_id, label=label)

    if origin:
        graph.add_edge(origin, node_id)


def plot_func(play, stats):
    generation = stats["generation"]
    best = stats["generation_best"]
    every = play.config["live_plot"].get("every", 100)

    if generation == 0:
        plt.figure(figsize=(10, 8))

    if (generation % every) == 0:
        plt.clf()

        # create graph
        graph = nx.DiGraph()
        traverse_tree(best.root, graph)
        labels = dict((n, d["label"]) for n, d in graph.nodes(data=True))

        pos = nx.graphviz_layout(graph, prog='dot')
        nx.draw(
            graph,
            pos,
            with_labels=True,
            labels=labels,
            arrows=False,
            node_shape=None
        )

        # plot graph
        plt.draw()
        plt.pause(0.0001)  # very important else plot won't be displayed


def get_row_data(data, index):
    data_row = {}
    for key in data.keys():
        if key != "rows":
            data_row[key] = data[key][index]

    return data_row


def traverse_tree(node, functions, data):
    if node.is_terminal():
        if node.value == data[node.name]:
            return True
        else:
            return False

    elif node.is_class_function():
        value = node.value
        class_attribute = node.class_attribute

        func = functions.get_function(node.name)
        result = func(value, data[class_attribute])

        if result:
            return traverse_tree(node.branches[0], functions, data)
        else:
            return traverse_tree(node.branches[1], functions, data)


def evaluate_tree(tree, functions, config):
    hits = 0
    output = []
    data = config["data"]
    rows = config["data"]["rows"]

    # go through each data row
    for i in range(rows):
        data_row = get_row_data(data, i)
        result = traverse_tree(tree.root, functions, data_row)

        if result:
            hits += 1

        output.append(result)

    # calcuate score
    score = ((rows - hits) ** 2) + tree.size

    return score, output


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

            else:
                cached_record = cache[str(tree)]
                score = cached_record["score"]
                output = cached_record["output"]
                match_cached += 1

        else:
            score, output = evaluate_tree(tree, functions, config)

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
            diversity=diversity
        )

    return best_output


def predict(node, functions, data):
    if node.is_terminal():
        return node.value

    elif node.is_class_function():
        value = node.value
        class_attribute = node.class_attribute

        func = functions.get_function(node.name)
        result = func(value, data[class_attribute])

        if result:
            return predict(node.branches[0], functions, data)
        else:
            return predict(node.branches[1], functions, data)


def predict_tree(tree, functions, config):
    output = []
    data = config["data"]
    rows = config["data"]["rows"]

    # go through each data row
    for i in range(rows):
        data_row = get_row_data(data, i)
        result = predict(tree.root, functions, data_row)
        output.append(result)

    return output
