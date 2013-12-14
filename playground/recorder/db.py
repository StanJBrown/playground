#!/usr/bin/env python
import os

import psycopg2 as db
import psycopg2.extras as db_extras

from playground.recorder import RecordType


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
        except db.DatabaseError:
            raise

    def disconnect(self):
        try:
            self.conn.close()
        except db.DatabaseError:
            raise

    def table_name(self, record_type):
        if record_type == RecordType.POPULATION:
            return self.populations
        elif record_type == RecordType.TREE:
            return self.trees
        elif record_type == RecordType.SELECTION:
            return self.selections
        elif record_type == RecordType.CROSSOVER:
            return self.crossovers
        elif record_type == RecordType.MUTATION:
            return self.mutations

    def setup_tables(self):
        try:
            cwd = os.path.dirname(__file__)
            table_schema = os.path.join(cwd, "./schemas/default.sql")
            table_schema = os.path.normpath(table_schema)

            self.cursor.execute(open(table_schema, "r").read())
            self.conn.commit()
        except db.DatabaseError:
            raise

    def purge_tables(self):
        try:
            cwd = os.path.dirname(__file__)
            table_schema = os.path.join(cwd, "./schemas/purge_default.sql")
            table_schema = os.path.normpath(table_schema)

            self.cursor.execute(open(table_schema, "r").read())
            self.conn.commit()
        except db.DatabaseError:
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
            self.conn.rollback()
            raise

    def record_selection(self, selection):
        try:
            query = """
                INSERT INTO {table}
                (
                    method,
                    selected
                )
                VALUES
                (
                    '{method}',
                    {selected}
                )
            """.format(
                table=self.selections,
                method=selection.method,
                selected=selection.selected,
            )
            self.cursor.execute(query)

        except db.DatabaseError:
            self.conn.rollback()
            raise

    def record_crossover(self, crossover):
        try:
            query = """
                INSERT INTO {table}
                (
                    method,
                    crossover_probability,
                    random_probability,
                    crossovered
                )
                VALUES
                (
                    '{method}',
                    {crossover_probability},
                    {random_probability},
                    {crossovered}
                )
            """.format(
                table=self.crossovers,
                method=crossover.method,
                crossover_probability=crossover.crossover_probability,
                random_probability=crossover.random_probability,
                crossovered=crossover.crossovered
            )
            self.cursor.execute(query)

        except db.DatabaseError:
            self.conn.rollback()
            raise

    def record_mutation(self, mutation):
        try:
            query = """
                INSERT INTO {table}
                (
                    method,
                    mutation_probability,
                    random_probability,
                    mutated
                )
                VALUES
                (
                    '{method}',
                    {mutation_probability},
                    {random_probability},
                    {mutated}
                )
            """.format(
                table=self.mutations,
                method=mutation.method,
                mutation_probability=mutation.mutation_probability,
                random_probability=mutation.random_probability,
                mutated=mutation.mutated
            )
            self.cursor.execute(query)

        except db.DatabaseError:
            self.conn.rollback()
            raise

    def record(self, record_type, data):
        try:
            if record_type == RecordType.POPULATION:
                self.record_population(data)
            elif record_type == RecordType.SELECTION:
                self.record_selection(data)
            elif record_type == RecordType.CROSSOVER:
                self.record_crossover(data)
            elif record_type == RecordType.MUTATION:
                self.record_mutation(data)
            else:
                raise RuntimeError("Undefined record type!")
            self.conn.commit()

        except db.DatabaseError:
            raise
        except:
            raise
        finally:
            self.conn.rollback()

    def _build_conditions(self, conditions):
        if conditions is not None:
            conditions = "WHERE " + " AND ".join(conditions)
        else:
            conditions = ""
        return conditions

    def _build_limit(self, limit):
        if limit is not None:
            limit = "LIMIT " + str(limit)
        else:
            limit = ""
        return limit

    def select(self, record_type, conditions=None, limit=None):
        try:
            table = self.table_name(record_type)
            conditions = self._build_conditions(conditions)
            limit = self._build_limit(limit)

            query = "SELECT * FROM {table} {conditions} {limit}".format(
                table=table,
                conditions=conditions,
                limit=limit
            )
            query = query.strip()
            query += ";"

            self.cursor.execute(query)
            data = self.cursor.fetchall()

            return data

        except db.DatabaseError:
            self.conn.rollback()
            raise

    def remove(self, record_type, conditions=None, limit=None):
        try:
            table = self.table_name(record_type)
            conditions = self._build_conditions(conditions)
            limit = self._build_limit(limit)

            query = "DELETE FROM {table} {conditions} {limit}".format(
                table=table,
                conditions=conditions,
                limit=limit
            )
            query = query.strip()
            query += ";"

            self.cursor.execute(query)

        except db.DatabaseError:
            self.conn.rollback()
            raise
