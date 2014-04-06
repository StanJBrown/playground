#!/usr/bin/env python
import os
import sys
import unittest
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.benchmark.log_analyzer as log_analyzer

# SETTINGS
script_path = os.path.dirname(__file__)
log_file = "/Users/chutsu/data/benchmark_navive_parameter_sweep.log"


class LogAnalzyerTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_log(self):
        json_data = log_analyzer.parse_log(log_file)

        # import pprint
        # pprint.pprint(json_data[0])

        self.assertIsNotNone(json_data[0]["best_score"])

    def test_sort_records_by(self):
        json_data = log_analyzer.parse_log(log_file)
        json_data = log_analyzer.sort_records_by("best_score", json_data)

        # runtimes = []
        # best_scores = []
        # for record in json_data:
        #     runtimes.append(record["runtime"])
        #     best_scores.append(record["best_score"])

        # import matplotlib.pyplot as plt
        # plt.scatter(best_scores, runtimes)
        # plt.show()

        # assert
        prev = json_data.pop(0)["best_score"]
        for record in json_data:
            self.assertTrue(record["best_score"] >= prev)
            prev = record["best_score"]

    def test_parse_general_stats(self):
        json_data = log_analyzer.parse_log(log_file)
        json_data = log_analyzer.sort_records_by("best_score", json_data)
        stats = log_analyzer.parse_general_stats(json_data)

        # import matplotlib.pyplot as plt
        # from pylab import figure
        # figure(facecolor='white')
        # plt.scatter(stats["best_scores"], stats["runtimes"])
        # plt.xlabel("best_scores")
        # plt.ylabel("runtimes")
        # plt.show()

        # assert
        self.assertIsNotNone(stats["best_individuals"])
        self.assertIsNotNone(stats["best_scores"])
        self.assertIsNotNone(stats["runtimes"])

    def test_plot_matrix(self):
        json_data = log_analyzer.parse_log(log_file)
        log_analyzer.plot_matrix(
            json_data,
            show_plot=True,
            save_plot=True,
            save_path="test.png"
        )
        time.sleep(2)

        self.assertTrue(os.path.isfile("test.png"))
        os.remove("test.png")

if __name__ == "__main__":
    unittest.main()
