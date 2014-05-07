#!/usr/bin/env python2


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
    curr_best = stats["current_best"]
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


def traverse(cartesian, node_addr, functions, output, visited, config):
    # pre-check
    if node_addr < len(cartesian.input_nodes):
        return

    # get current node
    node = cartesian.graph()[node_addr]

    # traverse children first
    conn_genes = node[1:]
    for conn in conn_genes:
        traverse(cartesian, conn, functions, output, visited, config)

    # traverse root node
    if node_addr not in visited:
        # evaluate function with data
        node_output = eval_node(node, conn_genes, functions, output, config)

        # record node output and append node index to visited
        output[node_addr] = node_output
        visited.append(node_addr)


def evaluate_cartesian(cartesian, functions, config):
    visited = []
    results = []
    output = {}
    output_node_data = []
    sse = None

    try:
        # prep output with input data
        for i in range(len(cartesian.input_nodes)):
            output[i] = cartesian.input_nodes[i]

        # for node in output_nodes:
        for output_node_index in range(len(cartesian.output_nodes)):
            node_addr = cartesian.output_nodes[output_node_index]
            traverse(cartesian, node_addr, functions, output, visited, config)
            results.append(output[node_addr])

            # get output from node
            del output_node_data[:]
            if node_addr < len(cartesian.input_nodes):
                input_name = cartesian.input_nodes[node_addr]
                output_node_data = config["data"][input_name]
            else:
                output_node_data = output[node_addr]

            # get training data to compare
            resp_var = config["response_variables"][output_node_index]["name"]
            resp_data = config["data"][resp_var]

            # calculate sum squared error (SSE)
            sse = 0
            for i in range(len(resp_data)):
                sse += pow(abs(output_node_data[i] - resp_data[i]), 2)
                # if abs(output_node_data[i] - resp_data[i]) > 0.1:
                #     sse += 1
            # sse += len(cartesian.program())

    except:
        pass

    return (sse, output_node_data)


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
    # evaluator_config = config.get("evaluator", None)
    use_cache = True

    best_score = None
    best_output = None
    cartesians_evaluated = 0
    nodes_evaluated = 0
    match_cached = 0

    # evaluate cartesians
    for cartesian in cartesians:
        score = None
        output = None

        # use cahce?
        if use_cache:
            if str(cartesian) not in cache:
                score, output = evaluate_cartesian(
                    cartesian,
                    functions,
                    config
                )
                nodes_evaluated += cartesian.rows * cartesian.columns
                cartesians_evaluated += 1

            else:
                cached_record = cache[str(cartesian)]
                score = cached_record["score"]
                output = cached_record["output"]
                match_cached += 1

        else:
            score, output = evaluate_cartesian(cartesian, functions, config)
            nodes_evaluated += cartesian.size

        # check result
        if score is not None:
            cartesian.score = score
            results.append(cartesian)

            if score <= best_score or best_score is None:
                best_score = score
                best_output = output

        # cache cartesian
        cache[str(cartesian)] = {"score": score, "output": output}

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

    return best_output
