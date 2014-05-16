#!/usr/bin/env python2
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

import playground.config as config
from playground.gp.functions import GPFunctionRegistry
from playground.gp.tree.generator import TreeGenerator
from playground.gp.tree.classifier_evaluation import evaluate
from playground.gp.tree.classifier_evaluation import evaluate_tree


class ClassifierEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "max_population": 5,

            "tree_generation": {
                "tree_type": "CLASSIFICATION_TREE",
                "method": "FULL_METHOD",
                "initial_max_depth": 2
            },

            "evaluator": {
                "use_cache": True
            },

            "function_nodes": [
                {
                    "type": "CLASS_FUNCTION",
                    "name": "GREATER_THAN",
                    "arity": 2,

                    "data_range": {
                        "lower_bound": 0.0,
                        "upper_bound": 10.0,
                        "decimal_places": 0,
                    }
                },
                {
                    "type": "CLASS_FUNCTION",
                    "name": "LESS_THAN",
                    "arity": 2,

                    "data_range": {
                        "lower_bound": 0.0,
                        "upper_bound": 10.0,
                        "decimal_places": 0,
                    }
                },
                {
                    "type": "CLASS_FUNCTION",
                    "name": "EQUALS",
                    "arity": 2,
                    "decimal_precision": 2,
                    "data_range": {
                        "lower_bound": 0.0,
                        "upper_bound": 10.0,
                        "decimal_places": 0,
                    }
                }
            ],

            "terminal_nodes": [
                {
                    "type": "RANDOM_CONSTANT",
                    "name": "species",
                    "range": [
                        1.0,
                        2.0,
                        3.0
                    ]
                },
            ],

            "input_variables": [
                {"name": "sepal_length"},
                {"name": "sepal_width"},
                {"name": "petal_length"},
                {"name": "petal_width"}
            ],

            "class_attributes": [
                "sepal_length",
                "sepal_width",
                "petal_length",
                "petal_width"
            ],

            "data_file": "tests/data/iris.dat",

            "response_variables": [{"name": "species"}]
        }
        config.load_data(self.config)

        self.functions = GPFunctionRegistry("CLASSIFICATION")
        self.generator = TreeGenerator(self.config)
        self.population = self.generator.init()

    def test_evaluate_tree(self):
        for i in range(100):
            tree = self.generator.generate_tree()
            score, output = evaluate_tree(tree, self.functions, self.config)

            # self.assertTrue(score < 1.0)
            self.assertEquals(len(output), self.config["data"]["rows"])

    def test_evaluate(self):
        results = []
        evaluate(self.population.individuals, self.functions, self.config, results)
        self.assertTrue(len(results), len(self.population.individuals))


if __name__ == "__main__":
    unittest.main()
