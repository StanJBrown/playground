#!/usr/bin/env python
import os
import sys
import time
import signal
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import playground.config
from playground.playnode.grand_central import GrandCentral
from playground.playnode.node import PlayNodeStatus

# SETTINGS
cwd = os.path.dirname(__file__)
config_fp = os.path.normpath(os.path.join(cwd, "../config/grand_central.json"))


class GrandCentralTests(unittest.TestCase):
    def setUp(self):
        config = playground.config.load_config(config_fp)
        self.nodes = config["playnodes"]
        self.grand_central = GrandCentral(config)

    def tearDown(self):
        for node in self.nodes:
            print node
            if node.get("pid", False):
                os.kill(node["pid"], signal.SIGTERM)

    def test_start_node(self):
        # start node
        self.grand_central.start_node(self.nodes[0])
        time.sleep(1)  # sleep

        # assert
        pidfile = "/tmp/playground-{0}-{1}.pid".format(
            self.nodes[0]["host"],
            self.nodes[0]["port"]
        )
        self.assertTrue(os.path.isfile(pidfile))

        self.grand_central.stop_nodes()
        time.sleep(1)  # sleep

    def test_stop_node(self):
        # start node
        self.grand_central.start_node(self.nodes[0])

        # stop node
        self.grand_central.stop_node(self.nodes[0])
        time.sleep(1)  # sleep before you check

        # assert
        pidfile = "/tmp/playground-{0}-{1}.pid".format(
            self.nodes[0]["host"],
            self.nodes[0]["port"]
        )
        self.assertFalse(os.path.isfile(pidfile))

    def test_start_nodes(self):
        # start nodes
        self.grand_central.start_nodes()
        time.sleep(1)  # sleep

        # assert
        for node in self.nodes:
            pidfile = "/tmp/playground-{0}-{1}.pid".format(
                node["host"],
                node["port"]
            )
            self.assertTrue(os.path.isfile(pidfile))

        self.grand_central.stop_nodes()
        time.sleep(1)  # sleep

    def test_stop_nodes(self):
        # start and nodes
        self.grand_central.start_nodes()
        time.sleep(1)  # sleep

        self.grand_central.stop_nodes()
        time.sleep(1)  # sleep

        # assert
        for node in self.nodes:
            pidfile = "/tmp/playground-{0}-{1}.pid".format(
                node["host"],
                node["port"]
            )
            self.assertFalse(os.path.isfile(pidfile))

    def test_remote_play(self):
        target_file = "examples/symbolic_regression/symbolic_regression.py"
        target = os.path.join(os.path.realpath(os.getcwd()), target_file)

        self.grand_central.remote_play(
            self.nodes[0],
            target,
            [],
            python_interpreter="PYPY"
        )

    def test_query_node(self):
        # start and query node
        self.grand_central.start_nodes()
        time.sleep(1)  # sleep

        response = self.grand_central.query_node(
            self.nodes[0],
            "GET",
            "/status"
        )

        self.grand_central.stop_nodes()
        time.sleep(1)  # sleep

        # assert
        self.assertEquals(response["status"], PlayNodeStatus.OK)

    def test_transfer_file(self):
        # start nodes and transfer file
        target = config_fp
        destination = "/tmp/config_file_test"
        self.grand_central.start_nodes()
        time.sleep(1)  # sleep

        self.grand_central.transfer_file(self.nodes[0], target, destination)

        self.grand_central.stop_nodes()
        time.sleep(1)  # sleep

        self.assertTrue(os.path.isfile(destination))
        os.unlink(destination)

    def test_check_node(self):
        # start nodes and check node
        self.grand_central.start_nodes()
        time.sleep(1)  # sleep

        status = self.grand_central.check_node(self.nodes[0])

        self.grand_central.stop_nodes()
        time.sleep(1)  # sleep

        # assert
        self.assertTrue(status)


if __name__ == '__main__':
    unittest.main()
