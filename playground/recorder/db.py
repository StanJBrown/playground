#!/usr/bin/env python
import os
import types

import psycopg2 as db
import psycopg2.extras as db_extras

from playground.recorder.record_type import RecordType


class DB(object):
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

    def insert(self, table, keys, vals, commit=False):
        try:
            q = "INSERT INTO %s (%s) VALUES %r" % (table, keys, tuple(vals),)
            self.cursor.execute(q)
            if commit:
                self.conn.commit()
        except db.DatabaseError:
            self.conn.rollback()
            raise

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

    def escape_unicode(self, string):
        if string is unicode:
            return string.encode("ascii", "ignore")
        else:
            return str(string)

    def dict_to_sql(self, query_dict):
        keys_sql = []
        vals_sql = []
        straight_forward_types = [
            types.BooleanType,
            types.IntType,
            types.LongType,
            types.FloatType,
            types.ComplexType,
            types.StringType,
            types.UnicodeType
        ]

        for key, value in query_dict.iteritems():
            value_type = type(value)

            if value_type in straight_forward_types:
                keys_sql.append(self.escape_unicode(key))
                vals_sql.append(self.escape_unicode(value))

            elif value_type is list:
                keys_sql.append(self.escape_unicode(key))
                val_list = []
                for element in value:
                    val_list.append(str(element))
                vals_sql.append('{' + ', '.join(val_list) + '}')

        keys_sql = ', '.join(keys_sql)

        return (keys_sql, vals_sql)

    def record_individual(self, population_id, generation, individual):
        try:
            individual_dict = {
                "population_id": population_id,
                "generation": generation,
                "score": individual.score,

                "size": individual.size,
                "depth": individual.depth,
                "branches": individual.branches,

                "func_nodes_len": len(individual.func_nodes),
                "term_nodes_len": len(individual.term_nodes),
                "input_nodes_len": len(individual.input_nodes),

                "func_nodes": individual.func_nodes,
                "term_nodes": individual.term_nodes,
                "input_nodes": individual.input_nodes,

                "program": str(individual),
                "dot_graph": str(individual)
            }
            keys, vals = self.dict_to_sql(individual_dict)
            self.insert(self.trees, keys, vals)
        except db.DatabaseError:
            raise

    def record_population(self, population):
        try:
            population_dict = {
                "generation": population.generation,
                "best_individual": str(population.best_individuals[0]),
                "best_score": population.best_individuals[0].score
            }
            keys, vals = self.dict_to_sql(population_dict)
            self.insert(self.populations, keys, vals)

            generation = population.generation
            for individual in population.individuals:
                self.record_individual(1, generation, individual)

        except db.DatabaseError:
            raise

    def record_selection(self, selection):
        try:
            selection_dict = {
                "method": selection.method,
                "selected": selection.selected
            }
            keys, vals = self.dict_to_sql(selection_dict)
            self.insert(self.selections, keys, vals)

        except db.DatabaseError:
            raise

    def record_crossover(self, crossover):
        try:
            crossover_dict = {
                "method": crossover.method,
                "crossover_probability": crossover.crossover_probability,
                "random_probability": crossover.random_probability,
                "crossovered": crossover.crossovered
            }
            keys, vals = self.dict_to_sql(crossover_dict)
            self.insert(self.crossovers, keys, vals)

        except db.DatabaseError:
            raise

    def record_mutation(self, mutation):
        try:
            mutation_dict = {
                "method": mutation.method,
                "mutation_probability": mutation.mutation_probability,
                "random_probability": mutation.random_probability,
                "mutated": mutation.mutated
            }
            keys, vals = self.dict_to_sql(mutation_dict)
            self.insert(self.mutations, keys, vals)

        except db.DatabaseError:
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
