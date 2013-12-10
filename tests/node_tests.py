#!/usr/bin/env python
import os
import sys
import json
import signal
import socket
import time
import unittest
import subprocess
from subprocess import Popen
from subprocess import check_call
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from playground.node import PlayNode
from playground.node import PlayNodeType
from playground.node import PlayNodeState


def check_call_modify(command, output_file):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in p.stdout:
        output_file.write(line)
    p.wait()
    if p.returncode:
        raise subprocess.CalledProcessError(p.returncode, command)
    return p.returncode


class NodeTests(unittest.TestCase):
    def setUp(self):
        self.processes = 0

        file_name = str(__file__)
        host = "localhost"
        port = 8080
        listen = str(5)

        # start the playground nodes
        self.node_1 = Popen(["python", file_name, host, str(port), listen])
        self.node_2 = Popen(["python", file_name, host, str(port + 1), listen])
        self.node_3 = Popen(["python", file_name, host, str(port + 2), listen])

        # sleep for 2 seconds while the servers are starting
        time.sleep(1)

    def tearDown(self):
        # shutdown all the playground nodes
        os.kill(self.node_1.pid, signal.SIGKILL)
        os.kill(self.node_2.pid, signal.SIGKILL)
        os.kill(self.node_3.pid, signal.SIGKILL)

    def transmit(self, raw_msg):
        msg = json.dumps(raw_msg)

        print "Processes before START message!"
        processes_before = self.check_nodes()

        # send the START message
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 8080))
        s.send(msg)
        print "send[localhost:8080]: ", msg

        # get result
        raw_data = s.recv(8192)
        result = json.loads(raw_data)
        print "recieve[localhost:8080]: ", result, "\n"
        print "Processes after START message!"
        processes_after = self.check_nodes()
        print "\n\n"

        # clean up
        s.close()

        return (result, processes_before, processes_after)

    def check_nodes(self):
        check_call(["isrunning", "python"])
        print "\n"

        output = open("out", "w")
        check_call_modify(["isrunning", "python"], output)
        output.close()

        output = open("out", "r")
        processes = len(output.read().split("\n"))
        output.close()

        return processes

    def check_state(self, state):
        raw_msg = {"message": PlayNode.STATE}
        msg = json.dumps(raw_msg)

        # send the STATE message
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 8080))
        s.send(msg)

        # recieve
        raw_data = s.recv(8192)
        result = json.loads(raw_data)

        if (result["message"] == state):
            return True
        else:
            ret_state = result["message"]
            print("Error! state returned: ", ret_state, " instead of ", state)
            return False

    def test_start(self):
        raw_msg = {"message": PlayNode.START}
        result, processes_before, processes_after = self.transmit(raw_msg)

        self.assertTrue(processes_before == processes_after)
        self.assertEquals(result["message"], PlayNode.OK)
        self.assertTrue(self.check_state(PlayNodeState.ONLINE))

    def test_stop(self):
        raw_msg = {"message": PlayNode.STOP}
        result, processes_before, processes_after = self.transmit(raw_msg)

        self.assertTrue(processes_before == processes_after)
        self.assertEquals(result["message"], PlayNode.OK)
        self.assertTrue(self.check_state(PlayNodeState.OFFLINE))

    def test_kill(self):
        raw_msg = {"message": PlayNode.KILL}
        result, processes_before, processes_after = self.transmit(raw_msg)

        self.assertTrue(processes_before > processes_after)
        self.assertEquals(result["message"], PlayNode.OK)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        host = sys.argv[1]
        port = int(sys.argv[2])
        listen = int(sys.argv[3])

        node = PlayNode(PlayNodeType.EVALUATOR, host, port, listen)
        node.start()
    else:
        unittest.main()
