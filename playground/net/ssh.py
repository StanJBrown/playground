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


def send_cmd(node, cmd, credentials):
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

        stdin, stdout, stderr = ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        ssh.close()

        result = {
            "stdout": stdout.read(),
            "stderr": stderr.read(),
            "exit_status": exit_status,
            "exception": None
        }
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
    pool = Pool(processes=100)

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
    pool = Pool(processes=100)
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
    authkeys = credentials.get("remote_authkeys_fp", "~/.ssh/authorized_keys")

    # add local public key to remote node's authorized_keys file
    for node in nodes:
        ssh.connect(
            node,
            username=credentials.get("username", None),
            password=credentials.get("password", None),
            timeout=credentials.get("timeout", 2.0)
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


def get_netadaptor_details(nodes, credentials):
    node_net_details = []

    # run `ifconfig` on nodes and get the ifconfig dump
    cmd = "ifconfig"
    results = batch_send_cmd(nodes, cmd, credentials)

    # loop through every ifconfig dump and return result
    for result in results:
        node = result["node"]
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


def remote_sleep_mac(node, credentials):
    cmd = "pmset sleepnow && exit"
    result = send_cmd(node, cmd, credentials)

    if int(result["stdout"].strip()) == 0:
        return True
    else:
        return False


def remote_sleep_macs(nodes, credentials):
    workers = []
    sleep_nodes = []
    fail_nodes = []

    # concurrently test connection
    pool = Pool(processes=100)
    for node in nodes:
        worker = pool.apply_async(remote_sleep_mac, (node, credentials))
        workers.append((node, worker))

    # get results
    for worker in workers:
        node = worker[0]
        retry = 0
        while(retry != 3):
            try:
                result = worker[1].get()
                sleep = result[0]

                if sleep:
                    sleep_nodes.append(node)
                else:
                    res = {"node": node, "exception": "Failed to sleep mac!"}
                    fail_nodes.append(res)
                break

            except Exception:
                retry += 1
                time.sleep(1)

        if retry == 3:
            fail_nodes.append(node)
    del workers[:]

    return (sleep_nodes, fail_nodes)


def remote_play(node, target, args, credentials, **kwargs):
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


if __name__ == "__main__":
    nodes = []
    workers = []

    # ssh credentials
    credentials = {
        "username": "cc218"
    }

    # build nodes list
    for i in [62, 63]:
        node = "mac1-{0}-m.cs.st-andrews.ac.uk".format(str(i).zfill(3))
        nodes.append(node)

    # query online offline nodes
    online_nodes, offline_nodes = test_connections(nodes, credentials)
    print "ONLINE NODES: ", len(online_nodes)
    print "OFFLINE NODES: ", len(offline_nodes)

    # send_wol_packet("34:15:9e:22:7e:08")
    print remote_sleep_mac(online_nodes[0], credentials)
    # sleep_nodes, failed_nodes = remote_sleep_macs(online_nodes, credentials)
    # print "SLEEP NODES: ", len(sleep_nodes)
    # print "FAILED NODES: ", len(failed_nodes)


    # cmd = "ls"
    # results = batch_send_cmd(online_nodes, cmd, credentials)
    # for result in results:
    #     print result["node"]
    #     print result["output"]["stdout"]
