#!/usr/bin/env python
import sys
import os
import json
import pprint
import random
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import playground.config as config
from playground.recorder.json_store import JSONStore
# from playground.recorder.record_type import RecordType
from playground.functions import FunctionRegistry
from playground.gp.tree.tree_evaluation import evaluate
from playground.gp.tree.tree_generator import TreeGenerator
from playground.operators.selection import Selection
from playground.operators.crossover import GPTreeCrossover
from playground.operators.mutation import GPTreeMutation

# SETTINGS
config_fp = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../config/json_store.json")
)


class JSONStoreTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)

        self.functions = FunctionRegistry()
        self.tree_generator = TreeGenerator(self.config)

        self.json_store = JSONStore(self.config)
        self.json_store.setup_store()

        self.population = self.tree_generator.init()
        results = []
        cache = {}
        evaluate(
            self.population.individuals,
            self.functions,
            self.config,
            results,
            cache,
            self.json_store
        )
        self.population.sort_individuals()

        self.selection = Selection(self.config, recorder=self.json_store)
        self.crossover = GPTreeCrossover(self.config, recorder=self.json_store)
        self.mutation = GPTreeMutation(self.config, recorder=self.json_store)

    def tearDown(self):
        self.json_store.delete_store()

        del self.config
        del self.functions
        del self.tree_generator
        del self.population
        del self.json_store

    def test_setup_store(self):
        # assert
        file_exists = os.path.exists(self.config["json_store"]["store_file"])
        self.assertEquals(file_exists, True)

    def test_purge_store(self):
        # write something to store file
        self.json_store.store_file.write("Hello World\n")
        self.json_store.store_file.close()

        # purge store file
        self.json_store.purge_store()

        # assert
        store_file = open(self.config["json_store"]["store_file"], "r").read()
        self.assertEquals(len(store_file), 0)

    def test_delete_store(self):
        # delete store
        self.json_store.delete_store()

        # assert
        file_exists = os.path.exists(self.config["json_store"]["store_file"])
        self.assertEquals(file_exists, False)

    def test_record_population(self):
        self.json_store.record_population(self.population)

        record = self.json_store.generation_record
        self.assertNotEquals(record, {})
        self.assertEquals(record["population"]["generation"], 0)

    def test_record_selection(self):
        # record selection
        self.selection.select(self.population)

        # assert
        record = self.json_store.generation_record
        # pprint.pprint(record)
        self.assertNotEquals(record, {})
        self.assertEquals(record["selection"]["selected"], 5)

    def test_record_crossover(self):
        # record crossover
        tree_1 = self.population.individuals[0]
        tree_2 = self.population.individuals[1]
        self.crossover.crossover(tree_1, tree_2)

        # assert
        record = self.json_store.generation_record
        # pprint.pprint(record)
        self.assertNotEquals(record, {})
        self.assertEquals(record["crossover"][0]["crossovered"], True)
        self.assertEquals(record["crossover"][0]["index"], 1)
        self.assertEquals(record["crossover"][0]["method"], "POINT_CROSSOVER")

    def test_record_mutation(self):
        # record mutation
        tree = self.population.individuals[0]
        self.mutation.mutate(tree)

        # assert
        record = self.json_store.generation_record
        # pprint.pprint(record)
        self.assertNotEquals(record, {})
        self.assertEquals(record["mutation"][0]["method"], "SHRINK_MUTATION")
        self.assertEquals(record["mutation"][0]["mutation_probability"], 0.8)

    def test_record_evaulation(self):
        # record evaluation
        results = []
        evaluate(
            self.population.individuals,
            self.functions,
            self.config,
            results,
            recorder=self.json_store
        )

        # assert
        record = self.json_store.generation_record
        pprint.pprint(record)
        self.assertEquals(record["evaluation"]["cache_size"], 10)
        self.assertEquals(record["evaluation"]["match_cached"], 0)

    def test_record_to_file(self):
        # write record to file and close
        self.json_store.record_population(self.population)
        self.json_store.record_to_file()
        self.json_store.store_file.close()

        # open up the file and restore json to dict
        store_file = open(self.config["json_store"]["store_file"], "r").read()
        data = json.loads(store_file)

        # assert tests
        self.assertNotEquals(data, {})
        self.assertEquals(data["population"]["generation"], 0)


if __name__ == '__main__':
    random.seed(1)
    unittest.main()
