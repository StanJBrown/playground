#!/usr/bin/env python2.7
import os
import time
import json
import socket
from multiprocessing import Pool

import paramiko
from paramiko import BadHostKeyException
from paramiko import AuthenticationException
from paramiko import SSHException


def obtain_private_key():
    priv_key_path = os.path.expanduser("~/.ssh/id_rsa")
    priv_key = None

    if os.path.isfile(priv_key_path):
        priv_key = paramiko.RSAKey.from_private_key_file(priv_key_path)

    return priv_key

def send_cmd(node, cmd, credentials):
    try:
        # setup ssh client
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # connect
        ssh.connect(
            node,
            username=credentials.get("username", None),
            password=credentials.get("password", None),
            timeout=credentials.get("timeout", 2.0),
            pkey=obtain_private_key()
        )
        stdin, stdout, stderr = ssh.exec_command(cmd)

        # wait for the command to terminate
        while not stdout.channel.exit_status_ready() and stdout.channel.recv_ready():
            time.sleep(1)

        # get output
        exit_status = stdout.channel.recv_exit_status()
        result = {
            "stdout": stdout.read(),
            "stderr": stderr.read(),
            "exit_status": exit_status,
            "exception": None
        }
        ssh.close()
        return result

    except (
        BadHostKeyException,
        AuthenticationException,
        SSHException,
        socket.error
    ) as e:
        result = {
            "stdout": None,
            "stderr": None,
            "exit_status": -1,
            "exception": str(e)
        }
        return result


def batch_send_cmd(nodes, cmd, credentials):
    results = []
    workers = []
    pool = Pool(processes=5)

    # send command async
    for node in nodes:
        worker = pool.apply_async(send_cmd, (node, cmd, credentials))
        workers.append((node, worker))

    # for every process get the results (with retry)
    for worker in workers:
        retry = 0
        node = worker[0]
        while(retry != 3):
            try:
                results.append({"node": node, "output": worker[1].get()})
                break
            except Exception:
                retry += 1
                time.sleep(1)
    del workers[:]

    return results


def test_connection(node, credentials):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    private_key_path = os.path.expanduser("~/.ssh/id_rsa")
    private_key = None
    if os.path.isfile(private_key_path):
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

    try:
        ssh.connect(
            node,
            username=credentials.get("username", None),
            password=credentials.get("password", None),
            timeout=credentials.get("timeout", 2.0),
            pkey=private_key
        )

        ssh.close()
        return (True, None)

    except (
        BadHostKeyException,
        AuthenticationException,
        SSHException,
        socket.error
    ) as e:
        return (False, str(e))


def test_connections(nodes, credentials):
    workers = []
    online_nodes = []
    offline_nodes = []

    # concurrently test connection
    pool = Pool(processes=5)
    for node in nodes:
        worker = pool.apply_async(test_connection, (node, credentials))
        workers.append((node, worker))

    # get results
    for worker in workers:
        node = worker[0]
        retry = 0
        while(retry != 3):
            try:
                result = worker[1].get()
                online = result[0]
                exception = result[1]

                if online:
                    online_nodes.append(node)
                else:
                    res = {"node": node, "exception": exception}
                    offline_nodes.append(res)
                break

            except Exception:
                retry += 1
                time.sleep(1)

        if retry == 3:
            offline_nodes.append(node)
    del workers[:]

    return (online_nodes, offline_nodes)


def deploy_public_key(nodes, pubkey_path, credentials):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # obtain public key contents
    pubkey_file = open(pubkey_path, "rb")
    pubkey = pubkey_file.read()
    pubkey_file.close()

    # authorized keys file path
    default_remote_authkeys = os.path.expanduser("~/.ssh/authorized_keys")
    authkeys = credentials.get("remote_authkeys", default_remote_authkeys)

    # add local public key to remote node's authorized_keys file
    for node in nodes:
        ssh.connect(
            node,
            username=credentials.get("username", None),
            password=credentials.get("password", None),
            timeout=credentials.get("timeout", 2.0)
        )

        # append local public key
        ssh.exec_command("echo '{0}' >> {1}".format(pubkey.strip(), authkeys))
        ssh.close()


def parse_netadaptor_details(ifconfig_dump):
    interfaces = []

    # parse ifconfig dump line by line
    netadaptor = {}
    for line in ifconfig_dump.split('\n'):
        # parsing net adaptor entry
        if len(line) > 0 and line[0] != " ":
            if len(netadaptor):
                interfaces.append(netadaptor)
                netadaptor = {}

            adaptor = line.split(" ")[0]
            adaptor = adaptor.replace(":", "")
            netadaptor["interface"] = adaptor

            # on some ifconfig dumps the mac address is on the same
            # line as the network interface
            if "HWaddr" in line.split():
                netadaptor["mac_addr"] = line[-1]

        # line ip or mac address
        else:
            line = line.split()
            if "inet" in line:
                netadaptor["ip"] = line[1]

            if "ether" in line:
                netadaptor["mac_addr"] = line[1]

    # add last net adaptor
    interfaces.append(netadaptor)

    # drop "lo" interface
    interfaces = [i for i in interfaces if i["interface"] != "lo"]

    return interfaces


def get_netadaptor_details(nodes, credentials):
    node_net_details = []

    # run `ifconfig` on nodes and get the ifconfig dump
    cmd = "ifconfig"
    results = batch_send_cmd(nodes, cmd, credentials)

    # loop through every ifconfig dump and return result
    for result in results:
        node = result["node"]
        ifconfig_dump = result["output"]["stdout"]
        details = parse_netadaptor_details(ifconfig_dump)[0]

        node_net_details.append(
            {
                "node": node,
                "ip": details["ip"],
                "mac_addr": details["mac_addr"]
            }
        )

    return node_net_details


def remote_check_file(node, target, credentials):
    cmd = "[ -f {0} ] && echo '1' || echo '0'".format(target)
    result = send_cmd(node, cmd, credentials)

    if int(result["stdout"].strip()) == 0:
        return False
    else:
        return True


def record_netadaptor_details(file_path, nodes, credentials):
    # get all net adaptor details from nodes
    net_adaptors = get_netadaptor_details(nodes, credentials)

    # write out details to file in json format
    net_adaptor_file = open(file_path, "wb")
    net_adaptors_json = json.dumps({"nodes": net_adaptors})
    net_adaptor_file.write(net_adaptors_json + "\n")
    net_adaptor_file.close()
