#!/usr/bin/env python
import os
import sys
import json
import httplib
import time
import unittest
import subprocess
from subprocess import Popen
from subprocess import check_call
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from playnode.playnode import PlayNodeType
from playnode.playnode import PlayNodeMessage

# SETTINGS
n_script = "playnode/play/node.py"


def check_call_modify(command, output_file):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in p.stdout:
        output_file.write(line)
    p.wait()
    if p.returncode:
        raise subprocess.CalledProcessError(p.returncode, command)
    return p.returncode


class PlayNodeTests(unittest.TestCase):
    def setUp(self):
        self.processes = 0

        host = "localhost"
        self.ports = ["8080", "8081", "8082"]
        ntype = PlayNodeType.EVALUATOR

        # start the playground nodes
        Popen(["python", n_script, host, self.ports[0], ntype])
        Popen(["python", n_script, host, self.ports[1], ntype])
        Popen(["python", n_script, host, self.ports[2], ntype])

        # sleep for 2 seconds while the servers are starting
        time.sleep(1)

    def tearDown(self):
        # shutdown all the playground nodes
        for port in self.ports:
            print("Shuttung down server at port: %s" % port)
            self.transmit("localhost", port, "GET", "shutdown")

    def transmit(self, host, port, req_type, path, data=None):
        request = "/" + path

        # transmit
        conn = httplib.HTTPConnection(host, port)
        if data:
            conn.request(req_type, request, data)
        else:
            conn.request(req_type, request)

        # response
        response = conn.getresponse()
        data = response.read()
        conn.close()

        return data

    def check_nodes(self):
        check_call(["isrunning", "python"])
        print "\n"

        output = open("out", "w")
        check_call_modify(["isrunning", "python"], output)
        output.close()

        output = open("out", "r")
        processes = len(output.read().split("\n"))
        output.close()
        os.remove("out")

        return processes

    def check_state(self, host, port, state):
        data = self.transmit(host, port, "GET", "state")
        data = json.dumps(data)

        if (data["state"] == state):
            return True
        else:
            return False

    def test_message(self):
        msg = json.dumps({"message": "Hello World"})
        data = self.transmit("localhost", 8080, "POST", "message", msg)
        data = json.loads(data)

        self.assertEquals(data["message"], PlayNodeMessage.UNDEFINED)

    def test_shutdown(self):
        servers_before = self.check_nodes()
        self.transmit("localhost", 8080, "GET", "shutdown")
        servers_after = self.check_nodes()

        self.ports.remove("8080")
        self.assertTrue(servers_before > servers_after)


if __name__ == '__main__':
    unittest.main()
