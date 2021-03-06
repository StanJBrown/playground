#!/usr/bin/env python2
from scipy import stats


def rank_data(data, reverse=False):
    data_copy = [x[:] for x in data]

    for row in data_copy:
        # order elements in row
        order = sorted(list(row), reverse=reverse)

        # find duplicates in row
        duplicates = set([x for x in row if row.count(x) > 1])

        # rank row
        i = 0
        for el in row:
            if el not in duplicates:
                row[i] = order.index(el) + 1
            else:
                row[i] = order.index(el) + 1.5
            i += 1

    return data_copy


def sum_col_ranks(data):
    cols = len(data[0])
    rank_cols = [[] for i in range(cols)]

    # gather all column ranks
    for row in data:
        col_num = 0
        for el in row:
            rank_cols[col_num].append(el)
            col_num += 1

    # sum the column ranks
    result = []
    for col in rank_cols:
        result.append(sum(col))

    return result


def friedman_test_no_ties(data):
    n = float(len(data))  # rows
    k = float(len(data[0]))  # cols
    dof = k - 1  # degrees of freedom

    # rank data
    ranked_data = rank_data(data)
    ranks = sum_col_ranks(ranked_data)
    ranks = float(sum([x ** 2 for x in ranks]))

    # calculate test statistics
    test_stats = ((12.0 / (n * k * (k + 1))) * ranks) - 3.0 * n * (k + 1.0)
    p_value = 1 - stats.chi2.cdf(test_stats, dof)

    return (test_stats, p_value)

# parameterized algorithm can be formally defined as 7 tuple
# - infinite set of candidate configurations
# - infinite set of instances
# - probability measure over the set I
# - function associating to every instance the computation time allocated
# - random variable representing cost measure of a config on specific instance
# - range of c that is the possible values for the cost measure of the config
# on instance
# - probability measure over the set C
# - measures in some sense the desirability of specific config
# - total amount of time available for experimenting with given candidate
# config

# brute-froce problems:
# - too few configurations
# - too many configurations
# - spends equal amount of time on bad and good configurations
#
# racing-algorithm:
# - racing algorithm mitigates the last point
# - the problem of using racing algorithm approach is it **may not** mitigate
# the total amount of time needed to find best configuration
#
# - if null hypo rejected, we are justified in using pairwise comparisons. All
# candidates *significantly* worst (student t-test dist) then the best are
# discarded.
# - else all candidates remain
#
# friedman test requires n >= 10, minimal repeated measurements 6


# def f_race(param):
#     configurations = param["configurations"]
#     test_instances = param["test_instances"]
#
#     step = 0
#     survived_configs = []






