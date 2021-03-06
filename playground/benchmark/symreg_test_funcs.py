#!/usr/bin/env python2
import os
import math
import random
import parser


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


def generate_series_matrix(bounds, points, decimal_places=2):
    points_generated = 0
    matrix = []
    columns = len(bounds)

    # calculate the steps
    for i in range(columns):
        step = bounds[i]["upper"] - bounds[i]["lower"]
        step = step / float(points)
        bounds[i]["step"] = round(step, decimal_places)

    while (points_generated != points):

        tmp = []
        for i in range(columns):
            if bounds[i].get("last_number") is not None:
                num = round(bounds[i]["last_number"], decimal_places)
                num += round(bounds[i]["step"], decimal_places)
                bounds[i]["last_number"] = round(num, decimal_places)
            else:
                num = bounds[i]["lower"]
                bounds[i]["last_number"] = round(num, decimal_places)
            tmp.append(num)

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


def simple_test_functions(dest, pattern="simple_test_funcs", fext=".dat"):
    t_funcs = [
        "(v[0] * v[0])",
        "(v[0] * v[0]) + 10",
        "(v[0] * v[0] * v[0])",
        "(v[0] * v[0] * v[0]) + 10",
        "(v[0] * v[0] * v[0]) + math.exp(v[0])",
    ]

    bounds = [
        [{"lower": -1.0, "upper": 1.0}],
        [{"lower": -1.0, "upper": 1.0}],
        [{"lower": -1.0, "upper": 1.0}],
        [{"lower": -1.0, "upper": 1.0}],
        [{"lower": -1.0, "upper": 1.0}]
    ]

    points = [100, 100, 100, 100, 100]

    for i in range(len(t_funcs)):
        dest_path = os.path.join(dest, pattern)
        fp = "{0}{1}{2}".format(dest_path, i + 1, fext)

        matrix = generate_series_matrix(bounds[i], points[i])
        data = evaluate_test_function(t_funcs[i], matrix)
        write_test_data(fp, data)


def arabas_et_al_test_functions(dest, pattern="arabas_et_al-f", fext=".dat"):
    # Arabas, J., Michalewicz, Z. & Mulawka, J., 1994. GAVaPS-a genetic
    # algorithm with varying population size. Proceedings of the First IEEE
    # Conference on Evolutionary Computation. IEEE World Congress on
    # Computational Intelligence.

    t_funcs = [
        "-v[0] * math.sin(10.0 * math.pi * v[0]) + 1.0",
        "int(8.0 * v[0]) / 8.0",
        "v[0] * math.copysign(1, v[0])",
        " ".join(
            """
            0.5 + (math.sin(math.sqrt(v[0] ** 2 + v[1] **2) - 0.5) ** 2)
            / (1 + 0.001 * (v[0] ** 2 + v[1] ** 2)) **2
            """.split()
        )
    ]

    bounds = [
        [{"lower": -2.0, "upper": 1.0}],
        [{"lower": 0.0, "upper": 1.0}],
        [{"lower": -1.0, "upper": 2.0}],
        [{"lower": -100.0, "upper": 100.0}, {"lower": -100.0, "upper": 100.0}],
    ]

    points = [200, 50, 50, 50]

    for i in range(len(t_funcs)):
        dest_path = os.path.join(dest, pattern)
        fp = "{0}{1}{2}".format(dest_path, i + 1, fext)

        matrix = generate_series_matrix(bounds[i], points[i])
        data = evaluate_test_function(t_funcs[i], matrix)
        write_test_data(fp, data)


def nguyen_et_al_test_functions(dest, pattern="nguyen_et_al-f", fext=".dat"):
    # Uy, N.Q. et al., 2011. Semantically-based crossover in genetic
    # programming: application to real-valued symbolic regression. Genetic
    # Programming and Evolvable Machines, 12(2), p.91-119.

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
        dest_path = os.path.join(dest, pattern)
        fp = "{0}{1}{2}".format(dest_path, i + 1, fext)

        matrix = generate_random_matrix(bounds[i], points[i])
        data = evaluate_test_function(t_funcs[i], matrix)
        write_test_data(fp, data)


# def de_jong_test_functions(data_file="de_jong-f"):
#     t_funcs = [
#         "v[0] ** 2 + v[0] ** 2 + v[0] ** 2",
#         "(v[0] ** 2) * 30",
#         "100 * (v[0] ** 2 - v[1]) ** 2 + (1 - x[0]) ** 2"
#         "30 + (v[0] * 5)"
#     ]
#
#     bounds = [
#         [{"lower": -5.12, "upper": 5.12}],
#         [{"lower": -5.12, "upper": 5.12}],
#         [{"lower": -2.048, "upper": 2.048}],
#         [{"lower": -5.12, "upper": 5.12}],
#         [{"lower": -65.536, "upper": 65.536}]
#     ]

    # points = [200, 50, 50, 50]

    # for i in range(len(t_funcs)):
    #     fp = "{0}{1}{2}".format(data_file, i + 1, data_file_extension)
    #     matrix = generate_series_matrix(bounds[i], points[i])
    #     data = evaluate_test_function(t_funcs[i], matrix)
    #     write_test_data(fp, data)

if __name__ == "__main__":
    simple_test_functions(".")
