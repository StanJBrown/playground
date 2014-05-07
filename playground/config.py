#!/usr/bin/env python2
import os
import json
import csv


def _find_header_index(header_line, node_name):
    colnum = 0
    for col in header_line:
        if col == node_name:
            return colnum
        colnum += 1


def _parse_header(csv_reader, config):
    # get header
    header = csv_reader.next()
    header = [el.strip() for el in header]

    # obtain and set response variable index
    for response_var in config["response_variables"]:
        response_index = _find_header_index(header, response_var["name"])
        response_var["data_index"] = response_index

        # obtain and set input variable index
        for input_node in config["input_variables"]:
            index = _find_header_index(header, input_node["name"])
            input_node["data_index"] = index


def _parse_data_row(row, config, variables):
    colnum = 0
    for col in row:
        for var in variables:
            if var["data_index"] == colnum:
                config["data"][var["name"]].append(float(col))
        colnum += 1


def _parse_data(csv_reader, config):
    # var list containig details what each column is
    variables = []
    variables.extend(config["response_variables"])
    variables.extend(config["input_variables"])

    # create data and variables (i.e. a data table in list form)
    config["data"] = {}
    for var in variables:
        config["data"][str(var["name"])] = []

    rownum = 0
    for row in csv_reader:
        _parse_data_row(row, config, variables)
        rownum += 1

    # keep a record number of data rows
    config["data"]["rows"] = rownum


def load_data(config, abs_dir=None):
    # open data and csv reader
    if abs_dir:
        config["data_file"] = os.path.join(abs_dir, config["data_file"])
        config["data_file"] = os.path.normpath(config["data_file"])

    data_file = open(config["data_file"], "rb")
    csv_reader = csv.reader(data_file)

    _parse_header(csv_reader, config)
    _parse_data(csv_reader, config)

    # clean up
    data_file.close()


def load_config(config_file, abs_dir=None):
    if abs_dir:
        config_file = os.path.join(abs_dir, config_file)

    config = json.loads(open(config_file).read())

    # load data
    if config.get("data_file", False) and config["data_file"] is not None:
        load_data(config, abs_dir)

    # keep abs_dir in config
    if abs_dir:
        config["absolute_dir"] = abs_dir

    return config
