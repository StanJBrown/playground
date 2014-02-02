#!/bin/bash
import httplib


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


class GrandCentral(object):
    def __init__(self, config):
        self.nodes = config.get("nodes", None)

    def start_node(self, node):
        pass

    def stop_node(self, node):
        pass

    def start_nodes(self):
        for node in self.nodes:
            self.start_node(node)

    def stop_nodes(self):
        for node in self.nodes:
            self.stop_node(node)

    def check_node(self, node):
        pass
