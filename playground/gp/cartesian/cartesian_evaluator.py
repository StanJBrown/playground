#!/usr/bin/env python


def get_arity(node):
    return len(node) - 1


def eval_node(node, conn_genes, functions, data, config):
    arity = len(node[1:])
    function = functions[node[0]]
    num_inputs = config["cartesian"]["num_inputs"]
    rows = config["cartesian"]["rows"]
    columns = config["cartesian"]["columns"]
    max_addr = (rows * columns) + num_inputs - 1

    # prep input data
    node_input = []
    for i in range(arity):
        node_addr = conn_genes[i]

        # node is input
        if node_addr < num_inputs and node_addr >= 0:
            input_var = config["input_variables"][node_addr]["name"]
            node_input.append(config["data"][input_var])

        # node is function
        elif node_addr >= num_inputs:
            node_input.append(data[node_addr])

        # invalid node
        elif node_addr > max_addr:
            err = "Invalid node address [{0}]!".format(node_addr)
            raise RuntimeError(err)

    # evaluate node
    node_output = []
    for data_row in zip(*node_input):
        node_output.append(function(*data_row))

    return node_output


def traverse(cartesian, node_index, functions, output, visited, config):
    # pre-check
    if node_index < len(cartesian.input_nodes):
        return

    # get current node
    node = cartesian.graph()[node_index]

    # check arity first
    conn_genes = node[1:]
    for conn in conn_genes:
        traverse(cartesian, conn, functions, output, visited, config)

    # check root node
    if node_index not in visited:
        # evaluate function with data
        node_output = eval_node(node, conn_genes, functions, output, config)

        # record node output and append node index to visited
        output[node_index] = node_output
        visited.append(node_index)


def evaluate_cartesian(cartesian, functions, config):
    visited = []
    results = []
    output = {}

    # prep output with input data
    for i in range(len(cartesian.input_nodes)):
        output[i] = cartesian.input_nodes[i]

    # for node in output_nodes:
    for node_index in cartesian.output_nodes:
        traverse(cartesian, node_index, functions, output, visited, config)
        results.append(output[node_index])

    return (results, output)


def record_eval(recorder, **kwargs):
    use_cache = kwargs["use_cache"]
    cache = kwargs.get("cache", None)
    cache_size = kwargs.get("cache_size", None)
    match_cached = kwargs.get("match_cached", None)
    cartesians_evaluated = kwargs.get("cartesians_evaluated", None)
    cartesian_nodes_evaluated = kwargs.get("cartesian_nodes_evaluated", None)
    diversity = kwargs.get("diversity", None)

    if use_cache:
        eval_stats = {
            "cache": cache,
            "cache_size": cache_size,
            "match_cached": match_cached,
            "cartesians_evaluated": cartesians_evaluated,
            "cartesian_nodes_evaluated": cartesian_nodes_evaluated,
            "diversity": diversity
        }
    else:
        eval_stats = {
            "cartesians_evaluated": cartesians_evaluated,
            "cartesian_nodes_evaluated": cartesian_nodes_evaluated
        }
    recorder.record_evaluation(eval_stats)


def evaluate(cartesians, functions, config, results, cache={}, recorder=None):
    evaluator_config = config.get("evaluator", None)
    use_cache = evaluator_config.get("use_cache", False)

    best_score = None
    best_result = None
    cartesians_evaluated = 0
    nodes_evaluated = 0
    match_cached = 0

    # evaluate cartesians
    for cartesian in cartesians:
        score = None
        res = None

        # use cahce?
        if use_cache:
            if str(cartesian) not in cache:
                score, res = evaluate_cartesian(cartesian, functions, config)
                nodes_evaluated += cartesian.rows * cartesian.columns
                cartesians_evaluated += 1
            else:
                score = cache[str(cartesian)]
                match_cached += 1

        else:
            score, res = evaluate_cartesian(cartesian, functions, config)
            nodes_evaluated += cartesian.size

        # check result
        if score is not None:
            cartesian.score = score
            results.append(cartesian)

            if score < best_score or best_score is None:
                best_score = score
                best_result = res

        # cache cartesian
        cache[str(cartesian)] = score

    if recorder:
        # calculate cartesian diversity
        cartesian_strings = set([str(cartesian) for cartesian in cartesians])
        diversity = len(cartesian_strings) / float(len(cartesians))

        # record evaluation statistics
        record_eval(
            recorder,
            use_cache=use_cache,
            cache=cache,
            cache_size=len(cache),
            match_cached=match_cached,
            cartesians_evaluated=cartesians_evaluated,
            cartesian_nodes_evaluated=nodes_evaluated,
            diversity=diversity
        )

    return best_result
