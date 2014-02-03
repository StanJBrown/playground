#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import playground.config
from playground.playnode.grand_central import GrandCentral

# SETTINGS
cwd = os.path.dirname(__file__)
config_fp = os.path.normpath(os.path.join(cwd, "../config/grand_central.json"))


class GrandCentralTests(unittest.TestCase):
    def setUp(self):
        config = playground.config.load_config(config_fp)
        self.nodes = config["playnodes"]
        self.grand_central = GrandCentral(config)

    def tearDown(self):
        self.grand_central.stop_nodes()

    def test_start_node(self):
        # start node
        self.grand_central.start_node(self.nodes[0])

        # assert
        pidfile = "/tmp/playground-{0}-{1}.pid".format(
            self.nodes[0]["host"],
            self.nodes[0]["port"]
        )
        self.assertTrue(os.path.isfile(pidfile))

    def test_stop_node(self):
        # start node
        self.grand_central.start_node(self.nodes[0])

        # stop node
        self.grand_central.stop_node(self.nodes[0])

        # assert
        pidfile = "/tmp/playground-{0}-{1}.pid".format(
            self.nodes[0]["host"],
            self.nodes[0]["port"]
        )
        self.assertFalse(os.path.isfile(pidfile))

    def test_start_nodes(self):
        # start nodes
        self.grand_central.start_nodes()

        # assert
        for node in self.nodes:
            pidfile = "/tmp/playground-{0}-{1}.pid".format(
                node["host"],
                node["port"]
            )
            self.assertTrue(os.path.isfile(pidfile))

    def test_stop_nodes(self):
        # start and nodes
        self.grand_central.start_nodes()
        self.grand_central.stop_nodes()

        # assert
        for node in self.nodes:
            pidfile = "/tmp/playground-{0}-{1}.pid".format(
                node["host"],
                node["port"]
            )
            self.assertFalse(os.path.isfile(pidfile))

    def test_query_node(self):
        # start and query node
        # self.grand_central.start_nodes()
        # self.grand_central.query_node(
        #     self.nodes[0],
        # )

        # assert
        pass

    def test_transfer_file(self):
        # start nodes and transfer file
        target = config_fp
        destination = "/tmp/config_file_test"
        self.grand_central.start_nodes()
        self.grand_central.transfer_file(self.nodes[0], target, destination)

        self.assertTrue(os.path.isfile(destination))
        os.unlink(destination)


if __name__ == '__main__':
    unittest.main()
