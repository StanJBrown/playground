#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import playground.net.ssh as ssh

# SETTINGS
cwd = os.path.dirname(__file__)


class SSHTests(unittest.TestCase):
    def test_send_cmd(self):
        # pass test
        result = ssh.send_cmd("localhost", "ls", {})
        self.assertEquals(result["exit_status"], 0)
        self.assertTrue(len(result["stdout"]) > 0)

        # fail test
        result = ssh.send_cmd("randomhost", "ls", {})
        self.assertEquals(result["exit_status"], -1)
        self.assertEquals(result["stdout"], None)
        self.assertEquals(result["stderr"], None)

    def test_batch_send_cmd(self):
        # pass test
        result = ssh.send_cmd("localhost", "ls", {})
        self.assertEquals(result["exit_status"], 0)
        self.assertTrue(len(result["stdout"]) > 0)

        # fail test
        result = ssh.send_cmd("random", "ls", {})
        self.assertEquals(result["exit_status"], -1)
        self.assertEquals(result["stdout"], None)
        self.assertEquals(result["stderr"], None)
        self.assertTrue(len(result["exception"]) > 0)

    def test_test_connection(self):
        # pass test
        result = ssh.test_connection("localhost", {})
        self.assertTrue(result[0])

        # fail test
        result = ssh.test_connection("randomhost", {})
        self.assertFalse(result[0])
        self.assertTrue(len(result[1]) > 0)

    def test_test_connections(self):
        nodes = ["localhost"]

        # pass test
        online_nodes, offline_nodes = ssh.test_connections(nodes, {})
        self.assertEquals(len(online_nodes), 1)
        self.assertEquals(len(offline_nodes), 0)

        # fail test
        online_nodes, offline_nodes = ssh.test_connections(["x"], {})
        self.assertEquals(len(online_nodes), 0)
        self.assertEquals(len(offline_nodes), 1)

    def test_parse_netadaptor_details(self):
        result = ssh.send_cmd("localhost", "ifconfig", {})
        result = ssh.parse_netadaptor_details(result["stdout"])

        self.assertTrue(result["ip"] is not None)
        self.assertTrue(result["mac_addr"] is not None)

    def test_get_netadaptor_details(self):
        nodes = ["localhost"]
        result = ssh.get_netadaptor_details(nodes, {})[0]

        # assert
        self.assertTrue(result["node"] is not None)
        self.assertTrue(result["mac_addr"] is not None)

    def test_record_netadaptor_details(self):
        test_fp = "test.json"
        nodes = ["localhost"]

        # record net adaptor details
        ssh.record_netadaptor_details(test_fp, nodes, {})

        # assert
        test_file = open(test_fp, "r")
        test_file_contents = test_file.read()
        test_file.close()
        os.unlink(test_fp)

        self.assertTrue(len(test_file_contents) > 0)

    def test_remote_check_file(self):
        node = "localhost"
        ssh.send_cmd(node, "touch test.txt", {})
        pass_target = os.path.expanduser("~/test.txt")
        fail_target = os.path.expanduser("~/non-existent-file")

        # pass test
        result = ssh.remote_check_file(node, pass_target, {})
        self.assertTrue(result)

        # fail test
        result = ssh.remote_check_file(node, fail_target, {})
        self.assertFalse(result)

        os.unlink(pass_target)


if __name__ == '__main__':
    unittest.main()
