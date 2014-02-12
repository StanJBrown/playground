#!/usr/bin/env python
import time
import socket
from multiprocessing import Pool

import paramiko
from paramiko import BadHostKeyException
from paramiko import AuthenticationException
from paramiko import SSHException


def test_connection(node, username=None, password=None, timeout=2.0, **kwargs):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if kwargs.get("verbose", True):
            print "checking", node

        ssh.connect(
            node,
            username=username,
            password=password,
            timeout=timeout
        )

        ssh.close()
        return True
    except (
        BadHostKeyException,
        AuthenticationException,
        SSHException,
        socket.error
    ) as e:
        print node, e
        ssh.close()
        return False


def transfer_public_keys(nodes, pubkey_path, **kwargs):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # obtain public key contents
    pubkey_file = open(pubkey_path, "rb")
    pubkey = pubkey_file.read()
    pubkey_file.close()

    # authorized keys file path
    authkeys = kwargs.get("remote_authkeys_fp", "~/.ssh/authorized_keys")

    # add local public key to remote node's authorized_keys file
    for node in nodes:
        ssh.connect(
            node,
            username=kwargs.get("username", None),
            password=kwargs.get("password", None),
            timeout=0.1
        )

        # append local public key
        ssh.exec_command("echo '{0}' >> {1}".format(pubkey, authkeys))
        ssh.close()


if __name__ == "__main__":
    nodes = []
    workers = []
    online_nodes = []
    offline_nodes = []

    # ssh username, password
    username = ""
    password = ""

    # build nodes list
    for i in range(20):
        node = "mac1-{0}-m.cs.st-andrews.ac.uk".format(str(i).zfill(3))
        nodes.append(node)

    # concurrently test connection
    pool = Pool(processes=100)
    for node in nodes:
        worker = pool.apply_async(test_connection, (node, username, password))
        workers.append((node, worker))

    # get results
    for worker in workers:
        node = worker[0]

        retry = 0
        while(retry != 3):
            try:
                result = worker[1].get()
                if result:
                    print node, "ONLINE!"
                    online_nodes.append(node)
                else:
                    print node, "OFFLINE!"
                    offline_nodes.append(node)
                break
            except Exception:
                retry += 1
                time.sleep(1)

        if retry == 5:
            print node, "OFFLINE!"
            offline_nodes.append(node)

    print "ONLINE: ", online_nodes
    print "OFFLINE: ", offline_nodes
