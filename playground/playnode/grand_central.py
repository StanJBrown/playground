#!/bin/bash
import httplib

import paramiko


class GrandCentral(object):
    def __init__(self, config):
        self.nodes = config.get("nodes", None)

    def _ssh_node(self, node):
        ssh = paramiko.SSHClient()

        # load ssh keys
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy())

        # ssh to node
        ssh.connect(
            node["server"],
            username=node["user"],
            password=node["password"]
        )

        return ssh

    def start_node(self, node):
        ssh = self._ssh_node(node)

        cmd = """ """
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh.close()

    def stop_node(self, node):
        ssh = self._ssh_node(node)

        cmd = """ """
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        ssh.close()

    def start_nodes(self):
        for node in self.nodes:
            self.start_node(node)

    def stop_nodes(self):
        for node in self.nodes:
            self.stop_node(node)

    def query_node(self, host, port, req_type, path, data=None):
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

    def check_node(self, node):
        pass
