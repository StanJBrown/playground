#!/usr/bin/env python
import os
import sys
import math
import random
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import numpy as np
import matplotlib.pylab as plt

from sklearn import svm
from sklearn import tree
from sklearn.utils import shuffle
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
from sklearn.ensemble import RandomForestClassifier

import playground.play as play
import playground.gp.tree.classifier_evaluation as gp_eval
from playground.gp.tree.generator import TreeGenerator
from playground.gp.tree.evaluation import default_stop_func
from playground.gp.tree.evaluation import print_func
from playground.gp.tree.classifier_evaluation import evaluate
from playground.gp.tree.editor import edit_trees
from playground.selection import Selection
from playground.gp.tree.crossover import TreeCrossover
from playground.gp.tree.mutation import TreeMutation
from playground.gp.functions import GPFunctionRegistry


def test_data(data_size=1000, show_plot=False):
    x = np.random.uniform(0.0, 1.0, data_size)
    y = np.random.uniform(0.0, 1.0, data_size)

    # points will lie noisily in one class if point is inside
    # imaginary circle centered at zero with radius 0.5. and
    # in another class if outside
    categories = []
    for i in range(data_size):
        noise = np.random.uniform(-0.15, 0.15, 1)[0]
        radius = math.sqrt(abs(x[i] ** 2 + y[i] ** 2 + noise))

        if radius > 0.5:
            categories.append(1)
        else:
            categories.append(0)

    # actual test classification circle that seperates the two
    # categories
    circle_x = []
    circle_y = []
    for pt_x in np.arange(0.0, 0.6, 0.001):
        try:
            circle_y.append(math.sqrt(0.5 ** 2 - pt_x ** 2))
            circle_x.append(pt_x)
        except ValueError:
            pass
    solution = (circle_x, circle_y)

    # plot data
    if show_plot:
        color_map = np.array(['r', 'g', 'b'])
        plt.scatter(x, y, c=color_map[categories])
        plt.plot(circle_x, circle_y, linewidth=3.0)
        plt.show()

    return (x, y, categories, solution)


def compute_roc(solution, predicted, method):
    fpr, tpr, thresholds = roc_curve(solution, predicted)
    roc_auc = auc(fpr, tpr)
    print "[%s] area under the ROC curve: %f" % (method, roc_auc)

    return (fpr, tpr, roc_auc)


def svm_predict(train_data, test_data, train_cat):
    # SVM CLASSIFIER
    svm_classifier = svm.SVC(kernel="poly", probability=True)
    svm_fit = svm_classifier.fit(train_data, train_cat)
    predicted = svm_fit.predict_proba(test_data)

    return predicted[:, 1]


def dt_predict(train_data, test_data, train_cat):
    # DECISION TREE CLASSIFIER
    dt_classifier = tree.DecisionTreeClassifier()
    dt_fit = dt_classifier.fit(train_data, train_cat)
    predicted = dt_fit.predict(test_data)

    return predicted


def rf_predict(train_data, test_data, train_cat):
    # RANDOM FOREST CLASSIFIER
    rf_classifier = RandomForestClassifier()
    rf_fit = rf_classifier.fit(train_data, train_cat)
    predicted = rf_fit.predict(test_data)

    return predicted


def gp_traverse_tree(node, graph, origin=None):
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
            gp_traverse_tree(child, graph, node_id)

    elif node.is_terminal():
        node_id = id(node)
        label = "{0} = {1}".format(node.name, node.value)
        graph.add_node(node_id, label=label)

    if origin:
        graph.add_edge(origin, node_id)


def gp_plot_dt(best_tree, savefig=False):
    import networkx as nx
    import matplotlib.pyplot as plt

    graph = nx.DiGraph()
    gp_traverse_tree(best_tree.root, graph)
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

    if savefig:
        plt.savefig("gp_tree.png")

    plt.show()


