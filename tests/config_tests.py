#!/usr/bin/env python
import os
import sys
import csv
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/data_loader.json")


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        self.data_file = open(self.config["data_file"], "rb")
        self.csv_reader = csv.reader(self.data_file, delimiter=',')

        self.solution = {
            'x': [
                10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0,
                100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0,
                190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 260.0, 270.0,
                280.0, 290.0, 300.0, 310.0, 320.0, 330.0, 340.0, 350.0, 360.0
            ],
            'y': [
                -0.9848, -0.342, 0.866, 0.6428, -0.6428, -0.866, 0.342,
                0.9848, 0.0, -0.9848, -0.342, 0.866, 0.6428, -0.6428, -0.866,
                0.342, 0.9848, 0.0, -0.9848, -0.342, 0.866, 0.6428, -0.6428,
                -0.866, 0.342, 0.9848, -0.0, -0.9848, -0.342, 0.866, 0.6428,
                -0.6428, -0.866, 0.342, 0.9848, 0.0
            ]
        }

    def tearDown(self):
        self.data_file.close()

    def test_find_header_index(self):
        # get header line
        header_line = self.csv_reader.next()
        header_line = [el.strip() for el in header_line]

        # get index of x
        index = config._find_header_index(header_line, "x")
        self.assertEquals(index, 0)

        # get index of y
        index = config._find_header_index(header_line, "y")
        self.assertEquals(index, 1)

    def test_parse_header(self):
        config._parse_header(self.csv_reader, self.config)

        # check index of x
        input_node = self.config["input_nodes"][0]
        self.assertEquals(input_node["data_index"], 0)

        # check index of y
        response_var = self.config["response_variable"]
        self.assertEquals(response_var["data_index"], 1)

    def test_parse_data_row(self):
        config._parse_header(self.csv_reader, self.config)

        row = [0, 100]
        self.config["data"] = []
        variables = []
        variables.append(self.config["response_variable"])
        variables.extend(self.config["input_nodes"])

        # create data and variables (i.e. a data table in list form)
        self.config["data"] = {}
        for var in variables:
            self.config["data"][str(var["name"])] = []

        config._parse_data_row(row, self.config, variables)

        # assert x and y
        self.assertEquals(self.config["data"]["x"][0], 0)
        self.assertEquals(self.config["data"]["y"][0], 100)

    def test_parse_data(self):
        config._parse_header(self.csv_reader, self.config)
        config._parse_data(self.csv_reader, self.config)
        self.assertEquals(self.config["data"], self.solution)

    def test_load_data(self):
        config.load_data(self.config)
        self.assertEquals(self.config["data"], self.solution)


if __name__ == '__main__':
    unittest.main()
