#!/usr/bin/python3

import socket
import sys
import os
import argparse

# Functions
def receive(s, target):
    try:
        return s.recv(1024).decode().strip()
    except socket.timeout:
        print(f"ERROR/{target}/socket timeout")

# Script arguments
parser = argparse.ArgumentParser(description='SMTP enumeration tools')
parser.add_argument('mode', help='What you want the script to do either CHECK if server available or ENUM to enumerate users', choices=['CHECK', 'ENUM'])
parser.add_argument('target', help='host to perform operation on')
parser.add_argument('--users', help='file with usernames to enumerate. ENUM mode only')
args = parser.parse_args()


# Create a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(60)

# Connect to the Server
try: 
    connect = s.connect((args.target,25))
except socket.error:
    print(f"Can not connect to {args.target}")
    sys.exit(1)

# Receive the banner
banner = receive(s, args.target)
print(f"Connected to {args.target}, banner: {banner}")

# Flag to determine if enum possible
enumok = False

# CHECK mode will check if VRFY can be done on target
# Always do check before ENUM
s.send('VRFY user \r\n'.encode())
result = receive(s, args.target)
denylist = ["Cannot VRFY user", "VRFY is not supported", "503 Bad sequence"]
vulnlist = ["User unknown", "Recipient address rejected", "252 2.0.0"]
presentlist = ["250", "252"]
if any(substring in result for substring in denylist):
    print(f"NO: {args.target} not vulnerable to VRFY")
elif any(substring in result for substring in vulnlist):
    print(f"OK: {args.target} can be used to enumerate users with VRFY")
    enumok = True
else:
    print(f"ERROR: {args.target} response unknown '{result}'")

if args.mode == 'ENUM' and enumok:
    # ENUM mode to try out usernames from file
    if not os.path.isfile(args.users):
        print(f"file {args.users} not found")
        sys.exit(1)
    infile = open(args.users, 'r')
    for user in infile.readlines():
        user = user.strip()
        s.send(f'VRFY {user} \r\n'.encode())
        result = receive(s, args.target)
        basemsg = f"enum_user/{args.target}/{user}"
        if "550" in result:
            print(basemsg + "/unknown")
        elif any(substring in result for substring in presentlist):
            print(basemsg + f"/present/{result}")
        else:
            print(basemsg + f"/{result})")
    