#!/usr/bin/env python
import os
import time
import json
import socket
import struct
from multiprocessing import Pool

import paramiko
from paramiko import BadHostKeyException
from paramiko import AuthenticationException
from paramiko import SSHException


def ssh_send_cmd(node, cmd, username, password=None, **kwargs):
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
            username=username,
            password=password,
            timeout=kwargs.get("timeout", 2.0),
            pkey=private_key
        )

        stdin, stdout, stderr = ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        ssh.close()

        result = {
            "stdout": stdout.read(),
            "stderr": stderr.read(),
            "exit_status": exit_status
        }
        return result

    except (
        BadHostKeyException,
        AuthenticationException,
        SSHException,
        socket.error
    ):
        result = {
            "stdout": None,
            "stderr": None,
            "exit_status": -1
        }
        return result


def ssh_batch_send_cmd(nodes, cmd, username, password=None):
    pool = Pool(processes=100)
    results = []

    # send command async
    for node in online_nodes:
        worker = pool.apply_async(ssh_send_cmd, (node, cmd, username))
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


def test_connection(node, username, password=None, **kwargs):
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
            username=username,
            password=password,
            timeout=kwargs.get("timeout", 2.0),
            pkey=private_key
        )

        ssh.close()
        return True

    except (
        BadHostKeyException,
        AuthenticationException,
        SSHException,
        socket.error
    ):
        return False


def test_connections(nodes, username, password=None):
    # concurrently test connection
    pool = Pool(processes=100)
    for node in nodes:
        worker = pool.apply_async(test_connection, (node, username, password))
        workers.append((node, worker))

    # get results
    online_nodes = []
    offline_nodes = []

    for worker in workers:
        node = worker[0]
        retry = 0
        while(retry != 3):
            try:
                result = worker[1].get()
                if result:
                    online_nodes.append(node)
                else:
                    offline_nodes.append(node)
                break
            except Exception:
                retry += 1
                time.sleep(1)

        if retry == 3:
            offline_nodes.append(node)
    del workers[:]

    return (online_nodes, offline_nodes)


def deploy_public_key(nodes, pubkey_path, **kwargs):
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
            timeout=kwargs.get("timeout", 2.0)
        )

        # append local public key
        ssh.exec_command("echo '{0}' >> {1}".format(pubkey, authkeys))
        ssh.close()


def parse_netadaptor_details(ifconfig_dump):
    ip = None
    mac_addr = None
    ifconfig_dump = ifconfig_dump.split()

    # find inet and ether keywords and scrape the details
    for i in range(len(ifconfig_dump)):
        if ifconfig_dump[i] == "inet":
            ip = ifconfig_dump[i + 1]
        elif ifconfig_dump[i] == "ether":
            mac_addr = ifconfig_dump[i + 1]

    return {"mac_addr": mac_addr, "ip": ip}


def get_netadaptor_details(nodes, username, password=None, **kwargs):
    node_net_details = []

    # run `ifconfig` on nodes and get the ifconfig dump
    cmd = "ifconfig"
    results = ssh_batch_send_cmd(nodes, cmd, username, password, **kwargs)

    # loop through every ifconfig dump and return result
    for result in results:
        node = result["output"]["target"]
        ifconfig_dump = result["output"]["stdout"]
        details = parse_netadaptor_details(ifconfig_dump)

        node_net_details.append(
            {
                "node": node,
                "ip": details["ip"],
                "mac_addr": details["mac_addr"]
            }
        )

    return node_net_details


def record_netadaptor_details(file_path, nodes, username, password=None):
    # get all net adaptor details from nodes
    net_adaptors = get_netadaptor_details(nodes, username)

    # write out details to file in json format
    net_adaptor_file = open(file_path, "wb")
    net_adaptors_json = json.dumps({"nodes": net_adaptors})
    net_adaptor_file.write(net_adaptors_json + "\n")
    net_adaptor_file.close()


def remote_check_file(node, target, **kwargs):
    cmd = "[ -f {0} ] && echo '1' || echo '0'".format(target)
    stdin, stdout, stderr = ssh_send_cmd(node, cmd, kwargs)

    if int(stdout) == 0:
        err = "File [{0}] not found in remote node [{1}]".format(
            target,
            node["host"],
        )
        raise RuntimeError(err)
    else:
        return True


def remote_play(node, target, args, **kwargs):
    python_interpreter = kwargs.get("python_interpreter", "CPYTHON")

    # precheck
    dest = kwargs.get("dest", None)
    if dest:
        remote_check_file(node, dest)
    else:
        remote_check_file(node, target)

    if python_interpreter == "CPYTHON":
        cmd = ["python", target]
    elif python_interpreter == "PYPY":
        cmd = ["pypy", target]
    cmd.extend(args)
    cmd = " ".join(cmd)


def send_wol_packet(dst_mac_addr):
    addr_byte = dst_mac_addr.split(':')
    hw_addr = struct.pack(
        'BBBBBB',
        int(addr_byte[0], 16),
        int(addr_byte[1], 16),
        int(addr_byte[2], 16),
        int(addr_byte[3], 16),
        int(addr_byte[4], 16),
        int(addr_byte[5], 16)
    )
    macpck = '\xff' * 6 + hw_addr * 16
    scks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    scks.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    scks.sendto(macpck, ('<broadcast>', 9))
    scks.close()


def remote_sleep_mac(node, username, password=None, **kwargs):
    cmd = "pmset sleepnow && exit"
    result = ssh_send_cmd(node, cmd, username, password, **kwargs)

    print result
    if result["exit_status"] == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    nodes = []
    workers = []

    # ssh details
    username = "cc218"

    # build nodes list
    for i in range(70):
        node = "mac1-{0}-m.cs.st-andrews.ac.uk".format(str(i).zfill(3))
        nodes.append(node)

    # query online offline nodes
    online_nodes, offline_nodes = test_connections(nodes, username)
    print "ONLINE NODES: ", len(online_nodes)
    print "OFFLINE NODES: ", len(offline_nodes)

    # send_wol_packet("34:15:9e:22:7e:08")
    # remote_sleep_mac(node, username)

    cmd = "finger"
    results = ssh_batch_send_cmd(online_nodes, cmd, username)
    for result in results:
        print result["node"]
        print result["output"]["stdout"]
        # print result["output"]


    # 34:15:9e:22:7e:08

    # cmd = "pmset sleepnow"
    # results = ssh_batch_send_cmd(online_nodes, cmd, username)
    # print results
