#!/bin/bash
import os
import json
import time
import httplib
import subprocess
from subprocess import PIPE

from playground.playnode.node import PlayNodeStatus


class GrandCentral(object):
    def __init__(self, config, **kwargs):
        self.script_path = os.path.realpath(os.path.dirname(__file__))
        self.nodes = config.get("playnodes", None)
        self.pidfile_format = "/tmp/playground-{0}-{1}.pid"
        self.ssh = None

    def _ssh_send(self, node, cmd, output=False):
        ssh_cmd = ["ssh"]

        ssh_cmd.append(node["host"])
        ssh_cmd.append("'" + cmd + "'")

        if output:
            process = subprocess.Popen(ssh_cmd, stdout=PIPE, stderr=PIPE)
            out, err = process.communicate()
            return {"stdout": out, "stderr": err}
        else:
            subprocess.Popen(ssh_cmd)

    def _obtain_pid(self, node, limit=1):
        # obtain instance pid and update node dictionary
        pidfile = self.pidfile_format.format(node["host"], node["port"])
        cmd = "cat {0}".format(pidfile)

        # try
        counter = 0
        response = self._ssh_send(node, cmd, True)
        while (response["stdout"] == ""):
            time.sleep(1)  # sleep before you get the pid
            if counter == limit:
                err = "Failed to get pid for node [{0}:{1}]!".format(
                    node["host"],
                    node["port"]
                )
                raise RuntimeError(err)
            else:
                response = self._ssh_send(node, cmd, True)
                counter += 1

        result = json.loads(response["stdout"])
        return result["pid"]

    def start_node(self, node):
        # start node
        cmd = "python {0}/node.py {1} {2} {3}".format(
            self.script_path,
            node["host"],
            node["port"],
            node["type"]
        )
        print self._ssh_send(node, cmd, True)
        node["pid"] = self._obtain_pid(node)

    def stop_node(self, node):
        cmd = "kill {0}".format(node["pid"])
        self._ssh_send(node, cmd)
        node["pid"] = None

    def start_nodes(self):
        for node in self.nodes:
            self.start_node(node)

    def stop_nodes(self):
        for node in self.nodes:
            self.stop_node(node)

    def remote_check_file(self, node, target):
        cmd = "[ -f {0} ] && echo '1' || echo '0'".format(target)
        file_status = int(self._ssh_send(node, cmd, True)["stdout"])

        if file_status == 0:
            err = "File [{0}] not found in remote node [{1}]".format(
                target,
                node["host"],
            )
            raise RuntimeError(err)
        else:
            return True

    def remote_play(self, node, target, args, dest=None, **kwargs):
        python_interpreter = kwargs.get("python_interpreter", "CPYTHON")

        # precheck
        if dest:
            self.remote_check_file(node, dest)
        elif dest is None:
            self.remote_check_file(node, target)

        if python_interpreter == "CPYTHON":
            cmd = ["python", target]
        elif python_interpreter == "PYPY":
            cmd = ["pypy", target]
        cmd.extend(args)
        cmd = " ".join(cmd)

        self._ssh_send(node, cmd)

    def query_node(self, node, req_type, path, data=None):
        conn = httplib.HTTPConnection(node["host"], node["port"])
        request = "/".join(path.split("/"))
        data = None

        if data:
            conn.request(req_type, request, data)
        else:
            conn.request(req_type, request)

        # response
        response = conn.getresponse()
        data = response.read()
        conn.close()

        return json.loads(data)

    def transfer_file(self, node, source, destination):
        self._ssh_connect(node)
        sftp = self.ssh.open_sftp()
        sftp.put(source, destination)
        self.ssh.close()

    def check_node(self, node):
        response = self.query_node(node, "GET", "/status")
        if response["status"] == PlayNodeStatus.OK:
            return True
        else:
            return False
