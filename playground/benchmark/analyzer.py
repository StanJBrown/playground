#!/usr/bin/env python2
import os
import json
import zipfile

import matplotlib.pyplot as plt
from matplotlib.pyplot import setp
from matplotlib.pyplot import get_cmap
from matplotlib.pyplot import figlegend


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


def plot_summary_graph(data, labels, field_key, **kwargs):
    # markers
    markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', '+', 'x']

    # colors
    cm = get_cmap('gist_rainbow')
    cgen = [cm(1.0 * i / len(data)) for i in range(len(data))]

    # best score
    axis = plt.subplot(kwargs["fignum"], sharex=kwargs.get("sharex", None))
    klev_1, klev_2 = field_key.split(".")
    max_field = max(data[0][klev_1][klev_2])
    min_field = min(data[0][klev_1][klev_2])

    lines = []
    for i in range(len(data)):
        x = data[i]["population"]["generation"]
        y = data[i][klev_1][klev_2]
        lines.extend(plt.plot(x, y, markers[i], linestyle="-", color=cgen[i]))

        if max(y) > max_field:
            max_field = max(y)

        if min(y) > min_field:
            min_field = min(y)

    # legend
    if kwargs.get("show_legend", False):
        figlegend(tuple(lines), tuple(labels), 'best')

    setp(axis.get_xticklabels())
    plt.ylabel(kwargs.get("ylabel"))
    ylim_diff = kwargs.get("ylim_diff", 10)
    plt.ylim(min_field - ylim_diff, max_field + ylim_diff)

    return axis


def plot_summary(data, labels, fig_title=None):
    fig = plt.figure(figsize=(10, 13.5), facecolor="white")

    # figure title
    if fig_title:
        fig.suptitle(fig_title, fontsize=18)

    # best score
    plot_summary_graph(
        data,
        labels,
        "population.best_score",
        fignum=511,
        show_legend=True,
        ylabel="best score",
        ylim_diff=10
    )

    # diversity
    plot_summary_graph(
        data,
        labels,
        "evaluation.diversity",
        fignum=512,
        ylabel="diversity",
        ylim_diff=0.1
    )

    # cache size
    plot_summary_graph(
        data,
        labels,
        "evaluation.cache_size",
        fignum=513,
        ylabel="cache size",
        ylim_diff=10
    )

    # trees evaluated
    plot_summary_graph(
        data,
        labels,
        "evaluation.trees_evaluated",
        fignum=514,
        ylabel="tree evaluated",
        ylim_diff=10
    )

    # tree nodes evaluated
    plot_summary_graph(
        data,
        labels,
        "evaluation.tree_nodes_evaluated",
        fignum=515,
        ylabel="tree nodes evaluated",
        ylim_diff=10
    )

    # add shared x axis label
    plt.xlabel("generation")

    # additional settings
    plt.subplots_adjust(hspace=0.3)
    plt.show(block=False)
