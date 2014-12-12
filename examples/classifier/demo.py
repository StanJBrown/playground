#!/usr/bin/env python
import os
import sys
import math
import random
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import numpy as np
import matplotlib.pylab as plt
import matplotlib.colors as plt_colors

from sklearn import svm
from sklearn import tree
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import auc
from sklearn.metrics import roc_curve

from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB

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


def simple_test_data(data_size=1000, show_plot=False):
    x = np.random.uniform(0.0, 1.0, data_size)
    y = np.random.uniform(0.0, 1.0, data_size)

    # points will lie noisily in one class if point is inside
    # imaginary circle centered at zero with radius 0.5. and
    # in another class if outside
    categories = []
    for i in range(data_size):
        noise = np.random.uniform(-0.02, 0.02, 1)[0]
        radius_sq = x[i] ** 2 + y[i] ** 2 + noise
        radius = math.sqrt(radius_sq) if radius_sq > 0 else 0

        if radius > 0.2:
            categories.append(1)
        else:
            categories.append(0)

    # actual test classification circle that seperates the two
    # categories
    circle_x = []
    circle_y = []
    for pt_x in np.arange(0.0, 0.6, 0.001):
        try:
            circle_y.append(math.sqrt(0.2 ** 2 - pt_x ** 2))
            circle_x.append(pt_x)
        except ValueError:
            pass
    solution = (circle_x, circle_y)

    # plot data
    if show_plot:
        color_map = np.array(['r', 'g'])

        plt.scatter(x, y, c=color_map[categories])
        plt.plot(circle_x, circle_y, linewidth=3.0)

        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])

        plt.show()

    data = np.array(zip(x, y))
    return (data, categories, solution)


def compute_roc(solution, predicted, method):
    fpr, tpr, thresholds = roc_curve(solution, predicted)
    roc_auc = auc(fpr, tpr)
    print "[%s] area under the ROC curve: %f" % (method, roc_auc)

    hits = 0
    for i in range(len(solution)):
        if solution[i] == round(predicted[i]):
            hits += 1
    print "hits:", hits
    print "percentage:", hits / float(len(solution))
    print ""

    return (fpr, tpr, roc_auc)


def svm_predict(train_data, test_data, train_cat, xx, yy):
    # SVM CLASSIFIER
    svm_classifier = svm.SVC(kernel="rbf", probability=True)
    svm_fit = svm_classifier.fit(train_data, train_cat)

    predicted = svm_fit.predict_proba(test_data)

    contour = svm_fit.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    contour = contour.reshape(xx.shape)

    return predicted[:, 1], contour


def dt_predict(train_data, test_data, train_cat, xx, yy):
    # DECISION TREE CLASSIFIER
    dt_classifier = tree.DecisionTreeClassifier()
    dt_fit = dt_classifier.fit(train_data, train_cat)

    predicted = dt_fit.predict(test_data)

    contour = dt_fit.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    contour = contour.reshape(xx.shape)

    return predicted, contour


def rf_predict(train_data, test_data, train_cat, xx, yy):
    # RANDOM FOREST CLASSIFIER
    rf_classifier = RandomForestClassifier()

    rf_fit = rf_classifier.fit(train_data, train_cat)
    predicted = rf_fit.predict(test_data)

    contour = rf_fit.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    contour = contour.reshape(xx.shape)

    return predicted, contour


def kn_predict(train_data, test_data, train_cat, xx, yy):
    # K-NEAREST NEIGHBOUR CLASSIFIER
    kn_classifier = KNeighborsClassifier()

    kn_fit = kn_classifier.fit(train_data, train_cat)
    predicted = kn_fit.predict(test_data)

    contour = kn_fit.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    contour = contour.reshape(xx.shape)

    return predicted, contour


def ada_predict(train_data, test_data, train_cat, xx, yy):
    # ADA CLASSIFIER
    ada_classifier = AdaBoostClassifier()

    ada_fit = ada_classifier.fit(train_data, train_cat)
    predicted = ada_fit.predict(test_data)

    contour = ada_fit.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    contour = contour.reshape(xx.shape)

    return predicted, contour


def lda_predict(train_data, test_data, train_cat, xx, yy):
    # LDA CLASSIFIER
    lda_classifier = LDA()

    lda_fit = lda_classifier.fit(train_data, train_cat)
    predicted = lda_fit.predict(test_data)

    contour = lda_fit.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    contour = contour.reshape(xx.shape)

    return predicted, contour


def qda_predict(train_data, test_data, train_cat, xx, yy):
    # QDA CLASSIFIER
    qda_classifier = QDA()

    qda_fit = qda_classifier.fit(train_data, train_cat)
    predicted = qda_fit.predict(test_data)

    contour = qda_fit.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    contour = contour.reshape(xx.shape)

    return predicted, contour


def nb_predict(train_data, test_data, train_cat, xx, yy):
    # NAIVE BAYES CLASSIFIER
    nb_classifier = GaussianNB()

    nb_fit = nb_classifier.fit(train_data, train_cat)
    predicted = nb_fit.predict(test_data)

    contour = nb_fit.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    contour = contour.reshape(xx.shape)

    return predicted, contour


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


