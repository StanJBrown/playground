#!/usr/bin/env python
import math
import random
import parser

# GLOBAL VARS
data_file_extension = ".dat"


def write_test_data(fp, data):
    cols = len(data[0].split()) - 1
    data_file = open(fp, "wb")

    # create header
    variables = ["var{0}".format(i + 1) for i in range(cols)]
    variables.append("answer")
    header = ", ".join(variables)
    data_file.write(header + "\n")

    # write data
    for line in data:
        data_file.write("{0}\n".format(line))

    # close data file
    data_file.close()


def generate_random_matrix(bounds, points, decimal_places=2):
    points_generated = 0
    matrix = []
    columns = len(bounds)

    while (points_generated != points):

        tmp = []
        for i in range(columns):
            lower = bounds[i]["lower"]
            upper = bounds[i]["upper"]
            rand_num = round(random.uniform(lower, upper), decimal_places)
            tmp.append(rand_num)

        if tmp not in matrix:
            matrix.append(tmp)
            points_generated += 1

    return matrix


def evaluate_test_function(equation, var_values):
    data = []
    points = len(var_values)

    for i in range(points):
        # eval equation
        v = var_values[i]
        code = parser.expr(equation).compile()
        result = eval(code)

        # stringify results
        line = map(str, v)  # add variable values
        line.append(str(result))  # add result
        line = ", ".join(map(str, line))  # stringfy the data line
        data.append(line)

    return data


def nguyen_et_al_test_functions(data_file="nguyen_et_al-f"):
    t_funcs = [
        "v[0] ** 3 + v[0] ** 2 + v[0]",
        "v[0] ** 4 + v[0] ** 3 + v[0] ** 2 + v[0]",
        "v[0] ** 5 + v[0] ** 4 + v[0] ** 3 + v[0] ** 2 + v[0]",
        "v[0] ** 6 + v[0] ** 5 + v[0] ** 4 + v[0] ** 3 + v[0] ** 2 + v[0]",
        "math.sin(v[0] ** 2) * math.cos(v[0]) - 1",
        "math.sin(v[0]) + math.sin(v[0] + v[0] ** 2) - 1",
        "math.log(v[0] + 1) + math.log(v[0] ** 2 + 1)",
        "math.sqrt(v[0])",
        "math.sin(v[0]) + math.sin(v[1] ** 2)",
        "2 * math.sin(v[0]) * math.cos(v[1])"
    ]

    bounds = [
        [{"lower": -1, "upper": 1}],
        [{"lower": -1, "upper": 1}],
        [{"lower": -1, "upper": 1}],
        [{"lower": -1, "upper": 1}],
        [{"lower": -1, "upper": 1}],
        [{"lower": -1, "upper": 1}],
        [{"lower": 0, "upper": 2}],
        [{"lower": 0, "upper": 4}],
        [{"lower": -1, "upper": 1}, {"lower": -1, "upper": 1}],
        [{"lower": -1, "upper": 1}, {"lower": -1, "upper": 1}]
    ]

    points = [20, 20, 20, 20, 20, 20, 20, 20, 100, 100]

    for i in range(len(t_funcs)):
        fp = "{0}{1}{2}".format(data_file, i + 1, data_file_extension)
        matrix = generate_random_matrix(bounds[i], points[i])
        data = evaluate_test_function(t_funcs[i], matrix)
        write_test_data(fp, data)
