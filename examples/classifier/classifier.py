#!/usr/bin/env python2
import sys
import os
import time
import random
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.play as play
from playground.config import load_data
from playground.gp.tree.generator import TreeGenerator
from playground.gp.tree.evaluation import default_stop_func
from playground.gp.tree.evaluation import print_func
from playground.gp.tree.classifier_evaluation import evaluate
from playground.gp.tree.editor import edit_trees
from playground.selection import Selection
from playground.gp.tree.crossover import TreeCrossover
from playground.gp.tree.mutation import TreeMutation
from playground.gp.functions import GPFunctionRegistry

# SETTINGS
record_exception = False
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
config_fp = os.path.join(script_path, "sine_config.json")
# config_fp = os.path.join(script_path, "simple_test_func_4-config.json")


def traverse_tree(node, graph, origin=None):
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


if __name__ == "__main__":
    try:
        # setup
        random.seed(10)  # seed random so results can be reproduced
        config = {
            "max_population": 500,
            "max_generation": 20,
            "stale_limit": 10,

            "tree_generation": {
                "tree_type": "CLASSIFICATION_TREE",
                "method": "RAMPED_HALF_AND_HALF_METHOD",
                "depth_ranges": [
                    {"size": 4, "percentage": 0.25},
                    {"size": 3, "percentage": 0.25},
                    {"size": 2, "percentage": 0.25},
                    {"size": 1, "percentage": 0.25}
                ]
            },

            "evaluator": {
                "use_cache": True
            },

            "selection": {
                "method": "TOURNAMENT_SELECTION",
                "tournament_size": 10
            },

            "crossover": {
                "method": "POINT_CROSSOVER",
                "probability": 0.9
            },

            "mutation": {
                "methods": [
                    "POINT_MUTATION"
                ],
                "probability": 0.8
            },

            "function_nodes": [
                {
                    "type": "CLASS_FUNCTION",
                    "name": "GREATER_THAN",
                    "arity": 2,

                    "data_range": {
                        "lower_bound": 0.0,
                        "upper_bound": 10.0,
                        "decimal_places": 1,
                    }
                },
                {
                    "type": "CLASS_FUNCTION",
                    "name": "LESS_THAN",
                    "arity": 2,

                    "data_range": {
                        "lower_bound": 0.0,
                        "upper_bound": 10.0,
                        "decimal_places": 1,
                    }
                },
                {
                    "type": "CLASS_FUNCTION",
                    "name": "EQUALS",
                    "arity": 2,

                    "data_range": {
                        "lower_bound": 0.0,
                        "upper_bound": 10.0,
                        "decimal_places": 1
                    }
                }
            ],

            "terminal_nodes": [
                {
                    "type": "RANDOM_CONSTANT",
                    "name": "species",
                    "range": [
                        1.0,
                        2.0,
                        3.0
                    ]
                },
            ],

            "class_attributes": [
                "sepal_length",
                "sepal_width",
                "petal_length",
                "petal_width"
            ],

            "data_file": "data/iris.dat",
            "input_variables": [
                {"name": "sepal_length"},
                {"name": "sepal_width"},
                {"name": "petal_length"},
                {"name": "petal_width"}
            ],
            "response_variables": [{"name": "species"}]
        }
        load_data(config, script_path)
        functions = GPFunctionRegistry("CLASSIFICATION")
        generator = TreeGenerator(config)

        # genetic operators
        selection = Selection(config)
        crossover = TreeCrossover(config)
        mutation = TreeMutation(config)

        # run symbolic regression
        population = generator.init()

        start_time = time.time()
        details = play.play_details(
            population=population,
            evaluate=evaluate,
            functions=functions,
            selection=selection,
            crossover=crossover,
            mutation=mutation,
            print_func=print_func,
            stop_func=default_stop_func,
            config=config,
            editor=edit_trees,
        )
        play.play(details)

        import networkx as nx
        import matplotlib.pyplot as plt
        best = population.best_individuals[0]

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
        plt.show()

        end_time = time.time()
        print "GP run took: %2.2fsecs\n" % (end_time - start_time)

    except Exception as err:
        print err
        print traceback.print_exc()