def gp_predict(train_data, test_data, train_cat):
    # setup
    config = {
        "max_population": 800,
        "max_generation": 50,
        "stale_limit": 10,

        "tree_generation": {
            "tree_type": "CLASSIFICATION_TREE",
            "method": "RAMPED_HALF_AND_HALF_METHOD",
            "depth_ranges": [
                {"size": 4, "percentage": 0.10},
                {"size": 3, "percentage": 0.10},
                {"size": 2, "percentage": 0.30},
                {"size": 1, "percentage": 0.50}
            ]
        },

        "evaluator": {
            "use_cache": True
        },

        "selection": {
            "method": "TOURNAMENT_SELECTION",
            "tournament_size": 100
        },

        "crossover": {
            "method": "POINT_CROSSOVER",
            "probability": 0.8
        },

        "mutation": {
            "methods": [
                "SUBTREE_MUTATION"
            ],
            "probability": 0.2
        },

        "function_nodes": [
            {
                "type": "CLASS_FUNCTION",
                "name": "GREATER_THAN",
                "arity": 2,

                "data_range": {
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "decimal_places": 2,
                }
            },
            {
                "type": "CLASS_FUNCTION",
                "name": "LESS_THAN",
                "arity": 2,

                "data_range": {
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "decimal_places": 2,
                }
            },
            {
                "type": "CLASS_FUNCTION",
                "name": "EQUALS",
                "arity": 2,

                "data_range": {
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "decimal_places": 2
                }
            }
        ],

        "terminal_nodes": [
            {
                "type": "RANDOM_CONSTANT",
                "name": "category",
                "range": [
                    0.0,
                    1.0
                ]
            },
        ],

        "class_attributes": [
            "x",
            "y"
        ],

        "input_variables": [
            {"name": "x"},
            {"name": "y"}
        ],
        "response_variables": [{"name": "category"}]
    }

    # load data
    config["data"] = {}
    config["data"]["rows"] = len(train_data)
    config["data"]["x"] = []
    config["data"]["y"] = []
    config["data"]["category"] = train_cat
    for row in train_data:
        config["data"]["x"].append(row[0])
        config["data"]["y"].append(row[1])

    functions = GPFunctionRegistry("CLASSIFICATION")
    generator = TreeGenerator(config)

    # genetic operators
    selection = Selection(config)
    crossover = TreeCrossover(config)
    mutation = TreeMutation(config)

    # run symbolic regression
    population = generator.init()

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

    best_tree = population.best_individuals[0]
    gp_plot_dt(best_tree, True)

    # load test data
    config["data"] = {}
    config["data"]["rows"] = len(test_data)
    config["data"]["x"] = []
    config["data"]["y"] = []
    for row in test_data:
        config["data"]["x"].append(row[0])
        config["data"]["y"].append(row[1])

    # predict
    predicted = gp_eval.predict_tree(best_tree, functions, config)
    return predicted


def plot_roc(test_cat, plot_data, savefig=False):
    # Plot ROC curve
    plt.clf()

    for method, method_results in plot_data.items():
        fpr, tpr, roc_auc = compute_roc(test_cat, method_results, method)
        label = "[%s] ROC curve (area = %0.2f)" % (method, roc_auc)
        plt.plot(fpr, tpr, label=label)

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])

    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    plt.title('Receiver Operating Characteristic Curve (ROC)')
    plt.legend(loc="lower right")

    if savefig:
        plt.savefig("classifiers_roc.png")

    plt.show()


if __name__ == "__main__":
    # seed random so results can be reproduced
    random.seed(0)
    np.random.seed(0)

    # create test data
    x, y, categories, solution = test_data()
    data = np.array(zip(x, y))

    # shuffle and split training and test sets
    n_samples, features = data.shape
    data, categories = shuffle(data, categories)
    half = int(n_samples / 2)

    train_data, test_data = data[:half], data[half:]
    train_cat, test_cat = categories[:half], categories[half:]

    # classifiers
    svm_predicted = svm_predict(train_data, test_data, train_cat)
    dt_predicted = dt_predict(train_data, test_data, train_cat)
    rf_predicted = rf_predict(train_data, test_data, train_cat)
    gp_predicted = gp_predict(train_data, test_data, train_cat)

    # plot roc curves
    plot_data = {
        "SVM": svm_predicted,
        "DT": dt_predicted,
        "RF": rf_predicted,
        "GP": gp_predicted
    }
    plot_roc(test_cat, plot_data, True)
