# playground.net.ssh
The `ssh` module contains code to perform command line actions to the remote
host via SSH. This module can utilize multiple processes (i.e. batch mode) to
communicate to multiple machines at the same time, greatly saving time compared to
sending commands sequentially.

Module contents:

- send_cmd(node, cmd, credentials)
- batch_send_cmd(nodes, cmd, credentials)
- test_connection(node, credentials)
- test_connections(nodes, credentials)
- deploy_public_key(nodes, pubkey_path, credentials)
- parse_netadaptor_details(ifconfig_dump)
- get_netadaptor_details(nodes, credentials)
- remote_check_file(node, target, credentials)
- record_netadaptor_details(file_path, nodes, credentials)
- send_wol_packet(dst_mac_addr)
- send_wol_packets(net_adaptor_details)
- remote_sleep_mac(node, credentials)
- remote_sleep_macs(nodes, credentials)
- remote_play(node, target, args, credentials, **kwargs)

## send_cmd(node, cmd, credentials)


## batch_send_cmd(nodes, cmd, credentials)


## test_connection(node, credentials)


## test_connections(nodes, credentials)


## deploy_public_key(nodes, pubkey_path, credentials)


## parse_netadaptor_details(ifconfig_dump)


## get_netadaptor_details(nodes, credentials)


## remote_check_file(node, target, credentials)


## record_netadaptor_details(file_path, nodes, credentials)


## send_wol_packet(dst_mac_addr)

## send_wol_packets(net_adaptor_details)


## remote_sleep_mac(node, credentials)


## remote_sleep_macs(nodes, credentials)


## remote_play(node, target, args, credentials, **kwargs)
