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
from playground.recorder.db import RecordType
from playground.recorder.db import DB
from playground.operators.selection import Selection
from playground.operators.crossover import GPTreeCrossover
from playground.operators.mutation import GPTreeMutation

# SETTINGS
config_fp = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../config/db_adaptor.json")
)


class DBTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        data.load_data(self.config)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        self.db = DB(self.config)
        self.db.setup_tables()

        self.population = self.tree_initializer.init()
        self.population.evaluate_population()
        self.population.sort_individuals()

        self.selection = Selection(self.config, recorder=self.db)
        self.crossover = GPTreeCrossover(self.config, recorder=self.db)
        self.mutation = GPTreeMutation(self.config, recorder=self.db)

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
        data = self.db.select(RecordType.TREE)[0]

        self.assertEquals(round(data["score"], 4), round(individual.score, 4))
        self.assertEquals(data["size"], individual.size)
        self.assertEquals(data["depth"], individual.depth)
        self.assertEquals(data["branches"], individual.branches)

    def test_record_population(self):
        self.db.record_population(self.population)
        self.db.conn.commit()

        # assert
        data = self.db.select(RecordType.POPULATION)[0]

        best_individual = str(self.population.best_individuals[0])
        best_score = self.population.best_individuals[0].score
        self.assertEquals(data["generation"], self.population.generation)
        self.assertEquals(round(data["best_score"], 4), round(best_score, 4))
        self.assertEquals(data["best_individual"], best_individual)

    def test_record_selection(self):
        self.selection.select(self.population)

        # assert
        data = self.db.select(RecordType.SELECTION)
        self.assertEquals(len(data), 1)

        data = data[0]
        self.assertEquals(len(data), 3)
        self.assertEquals(data["method"], self.selection.method)
        self.assertEquals(data["selected"], self.selection.selected)

    def test_record_crossover(self):
        tree_1 = self.population.individuals[0]
        tree_2 = self.population.individuals[1]
        self.crossover.crossover(tree_1, tree_2)

        # assert
        data = self.db.select(RecordType.CROSSOVER)
        self.assertEquals(len(data), 1)

        data = data[0]
        self.assertEquals(len(data), 5)
        self.assertEquals(data["method"], self.crossover.method)
        self.assertEquals(
            round(data["crossover_probability"], 4),
            round(self.crossover.crossover_probability, 4)
        )
        self.assertEquals(
            round(data["random_probability"], 4),
            round(self.crossover.random_probability, 4)
        )
        self.assertEquals(data["crossovered"], self.crossover.crossovered)

    def test_record_mutation(self):
        tree = self.population.individuals[0]
        self.mutation.mutate(tree)

        # assert
        data = self.db.select(RecordType.MUTATION)
        self.assertEquals(len(data), 1)

        data = data[0]
        self.assertEquals(len(data), 5)
        self.assertEquals(data["method"], self.mutation.method)
        self.assertEquals(
            round(data["mutation_probability"], 4),
            round(self.mutation.mutation_probability, 4)
        )
        self.assertEquals(
            round(data["random_probability"], 4),
            round(self.mutation.random_probability, 4)
        )
        self.assertEquals(data["mutated"], self.mutation.mutated)

    def test_record(self):
        individual = self.population.individuals[0]
        self.db.record(RecordType.POPULATION, self.population)
        self.db.conn.commit()

        # assert population
        data = self.db.select(RecordType.POPULATION)[0]

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
        self.db.record(RecordType.POPULATION, self.population)
        data = self.db.select(RecordType.POPULATION)

        # population
        data_best_score = round(data[0]["best_score"], 4)
        pop_best_score = round(self.population.best_individuals[0].score, 4)
        self.assertEquals(pop_best_score, data_best_score)

        # individuals
        data = self.db.select(RecordType.TREE)
        self.assertEquals(len(self.population.individuals), len(data))

        data = self.db.select(RecordType.TREE, None, 1)
        self.assertEquals(len(data), 1)

    def test_remove(self):
        # setup
        self.db.record(RecordType.POPULATION, self.population)

        # check before remove
        data = self.db.select(RecordType.POPULATION)
        self.assertTrue(len(data) > 0)

        # remove
        self.db.remove(RecordType.POPULATION)

        # check after remove
        data = self.db.select(RecordType.POPULATION)
        self.assertEquals(len(data), 0)

if __name__ == '__main__':
    unittest.main()
