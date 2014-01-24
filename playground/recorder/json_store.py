#!/usr/bin/env python
import os
import json
from playground.recorder.record_type import RecordType


class JSONStore(object):
    def __init__(self, config):
        self.config = config
        self.json_store_config = config["json_store"]
        self.store_file_path = self.json_store_config.get("store_file", None)
        self.store_file = None
        self.generation_record = {
            "population": None,
            "selection": None,
            "crossover": [],
            "mutation": [],
            "evaluation": None
        }  # stores 1 generation of an EA run

    def setup_store(self):
        if self.store_file is None:
            self.store_file = open(self.store_file_path, "w")

    def purge_store(self):
        if self.store_file is None:
            self.store_file = open(self.store_file_path, "w")
            self.store_file.close()
        else:
            self.store_file.close()
            self.store_file = open(self.store_file_path, "w")
            self.store_file.close()

    def delete_store(self):
        # close store file if opened
        if self.store_file is not None:
            self.store_file.close()

        # remove store file if it exists
        if os.path.exists(self.store_file_path):
            os.remove(self.store_file_path)

    def record_population(self, population):
        self.generation_record["population"] = population.to_dict()

    def record_selection(self, selection):
        self.generation_record["selection"] = selection.to_dict()

    def record_crossover(self, crossover):
        self.generation_record["crossover"].append(crossover.to_dict())

    def record_mutation(self, mutation):
        self.generation_record["mutation"].append(mutation.to_dict())

    def record_evaluation(self, evaluation):
        self.generation_record["evaluation"] = evaluation

    def record_to_file(self):
        json_record = json.dumps(self.generation_record)
        # print json.dumps(self.generation_record, indent=4)
        self.store_file.write(json_record + "\n")

        # reset generation record
        self.generation_record = {
            "population": None,
            "selection": None,
            "crossover": [],
            "mutation": [],
            "evaluation": None
        }  # stores 1 generation of an EA run

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
        except:
            raise
