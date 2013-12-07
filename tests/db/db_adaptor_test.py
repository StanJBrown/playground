#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import playground.config as config
import playground.data_loader as data
from playground.functions import FunctionRegistry
from playground.evaluator import TreeEvaluator
from playground.initializer import TreeInitializer
from playground.db.db_adaptor import DBDataType
from playground.db.db_adaptor import DBAdaptor

# SETTINGS
config_fp = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../config/db_adaptor.json")
)


class DBAdaptorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        data.load_data(self.config)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        self.db = DBAdaptor(self.config)
        self.db.setup_tables()

        self.population = self.tree_initializer.init()
        self.population.evaluate_population()
        self.population.sort_individuals()

    def tearDown(self):
        self.db.purge_tables()

        del self.config
        del self.functions
        del self.evaluator
        del self.tree_initializer
        del self.db
        del self.population

    def test_record_indivdiuals(self):
        generation = self.population.generation
        individual = self.population.individuals[0]
        self.db.record_individual(1, generation, individual)
        self.db.conn.commit()

        # assert
        data = self.db.select(DBDataType.TREE)[0]

        self.assertEquals(round(data["score"], 4), round(individual.score, 4))
        self.assertEquals(data["size"], individual.size)
        self.assertEquals(data["depth"], individual.depth)
        self.assertEquals(data["branches"], individual.branches)

    def test_record_population(self):
        self.db.record_population(self.population)
        self.db.conn.commit()

        # assert
        data = self.db.select(DBDataType.POPULATION)[0]

        best_individual = str(self.population.best_individuals[0])
        best_score = self.population.best_individuals[0].score
        self.assertEquals(data["generation"], self.population.generation)
        self.assertEquals(round(data["best_score"], 4), round(best_score, 4))
        self.assertEquals(data["best_individual"], best_individual)

    def test_record(self):
        individual = self.population.individuals[0]
        self.db.record(DBDataType.POPULATION, self.population)
        self.db.conn.commit()

        # assert population
        data = self.db.select(DBDataType.POPULATION)[0]

        best_individual = str(self.population.best_individuals[0])
        best_score = self.population.best_individuals[0].score
        self.assertEquals(data["generation"], self.population.generation)
        self.assertEquals(round(data["best_score"], 4), round(best_score, 4))
        self.assertEquals(data["best_individual"], best_individual)

        # assert individual
        self.db.cursor.execute("SELECT * FROM trees")
        data = self.db.cursor.fetchall()[0]

        self.assertEquals(round(data["score"], 4), round(individual.score, 4))
        self.assertEquals(data["size"], individual.size)
        self.assertEquals(data["depth"], individual.depth)
        self.assertEquals(data["branches"], individual.branches)

    def test_select(self):
        self.db.record(DBDataType.POPULATION, self.population)
        data = self.db.select(DBDataType.POPULATION)

        # population
        data_best_score = round(data[0]["best_score"], 4)
        pop_best_score = round(self.population.best_individuals[0].score, 4)
        self.assertEquals(pop_best_score, data_best_score)

        # individuals
        data = self.db.select(DBDataType.TREE)
        self.assertEquals(len(self.population.individuals), len(data))

        data = self.db.select(DBDataType.TREE, None, 1)
        self.assertEquals(len(data), 1)

    def test_remove(self):
        # setup
        self.db.record(DBDataType.POPULATION, self.population)

        # check before remove
        data = self.db.select(DBDataType.POPULATION)
        self.assertTrue(len(data) > 0)

        # remove
        self.db.remove(DBDataType.POPULATION)

        # check after remove
        data = self.db.select(DBDataType.POPULATION)
        self.assertEquals(len(data), 0)

if __name__ == '__main__':
    unittest.main()