def gp_predict(train_data, test_data, train_cat, xx, yy):
    # setup
    config = {
        "max_population": 800,
        "max_generation": 30,
        "stale_limit": 10,

        "tree_generation": {
            "tree_type": "CLASSIFICATION_TREE",
            "method": "RAMPED_HALF_AND_HALF_METHOD",
            "depth_ranges": [
                {"size": 1, "percentage": 1.0}
            ]
        },

        "evaluator": {"use_cache": True},

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
            "probability": 0.8
        },

        "function_nodes": [
            {
                "type": "CLASS_FUNCTION",
                "name": "GREATER_THAN",
                "arity": 2,

                "data_range": {
                    "lower_bound": -1.0,
                    "upper_bound": 1.0,
                    "decimal_places": 2,
                }
            },
            {
                "type": "CLASS_FUNCTION",
                "name": "LESS_THAN",
                "arity": 2,

                "data_range": {
                    "lower_bound": -1.0,
                    "upper_bound": 1.0,
                    "decimal_places": 2,
                }
            },
            {
                "type": "CLASS_FUNCTION",
                "name": "EQUALS",
                "arity": 2,

                "data_range": {
                    "lower_bound": -1.0,
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
    # gp_plot_dt(best_tree, True)

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

    # load test data
    config["data"] = {}
    config["data"]["rows"] = xx.shape[0] * xx.shape[1]
    config["data"]["x"] = np.reshape(xx, xx.shape[0] * xx.shape[1])
    config["data"]["y"] = np.reshape(yy, yy.shape[0] * yy.shape[1])

    contour = gp_eval.predict_tree(best_tree, functions, config)
    contour = np.array(contour)
    contour = contour.reshape(xx.shape)

    return predicted, contour


def plot_roc(test_cat, plot_data, savefig=False):
    # Plot ROC curve
    plt.clf()
    results = []

    # calcualte and sort labels by roc_auc
    for method, method_results in plot_data.items():
        fpr, tpr, roc_auc = compute_roc(test_cat, method_results, method)
        label = "[%s] area = %0.2f" % (method, roc_auc)
        res = {"label": label, "fpr": fpr, "tpr": tpr, "roc_auc": roc_auc}
        results.append(res)
    results = sorted(results, key=lambda k: k['roc_auc'], reverse=True)

    # plot according to roc_auc ranking
    for r in results:
        plt.plot(r["fpr"], r["tpr"], label=r["label"])

    plt.title('Receiver Operating Characteristic Curve (ROC)')
    plt.legend(loc="lower right")
    plt.plot([0, 1], [0, 1], 'k--')

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])

    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    if savefig:
        plt.savefig("classifiers_roc.png")

    plt.show()


def plot_decision_contour(data, categories, xx, yy, contours, labels):
    cm = plt.cm.RdBu
    cm_bright = plt_colors.ListedColormap(['#FF0000', '#0000FF'])

    f, axarr = plt.subplots(1, len(contours))

    for index in range(len(contours)):
        contour = contours[index]

        axarr[index].set_title(labels[index])
        axarr[index].autoscale_view(True, True, True)

        axarr[index].contourf(xx, yy, contour, cmap=cm, alpha=0.8)
        axarr[index].scatter(
            data[:, 0],
            data[:, 1],
            c=categories,
            cmap=cm_bright
        )

    plt.show()


if __name__ == "__main__":
    # seed random so results can be reproduced
    random.seed(0)
    np.random.seed(0)

    # create test data
    # data, categories, solution = simple_test_data(1000)
    data, categories = datasets.make_circles(
        noise=0.2,
        factor=0.5,
        random_state=1
    )
    # data, categories = datasets.make_moons(noise=0.2, random_state=1)

    x_min, x_max = data[:, 0].min() - .5, data[:, 0].max() + .5
    y_min, y_max = data[:, 1].min() - .5, data[:, 1].max() + .5
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, 0.02),
        np.arange(y_min, y_max, 0.02)
    )

    # shuffle and split training and test sets
    n_samples, features = data.shape
    data, categories = shuffle(data, categories)
    half = int(n_samples / 2)
    train_data, test_data = data[:half], data[half:]
    train_cat, test_cat = categories[:half], categories[half:]

    # classifiers
    svm_pred, svm_dc = svm_predict(train_data, test_data, train_cat, xx, yy)
    dt_pred, dt_dc = dt_predict(train_data, test_data, train_cat, xx, yy)
    rf_pred, rf_dc = rf_predict(train_data, test_data, train_cat, xx, yy)
    kn_pred, kn_dc = kn_predict(train_data, test_data, train_cat, xx, yy)
    ada_pred, ada_dc = ada_predict(train_data, test_data, train_cat, xx, yy)
    lda_pred, lda_dc = lda_predict(train_data, test_data, train_cat, xx, yy)
    qda_pred, qda_dc = qda_predict(train_data, test_data, train_cat, xx, yy)
    nb_pred, nb_dc = nb_predict(train_data, test_data, train_cat, xx, yy)
    gp_pred, gp_dc = gp_predict(train_data, test_data, train_cat, xx, yy)

    contours = [
        svm_dc,
        dt_dc,
        rf_dc,
        kn_dc,
        ada_dc,
        lda_dc,
        qda_dc,
        nb_dc,
        gp_dc
    ]
    labels = [
        "SVM",
        "DT",
        "RF",
        "KN",
        "ADA",
        "LDA",
        "QDA",
        "NB",
        "GP"
    ]
    plot_decision_contour(data, categories, xx, yy, contours, labels)

    # plot roc curves
    plot_data = {
        "SVM": svm_pred,
        "DT": dt_pred,
        "RF": rf_pred,
        "KN": kn_pred,
        "ADA": ada_pred,
        "LDA": lda_pred,
        "QDA": qda_pred,
        "NB": nb_pred,
        "GP": gp_pred
    }
    plot_roc(test_cat, plot_data)
