#!/usr/bin/env python
import json
import itertools

import numpy as np
import matplotlib.pyplot as plt


def parse_log(path):
    # parse log file
    log_file = open(path, "r")
    log_jsons = []

    for line in log_file:
        json_data = None

        try:
            json_data = json.loads(line)
        except TypeError as e:
            print "ERROR!:", e, "->", line
            raise

        if json_data:
            log_jsons.append(json_data)

    # clean up
    log_file.close()
    return log_jsons


def sort_records_by(attribute, log_jsons, reverse=False):
    return sorted(log_jsons, key=lambda x: x[attribute], reverse=reverse)


def parse_general_stats(log_jsons):
    best_individuals = []
    best_scores = []
    runtimes = []

    for record in log_jsons:
        best_individuals.append(record["best"])
        best_scores.append(record["best_score"])
        runtimes.append(record["runtime"])

    return {
        "best_individuals": best_individuals,
        "best_scores": best_scores,
        "runtimes": runtimes
    }


def plot_matrix(log_jsons, **kwargs):
    pop_sizes = []
    c_probs = []
    m_probs = []
    best_scores = []
    runtimes = []

    # parse needed data
    for record in log_jsons:
        pop_sizes.append(record["config"]["max_population"])
        c_probs.append(record["config"]["crossover"]["probability"] * 100)
        m_probs.append(record["config"]["mutation"]["probability"] * 100)
        best_scores.append(record["best_score"])
        runtimes.append(record["runtime"])

    # plot graph
    fields = [
        "Population Size",
        "Crossover Prob (%)",
        "Mutation Prob (%)",
        "Best Score",
        "Run Time (seconds)"
    ]

    data = [
        pop_sizes,
        c_probs,
        m_probs,
        best_scores,
        runtimes
    ]

    scatterplot_matrix(
        data,
        fields,
        linestyle="none",
        marker='o',
        color="#75B4FF",
        figsize=(12, 12)
    )

    if kwargs.get("show_plot", False):
        plt.show(block=kwargs.get("show_block", False))

    if kwargs.get("save_plot", False):
        plt.savefig(
            kwargs["save_path"],
            format=kwargs.get("save_format", "png")
        )


def scatterplot_matrix(data, names=[], **kwargs):
    numvars, numdata = len(data), len(data[0])
    fig, axes = plt.subplots(
        nrows=numvars,
        ncols=numvars,
        figsize=kwargs.get("figsize", (8, 8)),
        facecolor=kwargs.get("facecolor", "white")
    )
    fig.subplots_adjust(hspace=0.0, wspace=0.0)

    # remove kwargs before plot command
    if kwargs.get("figsize"):
        kwargs.pop("figsize")
    if kwargs.get("facecolor"):
        kwargs.pop("facecolor")

    for ax in axes.flat:
        # hide all ticks and labels
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # set up ticks only on one side for the "edge" subplots...
        if ax.is_first_col():
            ax.yaxis.set_ticks_position('left')
        if ax.is_last_col():
            ax.yaxis.set_ticks_position('right')
        if ax.is_first_row():
            ax.xaxis.set_ticks_position('top')
        if ax.is_last_row():
            ax.xaxis.set_ticks_position('bottom')

    # plot the data.
    for i, j in zip(*np.triu_indices_from(axes, k=1)):
        for x, y in [(i, j), (j, i)]:
            axes[x, y].plot(data[y], data[x], **kwargs)

    # label the diagonal subplots...
    if not names:
        names = ['x'+str(i) for i in range(numvars)]

    for i, label in enumerate(names):
        axes[i, i].annotate(label, (0.5, 0.5), xycoords='axes fraction',
                            ha='center', va='center')

    # turn on the proper x or y axes ticks.
    for i, j in zip(range(numvars), itertools.cycle((-1, 0))):
        axes[j, i].xaxis.set_visible(True)
        axes[i, j].yaxis.set_visible(True)

    # if numvars is odd, the bottom right corner plot doesn't have the
    # correct axes limits, so we pull them from other axes
    if numvars % 2:
        xlimits = axes[0, -1].get_xlim()
        ylimits = axes[-1, 0].get_ylim()
        axes[-1, -1].set_xlim(xlimits)
        axes[-1, -1].set_ylim(ylimits)

    return fig
