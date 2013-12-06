#!/usr/bin/env python
import os

import psycopg2 as db
import psycopg2.extras as db_extras


class DBDataType(object):
    POPULATION = "POPULATION"
    TREE = "TREE"
    SELECTION = "SELECTION"
    CROSSOVER = "CROSSOVER"
    MUTATION = "MUTATION"


class DBAdaptor(object):
    def __init__(self, config):
        self.config = config
        self.host = config["database"]["host"]
        self.port = config["database"]["port"]
        self.db = config["database"]["database"]
        self.user = config["database"]["user"]

        self.conn = None
        self.cursor = None

        # tables
        self.populations = "populations"
        self.trees = "trees"
        self.selections = "selections"
        self.crossovers = "crossovers"
        self.mutations = "mutations"

        self.connect()

    def connect(self):
        try:
            self.conn = db.connect(database=self.db, user=self.user)
            self.cursor = self.conn.cursor(cursor_factory=db_extras.DictCursor)
        except db.DatabaseError, e:
            print('Error {0}'.format(e))
            raise

    def setup_tables(self):
        try:
            cwd = os.path.dirname(__file__)
            table_schema = os.path.join(cwd, "./schemas/default.sql")
            table_schema = os.path.normpath(table_schema)

            self.cursor.execute(open(table_schema, "r").read())
            self.conn.commit()
        except db.DatabaseError, e:
            print('Error {0}'.format(e))
            raise

    def purge_tables(self):
        try:
            cwd = os.path.dirname(__file__)
            table_schema = os.path.join(cwd, "./schemas/purge_default.sql")
            table_schema = os.path.normpath(table_schema)

            self.cursor.execute(open(table_schema, "r").read())
            self.conn.commit()
        except db.DatabaseError, e:
            print('Error {0}'.format(e))
            raise

    def record_individual(self, population_id, generation, individual):
        try:

            func_nodes = []
            for node in individual.func_nodes:
                func_nodes.append(node.name.encode("ascii", "ignore"))

            term_nodes = []
            for node in individual.term_nodes:
                if node.name is not None:
                    term_nodes.append(node.name.encode("ascii", "ignore"))
                else:
                    term_nodes.append(node.value)

            input_nodes = []
            for node in individual.input_nodes:
                input_nodes.append(node.name.encode("ascii", "ignore"))

            query = """
                INSERT INTO {table}
                (
                    population_id,
                    generation,
                    score,

                    size,
                    depth,
                    branches,

                    func_nodes_len,
                    term_nodes_len,
                    input_nodes_len,

                    func_nodes,
                    term_nodes,
                    input_nodes,

                    program,
                    dot_graph
                )
                VALUES (
                    {population_id},
                    {generation},
                    {score},

                    {size},
                    {depth},
                    {branches},

                    {func_nodes_len},
                    {term_nodes_len},
                    {input_nodes_len},

                    ARRAY{func_nodes},
                    ARRAY{term_nodes},
                    ARRAY{input_nodes},

                    '{program}',
                    '{dot_graph}'
                )
            """.format(
                table=self.trees,

                population_id=population_id,
                generation=generation,
                score=individual.score,

                size=individual.size,
                depth=individual.depth,
                branches=individual.branches,

                func_nodes_len=len(individual.func_nodes),
                term_nodes_len=len(individual.term_nodes),
                input_nodes_len=len(individual.input_nodes),

                func_nodes=func_nodes,
                term_nodes=term_nodes,
                input_nodes=input_nodes,

                program=str(individual),
                dot_graph=str(individual)
            )
            self.cursor.execute(query)
        except db.DatabaseError:
            raise

    def record_population(self, population):
        try:
            best_individual = str(population.best_individuals[0])
            best_score = population.best_individuals[0].score

            query = """
                INSERT INTO {table}
                (
                    generation,
                    best_score,
                    best_individual
                )
                VALUES
                (
                    {generation},
                    {best_score},
                    '{best_individual}'
                )
            """.format(
                table=self.populations,
                generation=population.generation,
                best_score=best_score,
                best_individual=best_individual
            )
            self.cursor.execute(query)

            generation = population.generation
            for individual in population.individuals:
                self.record_individual(1, generation, individual)

        except db.DatabaseError:
            raise

    def record(self, data_type, data):
        try:
            if data_type == DBDataType.POPULATION:
                self.record_population(data)
            self.conn.commit()

        except db.DatabaseError:
            raise

    def remove(self, data):
        print ""

    def update(self, data):
        print ""

    def read(self, data):
        print ""
