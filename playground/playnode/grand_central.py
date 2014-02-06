#!/bin/bash
import os
import json
import time
import httplib
import platform

import paramiko

from playground.playnode.node import PlayNodeStatus


class GrandCentral(object):
    def __init__(self, config, **kwargs):
        self.script_path = os.path.realpath(os.path.dirname(__file__))
        self.os = platform.system()
        self.nodes = config.get("playnodes", None)
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.pidfile_format = "/tmp/playground-{0}-{1}.pid"

        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def _ssh_connect(self, node):
        if self.username is None:
            self.ssh.connect(node["host"])
        else:
            self.ssh.connect(
                node["host"],
                username=self.username,
                password=self.password
            )

    def _ssh_send(self, node, cmd, output=False):
        self._ssh_connect(node)

        if self.os == "Darwin":  # Mac
            cmd = "source ~/.bash_profile; " + cmd
        elif self.os == "Linux":
            cmd = "source ~/.bashrc; " + cmd
        else:
            raise RuntimeError("Unrecogised OS type [{0}]!".format(self.os))

        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        self.ssh.close()
        if output:
            return {"stdout": ssh_stdout.read(), "stderr": ssh_stderr.read()}

    def start_node(self, node):
        # start node
        cmd = "python {0}/node.py {1} {2} {3}".format(
            self.script_path,
            node["host"],
            node["port"],
            node["type"]
        )
        print cmd
        self._ssh_send(node, cmd)

        # obtain instance pid and update node dictionary
        pidfile = self.pidfile_format.format(node["host"], node["port"])
        cmd = "cat {0}".format(pidfile)

        # try
        limit = 5
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

        print "STDOUT: ", response["stdout"]
        print "STDERR: ", response["stderr"]
        result = json.loads(response["stdout"])
        node["pid"] = result["pid"]

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
