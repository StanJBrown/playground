#!/bin/bash
import httplib

import paramiko


class GrandCentral(object):
    def __init__(self, config, **kwargs):
        self.os = config.get("OS", "MAC")
        self.nodes = config.get("playnodes", None)
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.pidfile = "/tmp/playnode_instances.pid"

        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()

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

        if self.os == "MAC":
            cmd = "source ~/.bash_profile; " + cmd
        elif self.os == "LINUX":
            cmd = "source ~/.bashrc; " + cmd
        else:
            raise RuntimeError("Invalid OS type [{0}]!".format(self.os))

        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        if output:
            print("STDOUT: " + ssh_stdout.read())
            print("STDERR: " + ssh_stderr.read())
        self.ssh.close()

    def start_node(self, node):
        cmd = "python -m playground.playnode.node {0} {1} {2}".format(
            node["host"],
            node["port"],
            node["type"]
        )
        self._ssh_send(node, cmd)

    def stop_node(self, node):
        host = node["host"]
        port = node["port"]

        pidfile = "/tmp/playground-{0}-{1}.pid".format(host, port)
        cmd = "kill `cat {0}`".format(pidfile)
        self._ssh_send(node, cmd)

    def start_nodes(self):
        for node in self.nodes:
            self.start_node(node)

    def stop_nodes(self):
        for node in self.nodes:
            self.stop_node(node)

    def query_node(self, node, req_type, path, data=None):
        conn = httplib.HTTPConnection(node["host"], node["port"])
        request = "/".join(path.split("/"))
        data = None

        if data:
            conn.request(req_type, request, data)
        # else:
        #     conn.request(req_type, request)

        # response
        response = conn.getresponse()
        data = response.read()
        conn.close()

        return data

    def transfer_file(self, node, source, destination):
        self._ssh_connect(node)
        sftp = self.ssh.open_sftp()
        sftp.put(source, destination)
        self.ssh.close()

    def check_node(self, node):
        pass
