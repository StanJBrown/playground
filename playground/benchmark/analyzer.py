#!/usr/bin/env python
import os
import json
import zipfile

# import matplotlib.pyplot as plt


def parse_data(fp):
    generations = []

    try:
        # parse fp
        fp = os.path.expandvars(fp)
        data_file, file_ext = os.path.splitext(fp)
        dirname = os.path.dirname(fp)

        # unpack zip file
        zipped_data = False
        if file_ext == ".zip":
            zipped_data = True
            with zipfile.ZipFile(fp) as zf:
                zf.extractall(dirname)

        # parse data - assumes data file has extension .dat
        data = open(data_file + ".dat", "r")
        for line in data:
            generations.append(json.loads(line))

        # remove extraced zip file
        if zipped_data:
            os.remove(data_file + ".dat")

    except IOError as msg:
        print "ERROR: parse_data() assumes data file has extension .dat!"
        print msg
        raise

    return generations


def summarize_population(population, summary):
    summary["generation"].append(population["generation"])
    summary["best_score"].append(population["best_score"])
    summary["best_individual"].append(population["best_individual"])


def summarize_evaluation(evaluation, summary):
    summary["cache_size"].append(evaluation["cache_size"])
    summary["diversity"].append(evaluation["diversity"])
    summary["matched_cache"].append(evaluation["match_cached"])
    summary["trees_evaluated"].append(evaluation["trees_evaluated"])
    summary["tree_nodes_evaluated"].append(evaluation["tree_nodes_evaluated"])


def summarize_crossover(crossover, summary):
    for key in crossover.iterkeys():
        if key == "crossovers":
            summary[key].append(crossover[key])

        elif key == "no_crossovers":
            summary[key].append(crossover[key])

        elif key not in summary:
            summary[key] = {}
            summary[key]["frequency"] = []
            summary[key]["failed"] = []
            summary[key]["success"] = []

        if key not in ["crossovers", "no_crossovers", "instances"]:
            success = crossover[key]["success"]
            failed = crossover[key]["failed"]
            frequency = crossover[key]["frequency"]

            summary[key]["success"].append(success)
            summary[key]["failed"].append(failed)
            summary[key]["frequency"].append(frequency)


def summarize_mutation(mutation, summary):
    for key in mutation.iterkeys():
        if key == "mutations":
            summary[key].append(mutation[key])

        elif key == "no_mutations":
            summary[key].append(mutation[key])

        elif key not in summary:
            summary[key] = {}
            summary[key]["frequency"] = []
            summary[key]["failed"] = []
            summary[key]["success"] = []

        if key not in ["mutations", "no_mutations", "instances"]:
            success = mutation[key]["success"]
            failed = mutation[key]["failed"]
            frequency = mutation[key]["frequency"]

            summary[key]["success"].append(success)
            summary[key]["failed"].append(failed)
            summary[key]["frequency"].append(frequency)


def summarize_selection(selection, summary):
    sel_method = selection["method"]
    if sel_method not in summary:
        summary[sel_method] = {}
        summary[sel_method]["selected"] = []

    summary[sel_method]["selected"].append(selection["selected"])


def summarize_data(fp):
    stats = {
        # population
        "population": {
            "generation": [],
            "best_score": [],
            "best_individual": []
        },

        # evaluation
        "evaluation": {
            "cache_size": [],
            "diversity": [],
            "matched_cache": [],
            "trees_evaluated": [],
            "tree_nodes_evaluated": []
        },

        # crossover
        "crossover": {
            "crossovers": [],
            "no_crossovers": []
        },

        # mutation
        "mutation": {
            "mutations": [],
            "no_mutations": []
        },

        # selection
        "selection": {}
    }

    generations = parse_data(fp)
    for generation in generations:
        summarize_population(generation["population"], stats["population"])
        summarize_evaluation(generation["evaluation"], stats["evaluation"])
        summarize_selection(generation["selection"], stats["selection"])
        summarize_crossover(generation["crossover"], stats["crossover"])
        summarize_mutation(generation["mutation"], stats["mutation"])

    return stats


# def plot_summary(generations):
#     plt.figure(figsize=(7, 10))
#
#     # generation best scores
#     plt.subplot(311)
#     plot_generation_best_scores(generations)
#
#     # all time best scores
#     plt.subplot(312)
#     plot_all_time_best_scores(generations)
#
#     # evaluation stats
#     plt.subplot(313)
#     plot_evaluation_stats(generations)
#
#     plt.subplots_adjust(
#         left=None,
#         bottom=None,
#         right=None,
#         top=None,
#         wspace=None,
#         hspace=0.6
#     )
#     plt.show()
