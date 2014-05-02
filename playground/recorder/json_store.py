#!/usr/bin/env python2.7
import os
import json
import errno
import zipfile
from playground.recorder.record_type import RecordType


class RecordLevel(object):
    MIN = "MIN"
    MAX = "MAX"


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

    def create_store_dir(self):
        try:
            store_dir = os.path.dirname(self.store_file_path)
            if store_dir:
                os.makedirs(store_dir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def setup_store(self):
        # expand on environment variables if defined
        self.store_file_path = os.path.expandvars(self.store_file_path)

        # create store dir if not already exists
        self.create_store_dir()

        # open store file for recording
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
        if self.store_file:
            self.store_file.close()
            self.store_file = None

        # remove store file if it exists
        if os.path.exists(self.store_file_path):
            os.remove(self.store_file_path)

        # remove compressed store file if it exists
        if os.path.exists(self.store_file_path.replace(".json", ".zip")):
            os.remove(self.store_file_path.replace(".json", ".zip"))

    def record_population(self, population):
        pop_dict = population.to_dict()

        if self.level == RecordLevel.MIN:
            pop_dict.pop("individuals")

        self.generation_record["population"] = pop_dict

    def record_selection(self, selection):
        select_dict = selection.to_dict()

        if self.level == RecordLevel.MIN:
            select_dict.pop("selected_individuals")

        self.generation_record["selection"] = select_dict

    def record_crossover(self, crossover):
        crossover_dict = crossover.to_dict()

        if self.level == RecordLevel.MIN:
            crossover_dict.pop("index")
            crossover_dict.pop("before_crossover")
            crossover_dict.pop("after_crossover")

        self.generation_record["crossover"].append(crossover_dict)

    def record_mutation(self, mutation):
        mutation_dict = mutation.to_dict()

        if self.level == RecordLevel.MIN:
            mutation_dict.pop("before_mutation")
            mutation_dict.pop("after_mutation")

        self.generation_record["mutation"].append(mutation_dict)

    def record_evaluation(self, evaluation_stats):
        if self.level == RecordLevel.MIN:
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

    def summarize_crossover(self, crossover):
        result = {
            "crossovers": 0,
            "no_crossovers": 0
        }

        for instance in crossover:
            method = instance["method"]
            crossed = instance["crossovered"]
            random_prob = instance["random_probability"]
            crossover_prob = instance["crossover_probability"]

            if method not in result:
                result[method] = {}
                result[method]["success"] = 0
                result[method]["failed"] = 0
                result[method]["frequency"] = 0

            if crossed:
                result[method]["success"] += 1
                result[method]["frequency"] += 1
                result["crossovers"] += 1
            else:
                # check to see if failure is due to probabilities or
                # true crossover failure
                if crossover_prob >= random_prob:
                    result[method]["failed"] += 1
                    result[method]["frequency"] += 1
                else:
                    result["no_crossovers"] += 1

        if self.level == RecordLevel.MAX:
            result["instances"] = crossover

        return result

    def summarize_mutation(self, mutations):
        result = {
            "mutations": 0,
            "no_mutations": 0
        }

        for instance in mutations:
            method = instance["method"]
            mutated = instance["mutated"]
            random_prob = instance["random_probability"]
            mutations_prob = instance["mutation_probability"]

            if method not in result:
                result[method] = {}
                result[method]["success"] = 0
                result[method]["failed"] = 0
                result[method]["frequency"] = 0

            if mutated:
                result[method]["success"] += 1
                result[method]["frequency"] += 1
                result["mutations"] += 1
            else:
                # check to see if failure is due to probabilities or
                # true mutations failure
                if mutations_prob >= random_prob:
                    result[method]["failed"] += 1
                    result[method]["frequency"] += 1
                else:
                    result["no_mutations"] += 1

        if self.level == RecordLevel.MAX:
            result["instances"] = mutations

        return result

    def summarize_store(self):
        if self.store_file:
            self.store_file.close()
            self.store_file = None

        # summarize records
        records = []
        self.store_file = open(self.store_file_path, "r")
        for record in self.store_file:
            record = json.loads(record)
            record["crossover"] = self.summarize_crossover(record["crossover"])
            record["mutation"] = self.summarize_mutation(record["mutation"])
            records.append(record)
        self.store_file.close()

        # rewrite store file
        self.store_file = open(self.store_file_path, "w")
        for record in records:
            self.store_file.write(json.dumps(record) + "\n")
        self.store_file.close()

    def finalize(self):
        store_file = self.store_file_path

        # summarize records
        self.summarize_store()

        # compress the store file
        if self.record_config.get("compress", False):
            # compress store file
            zip_file = self.replace_file_ext(self.store_file_path)
            zf = zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED)
            zf.write(store_file, os.path.basename(store_file))
            zf.close()

            # remove uncompressed store file
            os.remove(self.store_file_path)
