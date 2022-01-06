#!/usr/bin/python3

import subprocess
import ipaddress
import argparse

# Script arguments
parser = argparse.ArgumentParser(description='IP sweeper')
parser.add_argument('range', help='IP range in CIDR notation')
args = parser.parse_args()

# Get list of IPs to scan
range = ipaddress.ip_network(args.range)

for ip in range:
    ip = str(ip)
    # Make use of local ping command to do ping
    result = subprocess.run(["ping", "-t", "2", "-c", "1", ip], capture_output=True)
    if result.returncode == 0:
        # Get the average response time from the output
        latency = result.stdout.decode().split('\n')[-2].split()[-2].split('/')[-2]
        output = f"OK {latency}"
    elif result.returncode == 1:
        output = "NA"
    else:
        output = "ERROR"
    print(ip, output)
