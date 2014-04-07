#!/usr/bin/env python
import os
import sys
import unittest
# import time
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import playground.benchmark.analyzer as analyzer

# SETTINGS
cwd = os.path.dirname(__file__)
log_file = os.path.normpath(os.path.join(cwd, "../data/test.log"))
data_file = "../data/bps--arabas_et_al-f1--100_0.05_0.05-0.zip"
data_file = os.path.join(cwd, data_file)
data_file = os.path.normpath(data_file)


class AnalzyerTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_datafile(self):
        # pass test
        result = analyzer.parse_data(data_file)
        solution = {
            "population": {
                "generation": 0,
                "best_individual": "(COS((var1 MUL 0.0)))",
                "best_score": 133.6826393201821
            }
        }
        self.assertEquals(result[0]["population"], solution["population"])

        # exception test
        self.assertRaises(IOError, analyzer.parse_data, log_file)

    def test_summarize_data(self):
        # pass test
        result = analyzer.summarize_data(data_file)

        # import pprint
        # pprint.pprint(result)

        self.assertIsNotNone(result)
        self.assertTrue(len(result["population"]["generation"]), 11)
        self.assertTrue(len(result["population"]["best_score"]), 11)
        self.assertTrue(len(result["population"]["best_individual"]), 11)

        self.assertTrue(len(result["crossover"]["crossovers"]), 11)
        self.assertTrue(len(result["crossover"]["no_crossovers"]), 11)

        self.assertTrue(len(result["mutation"]["mutations"]), 11)
        self.assertTrue(len(result["mutation"]["no_mutations"]), 11)


if __name__ == "__main__":
    unittest.main()
