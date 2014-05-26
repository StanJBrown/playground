#!/usr/bin/env python
import math

import numpy as np
import matplotlib.pylab as plt

from sklearn import svm


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

    # test classification circle
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
        plt.plot(circle_x, circle_y)
        plt.show()

    return (x, y, categories, solution)


if __name__ == "__main__":
    x, y, categories, solution = test_data()

    svm_classifier = svm.SVC(kernel="linear", probability=True)
