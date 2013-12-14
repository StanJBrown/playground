#!/usr/bin/env python
import os
import sys
import json
import signal
import httplib
import time
import unittest
import subprocess
from subprocess import Popen
from subprocess import check_call
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from playground.node.node import PlayNode
from playground.node.node import PlayNodeType

# SETTINGS
node_script = "playground/node/node.py"


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
        port = 8080
        ntype = PlayNodeType.EVALUATOR

        # start the playground nodes
        self.node_1 = Popen(["python", node_script, host, str(port), ntype])
        # self.node_2 = Popen(["python", fname, host, str(port + 1), listen])
        # self.node_3 = Popen(["python", fname, host, str(port + 2), listen])

        # sleep for 2 seconds while the servers are starting
        time.sleep(1)

    def tearDown(self):
        # shutdown all the playground nodes
        os.kill(self.node_1.pid, signal.SIGKILL)
        # os.kill(self.node_2.pid, signal.SIGKILL)
        # os.kill(self.node_3.pid, signal.SIGKILL)

    # def transmit(self, raw_msg, host, port, path):
    #     msg = json.dumps(raw_msg)

        # print "Processes before START message!"
        # processes_before = self.check_nodes()

        # # send message
        # conn = httplib.HTTPConnection(host, port)
        # conn.request("GET", "/", path)
        # response = conn.getresponse()
        # msg = response.msg
        # print "send[localhost:8080]: ", msg

        # # get result
        # raw_data = s.recv(8192)
        # result = json.loads(raw_data)
        # time.sleep(1)
        # print "recieve[localhost:8080]: ", result, "\n"
        # print "Processes after message!"
        # processes_after = self.check_nodes()
        # print "\n\n"

        # # clean up
        # s.close()

        # return (result, processes_before, processes_after)

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
        conn = httplib.HTTPConnection(host, port)
        conn.request("GET", "/state")
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()

        if (data["state"] == state):
            return True
        else:
            return False

    def test_state(self):
        result = self.check_state("localhost", 8080, PlayNode.RUNNING)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
