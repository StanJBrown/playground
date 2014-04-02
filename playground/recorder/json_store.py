#!/usr/bin/env python
import os
import json
import zipfile
from playground.recorder.record_type import RecordType


class RecordLevel(object):
    MIN = 1
    MAX = 2


class JSONStore(object):
    def __init__(self, config):
        self.config = config
        self.record_config = config["recorder"]
        self.store_file_path = self.record_config.get("store_file", None)
        self.level = self.record_config.get("record_level", RecordLevel.MIN)
        self.store_file = None
        self.generation_record = {
            "population": None,
            "selection": None,
            "crossover": [],
            "mutation": [],
            "evaluation": []
        }  # stores 1 generation of an EA run

        self.setup_store()

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
        pop_dict = population.to_dict()

        if self.level is RecordLevel.MIN:
            pop_dict.pop("individuals")

        self.generation_record["population"] = pop_dict

    def record_selection(self, selection):
        select_dict = selection.to_dict()

        if self.level is RecordLevel.MIN:
            select_dict.pop("selected_individuals")

        self.generation_record["selection"] = select_dict

    def record_crossover(self, crossover):
        crossover_dict = crossover.to_dict()

        if self.level is RecordLevel.MIN:
            crossover_dict.pop("before_crossover")
            crossover_dict.pop("after_crossover")

        self.generation_record["crossover"].append(crossover_dict)

    def record_mutation(self, mutation):
        mutation_dict = mutation.to_dict()

        if self.level is RecordLevel.MIN:
            mutation_dict.pop("before_mutation")
            mutation_dict.pop("after_mutation")

        self.generation_record["mutation"].append(mutation_dict)

    def record_evaluation(self, evaluation_stats):
        if self.level is RecordLevel.MIN:
            evaluation_stats.pop("cache")

        self.generation_record["evaluation"] = evaluation_stats

    def record_to_file(self):
        json_record = json.dumps(self.generation_record)
        self.store_file.write(json_record + "\n")

        # reset generation record
        self.generation_record = {
            "population": None,
            "selection": None,
            "crossover": [],
            "mutation": [],
            "evaluation": []
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

    def replace_file_ext(self, path, target_ext="zip"):
        file_path = path.split(".")
        file_path[-1] = target_ext
        file_path = ".".join(file_path)

        return file_path

    def finalize(self):
        # compress the store file
        store_file = self.store_file_path

        if self.record_config.get("compress", False):
            # compress store file
            zip_file = self.replace_file_ext(self.store_file_path)
            zf = zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED)
            zf.write(store_file, os.path.basename(store_file))
            zf.close()

            # remove uncompressed store file
            os.remove(self.store_file_path)
