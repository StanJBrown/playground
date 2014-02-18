#!/usr/bin/env python
import os
import json

import matplotlib.pyplot as plt


def parse_data_file(data_fp):
    generations = []

    data_file = open(data_fp, "r")
    for line in data_file:
        generations.append(json.loads(line))

    return generations


def parse_generation_best_scores(generations):
    best_scores = []

    for g in generations:
        best_scores.append(g["population"]["best_score"])

    return best_scores


def parse_generation_best_individuals(generations):
    best_individuals = []

    for g in generations:
        best_individuals.append(g["population"]["best_individuals"])

    return best_individuals


def parse_all_time_best_scores(generations, reverse=False):
    best_scores = []
    curr_best = None
    best = generations[0]["population"]["best_score"]

    for g in generations:
        curr_best = g["population"]["best_score"]

        if reverse:
            if curr_best > best:
                best = curr_best
        else:
            if curr_best < best:
                best = curr_best
        best_scores.append(best)

    return best_scores


def parse_all_time_best_individuals(generations, reverse=False):
    best_individuals = []
    curr_best_score = None
    curr_best_individual = None
    best_score = generations[0]["population"]["best_score"]
    best_individual = generations[0]["population"]["best_individual"]

    for g in generations:
        curr_best_score = g["population"]["best_score"]
        curr_best_individual = g["population"]["best_individual"]

        if reverse:
            if curr_best_score > best_score:
                best_score = curr_best_score
                best_individual = curr_best_individual
        else:
            if curr_best_score < best_score:
                best_score = curr_best_score
                best_individual = curr_best_individual
        best_individuals.append(best_individual)

    return best_individuals


def parse_evaluation_stats(generations):
    cache_size = []
    matched_cache = []
    trees_evaluated = []
    result = {
        "cache_size": cache_size,
        "matched_cache": matched_cache,
        "trees_evaluated": trees_evaluated
    }

    for g in generations:
        cache_size.append(g["evaluation"][0]["cache_size"])
        matched_cache.append(g["evaluation"][0]["match_cached"])
        trees_evaluated.append(g["evaluation"][0]["trees_evaluated"])

    return result


def plot_generation_best_scores(generations, **kwargs):
    font = {
        "family": "serif",
        "color": "black",
        "weight": "normal",
        "size": 14
    }

    # graph labels
    plt.title("Generation Best Score vs Generations", fontdict=font)
    plt.xlabel("Generation", fontdict=font)
    plt.ylabel("Generation Best Score", fontdict=font)

    # graph data
    best_scores = parse_generation_best_scores(generations)
    gens = range(0, len(best_scores))

    # plot graph
    plt.plot(gens, best_scores)

    if kwargs.get("show_graph", False):
        # show graph
        plt.show()

    if kwargs.get("save_fig", False):
        # save graph
        plt.savefig(kwargs.get("fig_path", "graph.png"))


def plot_all_time_best_scores(generations, **kwargs):
    font = {
        "family": "serif",
        "color": "black",
        "weight": "normal",
        "size": 14
    }

    # graph labels
    plt.title("Best Score vs Generations", fontdict=font)
    plt.xlabel("Generation", fontdict=font)
    plt.ylabel("Best Score", fontdict=font)

    # graph data
    best_scores = parse_all_time_best_scores(generations)
    gens = range(0, len(best_scores))

    # plot graph
    plt.plot(gens, best_scores)

    if kwargs.get("show_graph", False):
        # show graph
        plt.show()

    if kwargs.get("save_fig", False):
        # save graph
        plt.savefig(kwargs.get("fig_path", "graph.png"))


def plot_evaluation_stats(generations, **kwargs):
    font = {
        "family": "serif",
        "color": "black",
        "weight": "normal",
        "size": 14
    }

    # graph data
    stats = parse_evaluation_stats(generations)
    gens = range(0, len(stats["cache_size"]))

    # plot graph
    print stats["cache_size"]
    plt.plot(gens, stats["cache_size"])
    plt.plot(gens, stats["matched_cache"])
    plt.plot(gens, stats["trees_evaluated"])

    # graph labels
    plt.title("Evauation Statistics", fontdict=font)
    plt.xlabel("Generation", fontdict=font)
    plt.legend(["cache size", "matched cache", "evaluated"], loc="upper left")

    if kwargs.get("show_graph", False):
        # show graph
        plt.show()

    if kwargs.get("save_fig", False):
        # save graph
        plt.savefig(kwargs.get("fig_path", "graph.png"))


if __name__ == "__main__":
    data_dir = "/tmp/data"
    data_file = "np_sweep_400_0.1_0.1-0.dat"
    data_path = os.path.join(data_dir, data_file)

    generations = parse_data_file(data_path)
    # plot_evaluation_stats(generations, show_graph=True)
    # plot_all_time_best_scores(generations, show_graph=True)
    # plot_generation_best_scores(generations, show_graph=True)
