#!/usr/bin/env python
import json
import socket
import asyncore


class PlayNodeType(object):
    EVALUATOR = "EVALUATOR"
    GRAND_CENTRAL = "GRAND_CENTRAL"


class PlayNodeState(object):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    BUSY = "BUSY"


class PlayNodeHandler(asyncore.dispatcher_with_send):
    def __init__(self, node, sock=None, map=None):
        asyncore.dispatcher_with_send.__init__(self, sock, map)
        self.node = node

    def handle_read(self):
        raw_data = self.recv(8192)
        if raw_data:
            data = json.loads(raw_data)
            return_data = {}

            if data["message"] == PlayNode.START:
                self.node.state = PlayNodeState.ONLINE

                return_data["message"] = PlayNode.OK
                self.send(json.dumps(return_data))

            elif data["message"] == PlayNode.STOP:
                self.node.state = PlayNodeState.OFFLINE

                return_data["message"] = PlayNode.OK
                self.send(json.dumps(return_data))

            elif data["message"] == PlayNode.STATE:
                return_data["message"] = self.node.state

                self.send(json.dumps(return_data))

            elif data["message"] == PlayNode.KILL:
                self.node.state = PlayNodeState.OFFLINE

                return_data["message"] = PlayNode.OK
                self.send(json.dumps(return_data))

                self.close()
                self.node.close()

            else:
                return_data["message"] = PlayNode.UNDEFINED


class PlayNode(asyncore.dispatcher):
    START = "START"
    STOP = "STOP"
    KILL = "KILL"
    OK = "OK"
    STATE = "STATE"
    EVALUATE = "EVALUATE"
    UNDEFINED = "UNDEFINED"

    def __init__(self, node_type, host, port, listen):
        self.node_type = None
        self.state = None
        self.buffer = []
        self.buffer_max_size = 8192

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def start(self, count=None):
        self.state = PlayNodeState.ONLINE
        asyncore.loop(count=count)

    def stop(self):
        self.state = PlayNodeState.OFFLINE

    def connect(self, host, port):
        self.connect((host, port))

    def handle_close(self):
        self.close()

    def handle_accept(self):
        incomming = self.accept()
        if incomming is not None:
            sock, addr = incomming
            PlayNodeHandler(self, sock)

    def handle_write(self):
        if len(self.buffer) > 0:
            data = self.buffer.pop()
            self.send(data)
